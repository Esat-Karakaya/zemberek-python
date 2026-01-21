from typing import List
from zemberek import (
    TurkishSpellChecker,
    TurkishSentenceNormalizer,
    TurkishSentenceExtractor,
    TurkishMorphology,
    TurkishTokenizer
)
from utils import get_morphology, match_capitilization

class MorphTokenizer:
    def __init__(self, tk_start, tk_end):
        self.morphology = get_morphology()
        self.tk_start = tk_start
        self.tk_end = tk_end
    
    def __tokenize_sentence(self, sentence: str) -> List[str]:
        analysis = self.morphology.analyze_sentence(sentence)
        after = self.morphology.disambiguate(sentence, analysis)

        tokens = []
        for sentence_word_analysis in after:
            best = sentence_word_analysis.best_analysis
            item = best.item
            original_surface = sentence_word_analysis.word_analysis.inp
            for i, m_data in enumerate(best.morpheme_data_list):
                if i == 0:
                    stem = item.normalized_lemma() if not item.is_unknown() else m_data.surface
                    if "'" in stem:
                        stem = stem.split("'")[0]
                    tokens.append(match_capitilization(original_surface, stem))
                elif len(m_data.surface) > 0:
                    tokens.append(self.tk_start + m_data.morpheme.id_ + self.tk_end)
        return tokens