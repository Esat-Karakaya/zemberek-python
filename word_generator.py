from utils import get_morphotactics, match_capitilization
from zemberek.morphology.morphotactics.morpheme import Morpheme
from zemberek.morphology.lexicon.dictionary_item import DictionaryItem
from zemberek.morphology.morphotactics.stem_transition import StemTransition
from zemberek.core.turkish.root_attribute import RootAttribute
from zemberek.core.turkish import PhoneticAttribute
from zemberek.morphology.analysis.attributes_helper import AttributesHelper
from zemberek.core.turkish.primary_pos import PrimaryPos
from zemberek.core.turkish.secondary_pos import SecondaryPos
from zemberek.core.turkish.turkish_alphabet import TurkishAlphabet
from zemberek.morphology.generator.word_generator import WordGenerator
from dictionary import morpheme_map
from zemberek.morphology.analysis.tr.pronunciation_guesser import PronunciationGuesser
import logging
from typing import List, Union, Literal, Set

class CustomWordGenerator:
    def __init__(self):
        self.guesser = PronunciationGuesser()
        self.alphabet = TurkishAlphabet.INSTANCE
        self.morphotactics = get_morphotactics()

    def generate_word(self, root: str, primary_pos: Literal["Noun", "Verb", "NamedEntity"], suffixes: Union[List[Morpheme], List[str]]) -> str:
        """Generate a word form using Zemberek's WordGenerator.
        
        Handles dictionary items, unknown words, and NamedEntity special logic.
        """
        if not suffixes:
            return root

        # Convert suffix identifiers to Morpheme objects
        suffix_objs = [s if isinstance(s, Morpheme) else morpheme_map[s] for s in suffixes]

        generator = WordGenerator(self.morphotactics)
        lexicon = self.morphotactics.get_root_lexicon()

        # Map input POS to internal Enums
        p_pos = PrimaryPos.Noun if primary_pos in ["Noun", "NamedEntity"] else PrimaryPos.Verb
        s_pos = SecondaryPos.ProperNoun if primary_pos == "NamedEntity" else SecondaryPos.None_

        # Find candidate StemTransitions
        candidates = []
        
        # 1. Look in Lexicon

        lex_key = root
        if primary_pos == "Verb":
            lex_key = self.add_Inf1_suffix(root)
        matching_items = [item for item in lexicon.item_map.get(lex_key, []) if item.primary_pos == p_pos]
        
        # If no match and capitalization is standard (Title or Upper), try lowercase lookup
        if not matching_items and (root.istitle() or root.isupper()):
            alphabet = TurkishAlphabet.INSTANCE
            alt_lex_key = root.translate(alphabet.lower_map).lower()
            if primary_pos == "Verb":
                alt_lex_key = self.add_Inf1_suffix(alt_lex_key)
            matching_items = [item for item in lexicon.item_map.get(alt_lex_key, []) if item.primary_pos == p_pos]
        if primary_pos == "NamedEntity":
            # Prefer ProperNoun entries if they exist
            proper_items = [item for item in matching_items if item.secondary_pos == SecondaryPos.ProperNoun]
            if proper_items:
                matching_items = proper_items

        for item in matching_items:
            if primary_pos == "NamedEntity":
                # For NamedEntity, we want to ensure no stem changes even if lexicon says otherwise
                # Create a synthetic candidate based on this item but with no modifying attributes
                # and surface strictly equal to root
                start_state = self.morphotactics.noun_S
                phonetic_attrs = self._get_phonetic_attributes(root)
                candidates.append(StemTransition(root, item, phonetic_attrs, start_state))
            else:
                candidates.extend(self.morphotactics.stem_transitions.get_transitions_for_item(item))

        # 2. If no candidates found, or for generic unknown words, create synthetic transition
        if not candidates:
            new_stem_transition = self.create_stem_transition(root, p_pos, s_pos)
            candidates.append(new_stem_transition)

        # Generate
        results = generator.generate(morphemes=tuple(suffix_objs), candidates=tuple(candidates))
        
        if results:
            generated_surface = results[0].surface
            # 3. Post-process NamedEntity or Number: add apostrophe
            is_named_entity = primary_pos == "NamedEntity"
            is_number = self.alphabet.contains_digit(root)
            if (is_named_entity or is_number) and generated_surface != root:
                # We assume the generator kept the root intact because we suppressed stem changes
                if generated_surface.startswith(root):
                    return root + "'" + generated_surface[len(root):]
            return match_capitilization(root, generated_surface)

        forced_result = self.force_suffixes_on_word(root, primary_pos=="NamedEntity", suffix_objs)
        return match_capitilization(root, forced_result)

    def force_suffixes_on_word(self, root: str, is_named_entity: bool, suffixes: List[Morpheme]) -> str:
        logging.warning(
            f"Couldn't add suffixes: {[s.id_ for s in suffixes]} to \"{root}\" "
            f"via zemberek's own method. Deploying work around"
        )
        
        generator = WordGenerator(self.morphotactics)
        
        current_surface = root
        apostrophe_added = False
        
        for suffix in suffixes:

            if suffix.id_=="Rel":
                current_surface+="ki"
                continue

            possible_pos = self.get_primary_pos_for_suffix(suffix)
            
            success = False
            # Try each possible PrimaryPos until one works
            for p_pos in possible_pos:
                # We treat the current surface as a new "stem" to bypass morphotactic restrictions
                s_pos = SecondaryPos.ProperNoun if is_named_entity and not apostrophe_added else SecondaryPos.None_
                
                candidate = self.create_stem_transition(current_surface, p_pos, s_pos)
                
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
    
    def get_primary_pos_for_suffix(self, morpheme: Morpheme) -> List[PrimaryPos]:
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

    def is_single_syllable(self, word: str) -> bool:
        from zemberek.core.turkish.turkish_alphabet import TurkishAlphabet
        vowel_count = sum(1 for char in word if TurkishAlphabet.INSTANCE.is_vowel(char))
        return vowel_count == 1

    def add_Inf1_suffix(self, verb: str) -> str:
        alphabet =TurkishAlphabet()
        is_frontal = alphabet.get_last_vowel(verb).is_frontal()
        sfx = "mek" if is_frontal else "mak"
        return verb+sfx

    def create_stem_transition(self, root: str, p_pos: PrimaryPos, s_pos: SecondaryPos = SecondaryPos.None_) -> StemTransition:
        attributes = set()
        if p_pos == PrimaryPos.Verb:
            if self.is_single_syllable(root):
                attributes.add(RootAttribute.Aorist_A)
            else:
                attributes.add(RootAttribute.Aorist_I)
        
        dummy_item = DictionaryItem(root, root, p_pos, s_pos, attributes=attributes)
        start_state = self.morphotactics.verbRoot_S if p_pos == PrimaryPos.Verb else self.morphotactics.noun_S
        phonetic_attrs = self._get_phonetic_attributes(root)
        res = StemTransition(root, dummy_item, phonetic_attrs, start_state)
        return res

    def _get_phonetic_attributes(self, root: str) -> Set[PhoneticAttribute]:
        """Get phonetic attributes for a root string.
        
        If the root contains digits, uses its pronunciation to derive correct attributes.
        """
        if self.alphabet.contains_digit(root):
            pronunciation = self.guesser.to_turkish_letter_pronunciation_with_digit(root)
            return AttributesHelper.get_morphemic_attributes(pronunciation)
        return AttributesHelper.get_morphemic_attributes(root)