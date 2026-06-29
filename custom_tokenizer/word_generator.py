from custom_tokenizer.utils import get_morphotactics, match_capitilization
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
from custom_tokenizer.dictionary import morpheme_map
from zemberek.morphology.analysis.tr.pronunciation_guesser import PronunciationGuesser
import logging
from typing import List, Union, Literal, Set

class CustomWordGenerator:
    def __init__(self):
        self.guesser = PronunciationGuesser()
        self.alphabet = TurkishAlphabet.INSTANCE
        self.morphotactics = get_morphotactics()

    def generate_word(self, root: str, word_type: Literal["Noun", "Verb", "NamedEntity"], suffixes: Union[List[Morpheme], List[str]]) -> str:
        """Generate a word form using Zemberek's WordGenerator.
        
        Handles dictionary items, unknown words, and NamedEntity special logic.
        """
        if not suffixes:
            return root

        suffix_objs = [s if isinstance(s, Morpheme) else morpheme_map[s] for s in suffixes]
        p_pos, s_pos = self._get_pos_enums(word_type)
        
        lexicon = self.morphotactics.get_root_lexicon()
        matching_items = self._find_lexicon_items(root, word_type, p_pos, lexicon)
        candidates = self._get_stem_candidates(root, matching_items, word_type, p_pos, s_pos)

        generator = WordGenerator(self.morphotactics)
        results = generator.generate(morphemes=tuple(suffix_objs), candidates=tuple(candidates))
        
        if results:
            return self._apply_post_processing(root, results[0].surface, word_type)

        forced_result = self.force_suffixes_on_word(root, word_type == "NamedEntity", suffix_objs)
        return match_capitilization(root, forced_result)

    def _get_pos_enums(self, word_type: str) -> tuple[PrimaryPos, SecondaryPos]:
        if word_type in ["Noun", "NamedEntity"]:
            p_pos = PrimaryPos.Noun
        elif word_type == "Adj":
            p_pos = PrimaryPos.Adjective
        else:  # Verb and others
            p_pos = PrimaryPos.Verb
        
        s_pos = SecondaryPos.ProperNoun if word_type == "NamedEntity" else SecondaryPos.None_
        return p_pos, s_pos

    def _filter_lexicon_items(self, items: List[DictionaryItem], word_type: str, p_pos: PrimaryPos = None) -> List[DictionaryItem]:
        if p_pos is not None:
            items = [item for item in items if item.primary_pos == p_pos]
        else:
            items = [item for item in items if item.primary_pos != PrimaryPos.Verb]

        if word_type == "Noun":
            items = [item for item in items if item.secondary_pos != SecondaryPos.ProperNoun]
        elif word_type == "NamedEntity":
            proper_items = [item for item in items if item.secondary_pos == SecondaryPos.ProperNoun]
            if proper_items:
                items = proper_items

        return items

    def _find_lexicon_items(self, root: str, word_type: str, p_pos: PrimaryPos, lexicon) -> List[DictionaryItem]:
        lex_key = root
        if word_type == "Verb":
            lex_key = self._add_Inf1_suffix(root)
        
        items = self._filter_lexicon_items(lexicon.item_map.get(lex_key, []), word_type, p_pos)
        
        if not items and (root.istitle() or root.isupper()):
            alt_lex_key = root.translate(self.alphabet.lower_map).lower()
            if word_type == "Verb":
                alt_lex_key = self._add_Inf1_suffix(alt_lex_key)
            items = self._filter_lexicon_items(lexicon.item_map.get(alt_lex_key, []), word_type, p_pos)

        # If still no items found, try any available POS as a fallback
        # (but exclude Verb to avoid inappropriate morphological rules)
        if not items:
            items = self._filter_lexicon_items(lexicon.item_map.get(lex_key, []), word_type)
            if not items and (root.istitle() or root.isupper()):
                alt_lex_key = root.translate(self.alphabet.lower_map).lower()
                if word_type == "Verb":
                    alt_lex_key = self._add_Inf1_suffix(alt_lex_key)
                items = self._filter_lexicon_items(lexicon.item_map.get(alt_lex_key, []), word_type)

        return items

    def _get_stem_candidates(self, root: str, items: List[DictionaryItem], word_type: str, p_pos: PrimaryPos, s_pos: SecondaryPos) -> List[StemTransition]:
        candidates = []
        has_vowel = any(self.alphabet.is_vowel(c) for c in root)
        for item in items:
            if word_type == "NamedEntity" and not has_vowel:
                # For vowel-less NamedEntities (abbreviations), ensure they have phonetic attributes
                # even if using a dictionary item, as some dictionary entries might be missing them.
                start_state = self.morphotactics.noun_S
                phonetic_attrs = self._get_phonetic_attributes(root)
                candidates.append(StemTransition(root, item, phonetic_attrs, start_state))
            else:
                candidates.extend(self.morphotactics.stem_transitions.get_transitions_for_item(item))

        if not candidates:
            candidates.append(self._create_stem_transition(root, p_pos, s_pos))
        return candidates

    def _turkish_lower(self, s: str) -> str:
        return s.translate(self.alphabet.lower_map).lower()

    def _apply_post_processing(self, root: str, generated_surface: str, word_type: str) -> str:
        is_named_entity = word_type == "NamedEntity"
        is_number = self.alphabet.contains_digit(root)
        root_lower = self._turkish_lower(root)
        generated_lower = self._turkish_lower(generated_surface)
        
        if (is_named_entity or is_number) and generated_lower != root_lower:
            if generated_lower.startswith(root_lower):
                suffix = generated_lower[len(root_lower):]
                return root + "'" + suffix
        
        return match_capitilization(root, generated_surface)

    def force_suffixes_on_word(self, root: str, is_named_entity: bool, suffixes: List[Morpheme]) -> str:
        logging.warning(
            f"Couldn't add suffixes: {[s.id_ for s in suffixes]} to \"{root}\" "
            f"via zemberek's own method. Deploying work around"
        )
        
        generator = WordGenerator(self.morphotactics)
        current_surface = root
        apostrophe_added = False
        
        for suffix in suffixes:
            if suffix.id_ == "Rel":
                current_surface += "ki"
                continue

            generated_surface = self._try_force_generate_suffix(
                current_surface, suffix, is_named_entity, apostrophe_added, generator
            )
            
            if generated_surface:
                current_surface, apostrophe_added = self._update_forced_surface(
                    current_surface, generated_surface, is_named_entity, apostrophe_added
                )
            else:
                logging.error(f"Could not generate suffix {suffix.id_} for {current_surface}")
                
        return current_surface

    def _try_force_generate_suffix(self, current_surface: str, suffix: Morpheme, is_named_entity: bool, apostrophe_added: bool, generator: WordGenerator) -> Union[str, None]:
        possible_pos = self._get_primary_pos_for_suffix(suffix)
        for p_pos in possible_pos:
            s_pos = SecondaryPos.ProperNoun if is_named_entity and not apostrophe_added else SecondaryPos.None_
            candidate = self._create_stem_transition(current_surface, p_pos, s_pos)
            results = generator.generate(morphemes=(suffix,), candidates=(candidate,))
            if results:
                return results[0].surface
        return None

    def _update_forced_surface(self, current_surface: str, generated_surface: str, is_named_entity: bool, apostrophe_added: bool) -> tuple[str, bool]:
        if is_named_entity and not apostrophe_added and generated_surface != current_surface:
            current_lower = self._turkish_lower(current_surface)
            generated_lower = self._turkish_lower(generated_surface)
            if generated_lower.startswith(current_lower):
                suffix_surface = generated_lower[len(current_lower):]
                return f"{current_surface}'{suffix_surface}", True
            else:
                return generated_surface, False
        return generated_surface, apostrophe_added
    
    def _get_primary_pos_for_suffix(self, morpheme: Morpheme) -> List[PrimaryPos]:
        m_id = morpheme.id_
        
        noun_suffixes = {
            "Pnon", "P1sg", "P2sg", "P3sg", "P1pl", "P2pl", "P3pl", "Nom", "Dat", "Acc", "Abl", "Loc", "Ins", "Gen", "Equ",
            "Dim", "Ness", "With", "Without", "Related", "JustLike", "Rel", "Agt", "Become", "Acquire", "Zero", "Root",
            "A1sg", "A2sg", "A3sg", "A1pl", "A2pl", "A3pl", "Past", "Narr", "Cond", "Cop", "Noun"
        }
        
        adjective_suffixes = {
            "Ly", "AsIf", "Agt", "JustLike", "Become", "Acquire"
        }
        
        verb_suffixes = {
            "Caus", "Recip", "Reflex", "Able", "Pass", "Neg", "Unable", "Pres", "Prog1", "Prog2", "Aor", "Fut", "Imp", "Req",
            "Opt", "Desr", "Neces", "Inf1", "Inf2", "Inf3", "ActOf", "PastPart", "NarrPart", "FutPart", "PresPart", "AorPart",
            "NotState", "FeelLike", "EverSince", "Repeat", "Almost", "Hastily", "Stay", "Start", "AsIf", "While",
            "When", "SinceDoingSo", "AsLongAs", "ByDoingSo", "Adamantly", "AfterDoingSo", "WithoutHavingDoneSo",
            "WithoutBeingAbleToHaveDoneSo", "A1sg", "A2sg", "A3sg", "A1pl", "A2pl", "A3pl", "Past", "Narr", "Cond", "Cop", "Verb",
            "Intrj"
        }

        results = []
        if m_id in noun_suffixes: results.append(PrimaryPos.Noun)
        if m_id in adjective_suffixes: results.append(PrimaryPos.Adjective)
        if m_id in verb_suffixes: results.append(PrimaryPos.Verb)
        
        if results: return results

        return [PrimaryPos.Unknown]

    def _is_single_syllable(self, word: str) -> bool:
        from zemberek.core.turkish.turkish_alphabet import TurkishAlphabet
        vowel_count = sum(1 for char in word if TurkishAlphabet.INSTANCE.is_vowel(char))
        return vowel_count == 1

    def _add_Inf1_suffix(self, verb: str) -> str:
        alphabet =TurkishAlphabet()
        is_frontal = alphabet.get_last_vowel(verb).is_frontal()
        sfx = "mek" if is_frontal else "mak"
        return verb+sfx

    def _create_stem_transition(self, root: str, p_pos: PrimaryPos, s_pos: SecondaryPos = SecondaryPos.None_) -> StemTransition:
        attributes = set()
        if p_pos == PrimaryPos.Verb:
            if self._is_single_syllable(root):
                attributes.add(RootAttribute.Aorist_A)
            else:
                attributes.add(RootAttribute.Aorist_I)
        
        dummy_item = DictionaryItem(root, root, p_pos, s_pos, attributes=attributes)
        
        # Determine the appropriate start state based on PrimaryPos
        if p_pos == PrimaryPos.Verb:
            start_state = self._get_verb_root_state(root)
        elif p_pos == PrimaryPos.Adjective:
            start_state = self.morphotactics.adjectiveRoot_ST
        else:  # Noun and others
            start_state = self.morphotactics.noun_S
        
        phonetic_attrs = self._get_phonetic_attributes(root)
        res = StemTransition(root, dummy_item, phonetic_attrs, start_state)
        return res

    def _get_verb_root_state(self, root: str):
        root_lower = root.translate(self.alphabet.lower_map).lower()
        if root_lower in {"di", "yi", "de", "ye"}:
            return self.morphotactics.vDeYeRoot_S
        # Unknown verb roots should use the general verb root state.
        # Vowel-ending stems without dictionary evidence should not be assumed
        # to be vowel-drop verbs, otherwise suffixes like Fut fail.
        return self.morphotactics.verbRoot_S

    def _get_phonetic_attributes(self, root: str) -> Set[PhoneticAttribute]:
        has_vowel = any(self.alphabet.is_vowel(c) for c in root)
        
        if not has_vowel and len(root) > 0:
            # Letter names are usually defined for lowercase letters in the guesser
            normalized_root = root.translate(self.alphabet.lower_map).lower()
            pronunciation = self.guesser.to_turkish_letter_pronunciations(normalized_root)
            if pronunciation:
                return AttributesHelper.get_morphemic_attributes(pronunciation)
        
        if self.alphabet.contains_digit(root):
            pronunciation = self.guesser.to_turkish_letter_pronunciation_with_digit(root)
            return AttributesHelper.get_morphemic_attributes(pronunciation)
            
        return AttributesHelper.get_morphemic_attributes(root)