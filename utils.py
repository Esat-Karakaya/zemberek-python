from typing import List, Union, Literal
from zemberek.core.turkish.primary_pos import PrimaryPos
from zemberek.morphology.morphotactics.morpheme import Morpheme
from zemberek.morphology.morphotactics.turkish_morphotactics import get_morpheme_map
from dictionary import morpheme_map
from zemberek.morphology.generator.word_generator import WordGenerator

def get_primary_pos_for_suffix(morpheme: Morpheme) -> List[PrimaryPos]:
    """
    Returns a list of possible PrimaryPos categories (Noun or Verb) for a word root 
    to receive the given suffix. In Turkish, many suffixes (person markers, copulas, 
    tense markers) can attach to both nominal and verbal roots.
    """
    m_id = morpheme.id_
    
    # Strictly Noun-targeting suffixes: Case, Possession, and Nominal Derivations
    strictly_noun_suffixes = {
        "Pnon", "P1sg", "P2sg", "P3sg", "P1pl", "P2pl", "P3pl",
        "Nom", "Dat", "Acc", "Abl", "Loc", "Ins", "Gen", "Equ",
        "Dim", "Ness", "With", "Without", "Related", "JustLike", "Rel", "Agt",
        "Become", "Acquire", "Ly", "Zero", "Root"
    }
    
    # Strictly Verb-targeting suffixes: Voice, Aspect, and Verbal Derivations
    strictly_verb_suffixes = {
        "Caus", "Recip", "Reflex", "Able", "Pass", "Neg",
        "Unable", "Pres", "Prog1", "Prog2", "Aor", "Fut", "Imp", "Opt", "Desr", "Neces",
        "Inf1", "Inf2", "Inf3", "ActOf",
        "PastPart", "NarrPart", "FutPart", "PresPart", "AorPart",
        "NotState", "FeelLike", "EverSince", "Repeat", "Almost", "Hastily", "Stay", "Start",
        "AsIf", "While", "When", "SinceDoingSo", "AsLongAs", "ByDoingSo",
        "Adamantly", "AfterDoingSo", "WithoutHavingDoneSo", "WithoutBeingAbleToHaveDoneSo"
    }

    # Suffixes that attach to both: Person markers and Copular Tense/Aspect
    # In Turkish, nominals can be used as predicates and receive person/tense/copula markers.
    overlapping_suffixes = {
        "A1sg", "A2sg", "A3sg", "A1pl", "A2pl", "A3pl",
        "Past", "Narr", "Cond", "Cop"
    }
    
    results = []
    if m_id in strictly_noun_suffixes or m_id in overlapping_suffixes:
        results.append(PrimaryPos.Noun)
    if m_id in strictly_verb_suffixes or m_id in overlapping_suffixes:
        results.append(PrimaryPos.Verb)
    
    if results:
        return results

    # If the morpheme is a POS marker itself, return that POS
    pos_map = {
        "Noun": PrimaryPos.Noun,
        "Adj": PrimaryPos.Adjective,
        "Verb": PrimaryPos.Verb,
        "Pron": PrimaryPos.Pronoun,
        "Adv": PrimaryPos.Adverb,
        "Conj": PrimaryPos.Conjunction,
        "Punc": PrimaryPos.Punctuation,
        "Ques": PrimaryPos.Question,
        "Postp": PrimaryPos.PostPositive,
        "Det": PrimaryPos.Determiner,
        "Num": PrimaryPos.Numeral,
        "Dup": PrimaryPos.Duplicator,
        "Interj": PrimaryPos.Interjection
    }
    
    if m_id in pos_map:
        return [pos_map[m_id]]
        
    return [PrimaryPos.Unknown]

_morphotactics = None

def get_morphotactics():
    global _morphotactics
    if _morphotactics is None:
        from zemberek.morphology.lexicon.root_lexicon import RootLexicon
        from zemberek.morphology.morphotactics.turkish_morphotactics import TurkishMorphotactics
        lexicon = RootLexicon.get_default()
        _morphotactics = TurkishMorphotactics(lexicon)
    return _morphotactics

def guess_primary_pos_given_suffixes(root: str, suffixes: List[Morpheme]) -> List[PrimaryPos]:

    morphotactics = get_morphotactics()
    candidate_pos_list = []
    
    # A. Check Dictionary
    lexicon = morphotactics.get_root_lexicon()
    if lexicon:
        dict_items = lexicon.item_map.get(root, [])
        for item in dict_items:
            if item.primary_pos not in candidate_pos_list:
                candidate_pos_list.append(item.primary_pos)
    
    # B. Check Suffix Constraints
    first_suffix_morpheme = suffixes[0]
    suffix_allowed_pos = get_primary_pos_for_suffix(first_suffix_morpheme)
    
    final_candidates = []
    
    # Merge lists prioritizing dictionary matches that agree with suffix
    for pos in candidate_pos_list:
        if pos in suffix_allowed_pos:
            final_candidates.append(pos)
            
    for pos in suffix_allowed_pos:
        if pos not in final_candidates:
            final_candidates.append(pos)
            
    for pos in candidate_pos_list:
        if pos not in final_candidates:
            final_candidates.append(pos)
            
    if not final_candidates:
        final_candidates = [PrimaryPos.Noun]
    
    return final_candidates

def generate_word(root: str, primary_pos: Literal["Noun", "Verb", "NamedEntity"], suffixes: Union[List[Morpheme], List[str]]) -> str:
    """Generate a word form using Zemberek's WordGenerator.

    This replaces the previous custom BFS implementation and leverages the
    built‑in generator which correctly handles phonetic exceptions such as
    voicing, doubling and last‑vowel drop.
    """
    if not suffixes:
        return root

    # Convert suffix identifiers to Morpheme objects when necessary
    suffix_objs = [s if isinstance(s, Morpheme) else morpheme_map[s] for s in suffixes]

    # Determine candidate primary POS values for the root based on the suffixes
    pos_candidates = guess_primary_pos_given_suffixes(root, suffix_objs)

    morphotactics = get_morphotactics()
    generator = WordGenerator(morphotactics)
    lexicon = morphotactics.get_root_lexicon()

    for pos in pos_candidates:
        # Find dictionary items matching the root and the candidate POS
        matching_items = [item for item in lexicon.item_map.get(root, []) if item.primary_pos == pos]
        # Try each matching item with its stem transitions
        for item in matching_items:
            stem_transitions = morphotactics.stem_transitions.get_transitions_for_item(item)
            results = generator.generate(item=item, morphemes=tuple(suffix_objs), candidates=stem_transitions)
            if results:
                return results[0].surface
        # Fallback: generate using generic stem transitions for the raw root string
        generic_transitions = morphotactics.stem_transitions.get_transitions(root)
        results = generator.generate(morphemes=tuple(suffix_objs), candidates=generic_transitions)
        if results:
            return results[0].surface

    # If all attempts fail, return the original root as a safe fallback
    return root
