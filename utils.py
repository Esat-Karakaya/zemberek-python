from typing import List, Union, Literal
from zemberek.core.turkish.primary_pos import PrimaryPos
from zemberek.core.turkish.secondary_pos import SecondaryPos
from zemberek.morphology.morphotactics.morpheme import Morpheme
from zemberek.morphology.lexicon.dictionary_item import DictionaryItem
from zemberek.morphology.morphotactics.stem_transition import StemTransition
from zemberek.morphology.analysis.attributes_helper import AttributesHelper
from zemberek.morphology.generator.word_generator import WordGenerator
from dictionary import morpheme_map
from zemberek.core.turkish.root_attribute import RootAttribute
from zemberek.core.turkish.turkish_alphabet import TurkishAlphabet
import logging

_morphotactics = None

def get_morphotactics():
    global _morphotactics
    if _morphotactics is None:
        from zemberek.morphology.lexicon.root_lexicon import RootLexicon
        from zemberek.morphology.morphotactics.turkish_morphotactics import TurkishMorphotactics
        lexicon = RootLexicon.get_default()
        _morphotactics = TurkishMorphotactics(lexicon)
    return _morphotactics

def generate_word(root: str, primary_pos: Literal["Noun", "Verb", "NamedEntity"], suffixes: Union[List[Morpheme], List[str]]) -> str:
    """Generate a word form using Zemberek's WordGenerator.
    
    Handles dictionary items, unknown words, and NamedEntity special logic.
    """
    if not suffixes:
        return root

    # Convert suffix identifiers to Morpheme objects
    suffix_objs = [s if isinstance(s, Morpheme) else morpheme_map[s] for s in suffixes]

    morphotactics = get_morphotactics()
    generator = WordGenerator(morphotactics)
    lexicon = morphotactics.get_root_lexicon()

    # Map input POS to internal Enums
    p_pos = PrimaryPos.Noun if primary_pos in ["Noun", "NamedEntity"] else PrimaryPos.Verb
    s_pos = SecondaryPos.ProperNoun if primary_pos == "NamedEntity" else SecondaryPos.None_

    # Find candidate StemTransitions
    candidates = []
    
    # 1. Look in Lexicon

    lex_key = root
    if primary_pos == "Verb":
        lex_key = add_Inf1_suffix(root)
    matching_items = [item for item in lexicon.item_map.get(lex_key, []) if item.primary_pos == p_pos]
    if primary_pos == "NamedEntity":
        # Prefer ProperNoun entries if they exist
        proper_items = [item for item in matching_items if item.secondary_pos == SecondaryPos.ProperNoun]
        if proper_items:
            matching_items = proper_items

    for item in matching_items:
        # For NamedEntity, we want to ensure no stem changes even if lexicon says otherwise
        if primary_pos == "NamedEntity":
            # Create a synthetic candidate based on this item but with no modifying attributes
            # and surface strictly equal to root
            start_state = morphotactics.noun_S
            phonetic_attrs = AttributesHelper.get_morphemic_attributes(root)
            candidates.append(StemTransition(root, item, phonetic_attrs, start_state))
        else:
            candidates.extend(morphotactics.stem_transitions.get_transitions_for_item(item))

    # 2. If no candidates found, or for generic unknown words, create synthetic transition
    if not candidates:
        new_stem_transition = create_stem_transition(root, p_pos, s_pos)
        candidates.append(new_stem_transition)

    # Generate
    results = generator.generate(morphemes=tuple(suffix_objs), candidates=tuple(candidates))
    
    if results:
        generated_surface = results[0].surface
        # 3. Post-process NamedEntity: add apostrophe
        if primary_pos == "NamedEntity" and generated_surface != root:
            # We assume the generator kept the root intact because we suppressed stem changes
            if generated_surface.startswith(root):
                return root + "'" + generated_surface[len(root):]
        return generated_surface

    return force_suffixes_on_word(root, primary_pos=="NamedEntity", suffix_objs)

