from typing import List
from zemberek.core.turkish.primary_pos import PrimaryPos
from zemberek.morphology.morphotactics.morpheme import Morpheme
from zemberek.morphology.morphotactics.turkish_morphotactics import get_morpheme_map

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
# Initialize morphotactics to populate the morpheme map
get_morphotactics()
m_map = get_morpheme_map()

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
    
    # 1. Determine Candidate Primary POSs
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

def generate_word(root: str, suffixes: List[Morpheme]) -> str:
    """
    Args:
        root (str): The root word string (e.g., "elma", "gel").
        suffixes (List[Morpheme]): A list of suffix Morpheme objects to attach.
        
    Returns:
        str: The generated surface form (e.g., "elmalara"). 
            Returns the best effort generation (or just the root) if strictly valid generation fails.
    """
    from zemberek.morphology.analysis.attributes_helper import AttributesHelper
    from zemberek.morphology.analysis.surface_transitions import SurfaceTransition
    from zemberek.morphology.morphotactics.morpheme import Morpheme

    if not suffixes:
        return root

    morphotactics = get_morphotactics()

    # 1. Guess Primary POS from suffixes
    final_candidates = guess_primary_pos_given_suffixes(root, suffixes)

    # 2. Try Generation for each Candidate
    best_result = root
    
    for pos in final_candidates:
        # Map primary pos to start state
        current_state = None
        if pos == PrimaryPos.Noun:
            current_state = morphotactics.noun_S
        elif pos == PrimaryPos.Verb:
            current_state = morphotactics.verbRoot_S
        elif pos == PrimaryPos.Adjective:
            current_state = morphotactics.adjectiveRoot_ST
        elif pos == PrimaryPos.Numeral:
            current_state = morphotactics.numeralRoot_ST
        elif pos == PrimaryPos.Pronoun:
            current_state = morphotactics.pronPers_S
        # Add other POS mappings as needed
        
        if current_state is None:
            continue
            
        surface = root
        attributes = AttributesHelper.get_morphemic_attributes(surface)
        
        current_suffixes_to_process = list(suffixes)
        success = True
        
        while current_suffixes_to_process:
            target_suffix = current_suffixes_to_process[0]
            
            # Search for path to target suffix (BFS)
            # Queue stores: (state, attributes, path_surface)
            # But wait, attributes depend on surface generated so far in the path.
            # We just need to find the NEXT STATE that corresponds to target_suffix.
            # Intervening states must be EMPTY transitions.
            
            queue = [(current_state, "")]
            visited = {current_state}
            path_found = None # (transition_to_target, accumulated_surface)
            
            # Limited depth BFS to find target suffix via empty transitions
            import collections
            bfs_q = collections.deque([(current_state, [])]) # state, list of transitions
            visited_states = {current_state}
            
            found_transition_path = None
            
            # We iterate to find a path of transitions: Empty -> Empty -> ... -> TargetSuffix
            while bfs_q:
                s, path = bfs_q.popleft()
                
                # Check if this state's outgoing transitions lead to target
                # But "s" is where we are coming FROM. 
                # We need to find a transition T from S such that T leads to target morpheme.
                
                # Direct check first
                match = None
                for t in s.outgoing:
                    if t.to.morpheme.id_ == target_suffix.id_:
                         match = t
                         break
                
                if match:
                    found_transition_path = path + [match]
                    break
                
                # If not direct, look for empty transitions to traverse
                # Limit depth to avoid infinite loops or deep searches (arbitrary limit 5)
                if len(path) < 5:
                    for t in s.outgoing:
                        # Empty transition check: template is empty/None
                        # SuffixTransition usually has surface_template. If it is empty or None, it produces no surface.
                        # MorphemeState.add_empty uses SuffixTransition but without template (defaults to "")
                        is_empty_transition = False
                        if hasattr(t, 'surface_template') and not t.surface_template:
                            is_empty_transition = True
                        
                        if is_empty_transition and t.to not in visited_states:
                            visited_states.add(t.to)
                            bfs_q.append((t.to, path + [t]))

            if found_transition_path:
                # Apply the path
                # Note: The path might contain multiple empty transitions and finally the target transition.
                # We need to generate surface and update attributes for EACH step in the path actually, 
                # because even empty transitions move state. 
                # BUT `generate_surface` on empty transition adds nothing.
                
                for trans in found_transition_path:
                    suffix_surface = SurfaceTransition.generate_surface(trans, attributes)
                    surface += suffix_surface
                    attributes = AttributesHelper.get_morphemic_attributes(surface)
                    current_state = trans.to
                
                # We successfully processed this suffix
                current_suffixes_to_process.pop(0)
            else:
                success = False
                break
        
        if success:
            return surface
        else:
            pass

    return best_result
