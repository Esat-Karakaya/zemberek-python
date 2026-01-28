from typing import List
from zemberek.morphology.analysis.sentence_analysis import SentenceAnalysis
from utils import get_morphology, match_capitilization, is_morph_analysis_ok

from zemberek.core.turkish import PrimaryPos, SecondaryPos

class MorphTokenizer:
    def __init__(self, tk_start, tk_end):
        self.morphology = get_morphology()
        self.special_token = lambda s: tk_start + s + tk_end
    
    def __tokenize_sentence(self, sentence: str) -> List[str]:
        analysis = self.morphology.analyze_sentence(sentence)
        after = self.morphology.disambiguate(sentence, analysis)

        whitespaces = self.__collect_whitespaces(sentence, after)

        words = []
        for sentence_word_analysis in after:
            tokens = self.__get_word_tokens(sentence_word_analysis)
            words.append(tokens)
            
        split_by_words = self.__reconstruct_sentence(words, whitespaces)
        return [token for word in split_by_words for token in word]

    def __get_word_type(self, item, original_surface: str) -> str:
        if item.primary_pos == PrimaryPos.Verb:
            return "Verb"

        # Check for numeric words recognized by Zemberek
        numeric_secondary_pos = {
            SecondaryPos.Cardinal, SecondaryPos.Clock, SecondaryPos.Date,
            SecondaryPos.Ordinal, SecondaryPos.Percentage, SecondaryPos.Ratio,
            SecondaryPos.Real, SecondaryPos.Distribution, SecondaryPos.Range
        }
        if item.secondary_pos in numeric_secondary_pos:
            return "Noun"

        # NamedEntity is anything with an apostrophe (that isn't a verb or numeric)
        if "'" in original_surface:
            return "NamedEntity"
            
        if item.primary_pos not in [PrimaryPos.Unknown, PrimaryPos.Punctuation]:
            return "Noun"
        return None

    def __get_word_tokens(self, sentence_word_analysis) -> List[str]:
        best = sentence_word_analysis.best_analysis
        item = best.item
        original_surface = sentence_word_analysis.word_analysis.inp
        
        if not is_morph_analysis_ok(original_surface):
            return list(original_surface) # declare word as unknown
            
        word_type = self.__get_word_type(item, original_surface)
        
        tokens = []
        suffixes = []
        for i, m_data in enumerate(best.morpheme_data_list):
            if i == 0:
                stem = item.normalized_lemma() if not item.is_unknown() else m_data.surface
                if "'" in original_surface and not item.is_unknown():
                    stem = original_surface.split("'")[0]
                tokens.extend(list(match_capitilization(original_surface, stem)))
            elif len(m_data.surface) > 0:
                suffixes.append(self.special_token(m_data.morpheme.id_))
        
        if len(suffixes) > 0:
            if word_type:
                tokens.append(self.special_token(word_type))
            tokens.extend(suffixes)
        return tokens

    def __reconstruct_sentence(self, words: List[List[str]], whitespaces: List[str]) -> List[List[str]]:
        sentence = []
        for i in range(len(words) + len(whitespaces)):
            if i % 2 == 1:
                if i // 2 < len(words):
                    sentence.append(words[i // 2])
            else:
                if i // 2 < len(whitespaces) and len(whitespaces[i // 2]) > 0:
                    sentence.append(list(whitespaces[i // 2]))
        return sentence
    
    def __collect_whitespaces(self, sentence: str, disambiguated_analysis: SentenceAnalysis) -> List[str]:
        whitespaces = []
        current_pos = 0
        
        for swa in disambiguated_analysis:
            original_surface = swa.word_analysis.inp
            # Find the start of this word in the original sentence
            start_idx = sentence.find(original_surface, current_pos)
            
            # The gap before this word
            whitespaces.append(sentence[current_pos:start_idx])
            
            # Move current_pos past the word
            current_pos = start_idx + len(original_surface)
            
        # Add the trailing characters (if any)
        whitespaces.append(sentence[current_pos:])
        
        return whitespaces