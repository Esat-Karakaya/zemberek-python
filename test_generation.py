from utils import generate_word, get_morphotactics
from zemberek.core.turkish.primary_pos import PrimaryPos
from zemberek.morphology.morphotactics.turkish_morphotactics import get_morpheme_map
import logging

# Configure logging to show errors but avoid noise
logging.basicConfig(level=logging.ERROR)

def test_generation(root, pos, suffix_ids, expected):
    result = generate_word(root, pos, suffix_ids)
    print(f"Root: {root} ({pos}), Suffixes: {suffix_ids} -> Result: {result}, Expected: {expected}")
    assert result == expected

if __name__ == "__main__":
    print("Starting generation tests...")
    
    # Noun Cases (Dictionary Match)
    test_generation("elma", "Noun", ["A3pl", "Dat"], "elmalara")
    test_generation("limon", "Noun", ["A3sg", "P1pl"], "limonumuz")
    test_generation("hak", "Noun", ["Dat"], "hakka")
    test_generation("burun", "Noun", ["Gen"], "burnun")
    
    # Verb Cases (Dictionary Match)
    test_generation("gel", "Verb", ["Prog1", "A1sg"], "geliyorum")
    test_generation("gel", "Verb", ["Past", "A1sg"], "geldim")
    
    # POS Inference
    test_generation("at", "Noun", ["Dat"], "ata") 
    test_generation("at", "Verb", ["Fut", "Narr", "A1sg"], "atacakmışım")

    # Aggressive POS Inference
    test_generation("elma", "Verb", ["Fut", "Narr", "A1sg"], "elmayacakmışım")
    test_generation("gel", "Noun", ["P1pl", "Gen"], "gelimizin")

    # Pronoun
    test_generation("biz", "Noun", ["A3pl"], "bizler")

    # Named Entity (Proper Noun)
    test_generation("Çıtçıt", "NamedEntity", ["Dat"], "Çıtçıt'a")
    test_generation("Bürokratistan", "NamedEntity", ["Loc", "Rel", "A3pl", "Gen"], "Bürokratistan'dakilerin")
    test_generation("Ahmet", "NamedEntity", ["Dat"], "Ahmet'e")

    # Unknown Root
    test_generation("bloop", "Noun", ["Dat"], "bloopa")
    test_generation("bloop", "Verb", ["Prog1"], "bloopuyor")

    # Broken Generation
    test_generation("kap", "Noun", ["Prog1", "Dim", "A3pl"], "kapıyorcuklar")

    print("\nAll tests passed!")
