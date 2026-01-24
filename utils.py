from zemberek import TurkishMorphology
from zemberek.core.turkish.turkish_alphabet import TurkishAlphabet
import logging

_morphotactics = None
_morphology = None

def get_morphotactics():
    global _morphotactics
    if _morphotactics is None:
        from zemberek.morphology.lexicon.root_lexicon import RootLexicon
        from zemberek.morphology.morphotactics.turkish_morphotactics import TurkishMorphotactics
        lexicon = RootLexicon.get_default()
        _morphotactics = TurkishMorphotactics(lexicon)
    return _morphotactics

def get_morphology():
    global _morphology
    if _morphology is None:
        _morphology = TurkishMorphology.create_with_defaults()
    return _morphology

def match_capitilization(ref: str, target: str) -> str:
    if not ref or not target:
        return target
    
    alphabet = TurkishAlphabet.INSTANCE
    
    if ref.isupper() and len(ref) > 1:
        return target.translate(alphabet.upper_map).upper()
        
    if ref[0].isupper():
        return target[0].translate(alphabet.upper_map).upper() + target[1:]

    return target[0].translate(alphabet.lower_map).lower() + target[1:]

def is_morph_analysis_ok(word: str) -> bool:
    parts = word[1:].split("'")
    trailing = parts[-1]
    if len(parts) > 2: return False
    if word.isupper(): return len(parts) == 1
    for c in trailing:
        if c.isupper(): return False
    return True