def force_suffixes_on_word(root: str, is_named_entity: bool, suffixes: List[Morpheme]) -> str:
    logging.warning(
        f"Couldn't add suffixes: {[s.id_ for s in suffixes]} to \"{root}\" "
        f"via zemberek's own method. Deploying work around"
    )
    
    morphotactics = get_morphotactics()
    generator = WordGenerator(morphotactics)
    
    current_surface = root
    apostrophe_added = False
    
    for suffix in suffixes:

        if suffix.id_=="Rel":
            current_surface+="ki"
            continue

        possible_pos = get_primary_pos_for_suffix(suffix)
        
        success = False
        # Try each possible PrimaryPos until one works
        for p_pos in possible_pos:
            # We treat the current surface as a new "stem" to bypass morphotactic restrictions
            s_pos = SecondaryPos.ProperNoun if is_named_entity and not apostrophe_added else SecondaryPos.None_
            
            candidate = create_stem_transition(current_surface, p_pos, s_pos)
            
            results = generator.generate(morphemes=(suffix,), candidates=(candidate,))
            if results:
                generated_surface = results[0].surface
                
                # Handle NamedEntity apostrophe
                if is_named_entity and not apostrophe_added and generated_surface != current_surface:
                    if generated_surface.startswith(current_surface):
                        suffix_surface = generated_surface[len(current_surface):]
                        current_surface = f"{current_surface}'{suffix_surface}"
                        apostrophe_added = True
                    else:
                        # Fallback if it doesn't start with root for some reason (e.g. softening)
                        current_surface = generated_surface
                else:
                    current_surface = generated_surface
                
                success = True
                break
        
        if not success:
            # If even the reset fails, we might just have to skip or append literally
            logging.error(f"Could not generate suffix {suffix.id_} for {current_surface}")
            
    return current_surface

def get_primary_pos_for_suffix(morpheme: Morpheme) -> List[PrimaryPos]:
    m_id = morpheme.id_
    
    noun_suffixes = {
        "Pnon", "P1sg", "P2sg", "P3sg", "P1pl", "P2pl", "P3pl", "Nom", "Dat", "Acc", "Abl", "Loc", "Ins", "Gen", "Equ",
        "Dim", "Ness", "With", "Without", "Related", "JustLike", "Rel", "Agt", "Become", "Acquire", "Ly", "Zero", "Root",
        "A1sg", "A2sg", "A3sg", "A1pl", "A2pl", "A3pl", "Past", "Narr", "Cond", "Cop", "Noun"
    }
    
    verb_suffixes = {
        "Caus", "Recip", "Reflex", "Able", "Pass", "Neg", "Unable", "Pres", "Prog1", "Prog2", "Aor", "Fut", "Imp",
        "Opt", "Desr", "Neces", "Inf1", "Inf2", "Inf3", "ActOf", "PastPart", "NarrPart", "FutPart", "PresPart", "AorPart",
        "NotState", "FeelLike", "EverSince", "Repeat", "Almost", "Hastily", "Stay", "Start", "AsIf", "While",
        "When", "SinceDoingSo", "AsLongAs", "ByDoingSo", "Adamantly", "AfterDoingSo", "WithoutHavingDoneSo",
        "WithoutBeingAbleToHaveDoneSo", "A1sg", "A2sg", "A3sg", "A1pl", "A2pl", "A3pl", "Past", "Narr", "Cond", "Cop", "Verb"
    }

    results = []
    if m_id in noun_suffixes: results.append(PrimaryPos.Noun)
    if m_id in verb_suffixes: results.append(PrimaryPos.Verb)
    
    if results: return results

    return [PrimaryPos.Unknown]

def is_single_syllable(word: str) -> bool:
    from zemberek.core.turkish.turkish_alphabet import TurkishAlphabet
    vowel_count = sum(1 for char in word if TurkishAlphabet.INSTANCE.is_vowel(char))
    return vowel_count == 1

def add_Inf1_suffix(verb: str) -> str:
    alphabet =TurkishAlphabet()
    is_frontal = alphabet.get_last_vowel(verb).is_frontal()
    sfx = "mek" if is_frontal else "mak"
    return verb+sfx

def create_stem_transition(root: str, p_pos: PrimaryPos, s_pos: SecondaryPos = SecondaryPos.None_) -> StemTransition:
    attributes = set()
    if p_pos == PrimaryPos.Verb:
        if is_single_syllable(root):
            attributes.add(RootAttribute.Aorist_A)
        else:
            attributes.add(RootAttribute.Aorist_I)
    
    morphotactics = get_morphotactics()

    dummy_item = DictionaryItem(root, root, p_pos, s_pos, attributes=attributes)
    start_state = morphotactics.verbRoot_S if p_pos == PrimaryPos.Verb else morphotactics.noun_S
    phonetic_attrs = AttributesHelper.get_morphemic_attributes(root)
    res = StemTransition(root, dummy_item, phonetic_attrs, start_state)
    return res

