import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from morph_tokenizer import MorphTokenizer

def print_test(sentence: str, tokenizer: MorphTokenizer):
    tokens = tokenizer._MorphTokenizer__tokenize_sentence(sentence)
    print(f"Tokens: {tokens}")
    print()

if __name__ == "__main__":
    tokenizer = MorphTokenizer("<|", "|>")
    print_test("Ayşe'yi, Veli'yi ve ghim'i eve çağırdı.", tokenizer)
    print_test("kitapçı eve gelirmiş.", tokenizer)
    print_test("Burnu burnu havadadır onun.", tokenizer)
    print_test("Yerisimi'ye gelirmiş.", tokenizer)

    print_test("AYŞE'Yİ ve ANNEM'i eVe çağırDI", tokenizer)
    print_test("TDK'ye, UNKNOWN'a, TÜİK'e ve ALİ'ye göre olan hjKŞFh şeyler", tokenizer)
    print_test("Annem, BABAM ve   kardeşlerime\ngöre\tdoğru olandır. ", tokenizer)

    print_test("Annem 11'de veya 12.00'da burada olur.", tokenizer)
    print_test("Örnek2'nin 3/4'ü oldu.", tokenizer) # unsupported
    print_test("Annem geldi", tokenizer) # unsupported