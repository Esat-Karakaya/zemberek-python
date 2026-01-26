from typing import List
from zemberek.morphology.analysis.sentence_analysis import SentenceAnalysis
from utils import get_morphology, match_capitilization, is_morph_analysis_ok

from zemberek.core.turkish import PrimaryPos, SecondaryPos

class MorphTokenizer:
    def __init__(self, tk_start, tk_end):
        self.morphology = get_morphology()
        self.tk_start = tk_start
        self.tk_end = tk_end
    
    def __tokenize_sentence(self, sentence: str) -> List[str]:
        analysis = self.morphology.analyze_sentence(sentence)
        after = self.morphology.disambiguate(sentence, analysis)

        whitespaces = self.__collect_whitespaces(sentence, after)

        words = []
        for sentence_word_analysis in after:
            best = sentence_word_analysis.best_analysis
            item = best.item
            original_surface = sentence_word_analysis.word_analysis.inp
            if not is_morph_analysis_ok(original_surface):
                words.append([original_surface]) # declare word as unknown
                continue
            
            # Determine word type
            word_type = None
            if item.primary_pos == PrimaryPos.Verb:
                word_type = "Verb"
            elif item.secondary_pos in [SecondaryPos.Abbreviation, SecondaryPos.ProperNoun]:
                word_type = "NamedEntity"
            elif item.primary_pos not in [PrimaryPos.Unknown, PrimaryPos.Punctuation]:
                word_type = "Noun"

            tokens = []
            suffixes = []
            for i, m_data in enumerate(best.morpheme_data_list):
                if i == 0:
                    stem = item.normalized_lemma() if not item.is_unknown() else m_data.surface
                    if "'" in original_surface and not item.is_unknown():
                        stem = original_surface.split("'")[0]
                    tokens.append(match_capitilization(original_surface, stem))
                elif len(m_data.surface) > 0:
                    suffixes.append(self.tk_start + m_data.morpheme.id_ + self.tk_end)
            
            if len(suffixes) > 0:
                if word_type:
                    tokens.append(self.tk_start + word_type + self.tk_end)
                tokens.extend(suffixes)
            words.append(tokens)
        sentence = []
        for i in range(len(words)+ len(whitespaces)-1):
            if i%2 == 1:
                sentence.append(words[i//2])
            elif len(whitespaces[i//2]) > 0:
                sentence.append([whitespaces[i//2]])
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