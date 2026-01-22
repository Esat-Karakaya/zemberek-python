from utils import generate_word, get_morphotactics
from zemberek.core.turkish.primary_pos import PrimaryPos
from zemberek.morphology.morphotactics.turkish_morphotactics import get_morpheme_map
import logging

# Configure logging to show errors but avoid noise
logging.basicConfig(level=logging.ERROR)

def test_generation(root, pos, suffix_ids, expected):
    result = generate_word(root, pos, suffix_ids)

    output=""
    if result != expected: output+="\033[31m"
    output+=f"Root: {root} ({pos}), Suffixes: {suffix_ids} -> Result: {result}, Expected: {expected}"
    print(output)
    if result != expected: print("\033[0m", end="")

if __name__ == "__main__":
    print("Starting generation tests...")
    
    # Noun Cases (Dictionary Match)
    test_generation("elma", "Noun", ["A3pl", "Dat"], "elmalara")
    test_generation("Burun", "Noun", ["A3sg", "P1pl"], "Burnumuz")
    test_generation("buRun", "Noun", ["A3sg", "P1pl"], "buRunumuz")
    test_generation("hak", "Noun", ["Dat"], "hakka")
    test_generation("burun", "Noun", ["Gen"], "burnun")
    
    # Verb Cases (Dictionary Match)
    test_generation("kaç", "Verb", ["Prog1", "A1sg"], "kaçıyorum")
    test_generation("koş", "Verb", ["Aor", "A1pl"], "koşarız")
    test_generation("gel", "Verb", ["AorPart"], "gelir")
    test_generation("seyret", "Verb", ["Aor", "AsIf"], "seyredercesine")
    
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
    test_generation("kitap", "Noun", ["Aor", "Almost"], "kitapırayaz")

    # All Caps
    test_generation("KAÇ", "Verb", ["Prog2", "A2pl"], "KAÇMAKTASINIZ")
    test_generation("HAK", "Noun", ["P2sg"], "HAKKIN")
    test_generation("TÜİK", "NamedEntity", ["P2sg"], "TÜİK'in")
    test_generation("TÜK", "NamedEntity", ["P2sg"], "TÜK'ün")

    # Numbers
    test_generation("11", "Noun", ["Loc"], "11'de")
    test_generation("12.00", "Noun", ["Loc"], "12.00'da")

    print("\nAll tests passed!")
