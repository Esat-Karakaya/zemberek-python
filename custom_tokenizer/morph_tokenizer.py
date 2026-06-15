import sys
from pathlib import Path
# Add the parent directory to sys.path to allow importing from the root
sys.path.append(str(Path(__file__).resolve().parent.parent))

from typing import List
from zemberek.morphology.analysis.word_analysis import WordAnalysis
from zemberek import TurkishSentenceExtractor
from utils import get_morphology, match_capitilization, is_morph_analysis_ok

from zemberek.core.turkish import PrimaryPos, SecondaryPos
from custom_tokenizer.detokenizer import MorphDetokenizer

class MorphTokenizer:
    def __init__(self, tk_start, tk_end):
        self.tk_start = tk_start
        self.tk_end = tk_end
        self.morphology = get_morphology()
        self.extractor = TurkishSentenceExtractor()
        self.special_token = lambda s: tk_start + s + tk_end

    def tokenize(self, text: str) -> List[str]:
        sentences = self.extractor.from_paragraph(text)
        
        all_tokens = []
        current_pos = 0
        
        for i, sentence_text in enumerate(sentences):
            # Find the sentence in the original text to capture preceding whitespace/newlines
            start_idx = text.find(sentence_text, current_pos)
            prefix = text[current_pos:start_idx]
            if prefix:
                all_tokens.extend(list(prefix))
            
            # Tokenize the sentence itself
            all_tokens.extend(self.__tokenize_sentence(sentence_text))
            
            current_pos = start_idx + len(sentence_text)
            
        # Add any trailing whitespace after the last sentence
        trailing = text[current_pos:]
        if trailing:
            all_tokens.extend(list(trailing))
            
        return all_tokens
    
    def detokenize(self, tokens: List[str]) -> str:
        detokenizer = MorphDetokenizer(tk_start=self.tk_start, tk_end=self.tk_end)
        return detokenizer.detokenize(tokens)
    
    def __tokenize_sentence(self, sentence: str) -> List[str]:
        after = self.morphology.analyze_sentence(sentence)

        whitespaces = self.__collect_whitespaces(sentence, after)

        words = []
        for word_analysis in after:
            tokens = self.__get_word_tokens(word_analysis)
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

    def __get_word_tokens(self, word_analysis: WordAnalysis) -> List[str]:
        original_surface = word_analysis.inp
        
        if not is_morph_analysis_ok(original_surface) or not word_analysis.analysis_results:
            return list(original_surface) # declare word as unknown
            
        best = word_analysis.analysis_results[0]
        item = best.item
            
        word_type = self.__get_word_type(item, original_surface)
        
        tokens = []
        suffixes = []
        for i, m_data in enumerate(best.morpheme_data_list):
            if i == 0:
                # Use the actual stem surface from morphological analysis instead of lemma
                stem = m_data.surface
                if "'" in original_surface and not item.is_unknown():
                    stem = original_surface.split("'")[0]
                tokens.extend(list(match_capitilization(original_surface, stem)))
            elif len(m_data.surface) > 0:
                suffixes.append(self.special_token(m_data.morpheme.id_))
        
        if len(suffixes) > 0:
            if word_type:
                tokens.append(self.special_token(word_type))
            tokens.extend(suffixes)
        else:
            return list(original_surface)
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
    
    def __collect_whitespaces(self, sentence: str, analyses: List[WordAnalysis]) -> List[str]:
        whitespaces = []
        current_pos = 0
        
        for wa in analyses:
            original_surface = wa.inp
            # Find the start of this word in the original sentence
            start_idx = sentence.find(original_surface, current_pos)
            
            # The gap before this word
            whitespaces.append(sentence[current_pos:start_idx])
            
            # Move current_pos past the word
            current_pos = start_idx + len(original_surface)
            
        # Add the trailing characters (if any)
        whitespaces.append(sentence[current_pos:])
        
        return whitespaces