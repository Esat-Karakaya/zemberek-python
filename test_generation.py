from utils import generate_word, get_morphotactics
from zemberek.core.turkish.primary_pos import PrimaryPos
from zemberek.morphology.morphotactics.turkish_morphotactics import get_morpheme_map
import logging

# Configure logging to show errors but avoid noise
logging.basicConfig(level=logging.ERROR)

def test_generation(root, suffix_ids, expected):
    result = generate_word(root, suffix_ids)
    print(f"Root: {root}, Suffixes: {suffix_ids} -> Result: {result}, Expected: {expected}")
    assert result == expected

if __name__ == "__main__":
    print("Starting generation tests with auto-POS inference (Morpheme objects)...")
    
    # Noun Cases (Dictionary Match)
    test_generation("elma", ["A3pl", "Dat"], "elmalara")
    test_generation("limon", ["A3sg", "P1pl"], "limonumuz")
    test_generation("hak", ["Dat"], "hakka")
    test_generation("burun", ["Gen"], "burnun")
    
    # Verb Cases (Dictionary Match)
    test_generation("gel", ["Prog1", "A1sg"], "geliyorum")
    test_generation("gel", ["Past", "A1sg"], "geldim")
    
    # Ambiguous / Suffix Inference
    test_generation("at", ["Dat"], "ata") 
    test_generation("at", ["Fut", "Narr", "A1sg"], "atacakmışım")

    # Agressive Suffix Inference
    """ 
    test_generation("elma", ["Fut", "Narr", "A1sg"], "elmayacakmışım")
    test_generation("gel", ["P1pl", "Gen"], "gelimizin")
    """
    
    # Pronoun
    test_generation("biz", ["A3pl"], "bizler")

    # Unknown Named Entity
    test_generation("Çıtçıt", ["Dat"], "Çıtçıt'a")
    test_generation("Bürokratistan", ["Loc", "Rel", "A3pl", "Gen"], "Bürokratistan'dakilerin")

    # Unknown Root (Inference from suffix)
    test_generation("bloop", ["Dat"], "bloopa")
    test_generation("bloop", ["Prog1"], "bloopuyor")

    print("\nAll tests passed!")
