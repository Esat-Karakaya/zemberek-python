from typing import List, Union, Literal
from zemberek.core.turkish.primary_pos import PrimaryPos
from zemberek.core.turkish.secondary_pos import SecondaryPos
from zemberek.morphology.morphotactics.morpheme import Morpheme
from zemberek.morphology.lexicon.dictionary_item import DictionaryItem
from zemberek.morphology.morphotactics.stem_transition import StemTransition
from zemberek.morphology.analysis.attributes_helper import AttributesHelper
from zemberek.morphology.generator.word_generator import WordGenerator
from dictionary import morpheme_map
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
    matching_items = [item for item in lexicon.item_map.get(root, []) if item.primary_pos == p_pos]
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
        dummy_item = DictionaryItem(root, root, p_pos, s_pos)
        start_state = morphotactics.verbRoot_S if p_pos == PrimaryPos.Verb else morphotactics.noun_S
        phonetic_attrs = AttributesHelper.get_morphemic_attributes(root)
        candidates.append(StemTransition(root, dummy_item, phonetic_attrs, start_state))

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

    return root

def force_suffixes_on_word(root: str, is_named_entity: bool, suffixes: List[Morpheme]) -> str:
    logging.warning(
        f"Warning\n adding suffixes: {[s.id_ for s in suffixes]} to the stem: {root} "
        f"was not possible with zemberek's built in method. Deploying work around"
        )

    """@utils.py#L85-86 
complete this function so that even completely broken word generation requests can be fulfilled."""