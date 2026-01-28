import sys
from pathlib import Path
import logging
sys.path.append(str(Path(__file__).parent.parent))

from morph_tokenizer import MorphTokenizer

def print_test(sentence: str, tokenizer: MorphTokenizer):
    tokens = tokenizer._MorphTokenizer__tokenize_sentence(sentence)
    print(f"Tokens: {tokens}")
    print()

logging.basicConfig(level=logging.ERROR)

def test_generation(sentence: str, tokenizer: MorphTokenizer, expected: Array):
    tokens = tokenizer._MorphTokenizer__tokenize_sentence(sentence)

    output=""
    if tokens != expected:
        output+="\033[31m"
        output+=f"Sentence: {sentence} ->\n Result: {tokens}\n Expected: {expected}\033[0m"
        print(output)

if __name__ == "__main__":
    tokenizer = MorphTokenizer("<|", "|>")
    test_generation("Ayşeyi, Ahmet'i Veli'yi ve ghim'i eve çağırdı.", tokenizer, ['A', 'y', 'ş', 'e', '<|Noun|>', '<|Acc|>', ',', ' ', 'A', 'h', 'm', 'e', 't', '<|NamedEntity|>', '<|Acc|>', ' ', 'V', 'e', 'l', 'i', '<|NamedEntity|>', '<|Acc|>', ' ', 'v', 'e', ' ', 'g', 'h', 'i', 'm', '<|NamedEntity|>', '<|Acc|>', ' ', 'e', 'v', '<|Noun|>', '<|Dat|>', ' ', 'ç', 'a', 'ğ', 'ı', 'r', '<|Verb|>', '<|Past|>', '.'])
    test_generation("kitapçı 2 kglik yani kg'lik TR'li eşya getirirmiş", tokenizer, ['k', 'i', 't', 'a', 'p', '<|Noun|>', '<|Agt|>', ' ', '2', ' ', 'k', 'g', '<|Noun|>', '<|Ness|>', ' ', 'y', 'a', 'n', 'i', ' ', 'k', 'g', '<|NamedEntity|>', '<|Ness|>', ' ', 'T', 'R', '<|NamedEntity|>', '<|With|>', ' ', 'e', 'ş', 'y', 'a', ' ', 'g', 'e', 't', 'i', 'r', '<|Verb|>', '<|Aor|>', '<|Narr|>'])
    test_generation("Burnu burnu havadadır onun.", tokenizer, ['B', 'u', 'r', 'u', 'n', '<|Noun|>', '<|P3sg|>', ' ', 'b', 'u', 'r', 'u', 'n', '<|Noun|>', '<|P3sg|>', ' ', 'h', 'a', 'v', 'a', '<|Noun|>', '<|Loc|>', '<|Cop|>', ' ', 'o', '<|Noun|>', '<|Gen|>', '.'])
    test_generation("Yerisimi'ye gelirmiş.", tokenizer, ['Y', 'e', 'r', 'i', 's', 'i', 'm', 'i', '<|NamedEntity|>', '<|Dat|>', ' ', 'g', 'e', 'l', '<|Verb|>', '<|Aor|>', '<|Narr|>', '.'])

    test_generation("AYŞE'Yİ ve ANNEM'i eVe çağırDI", tokenizer, ['A', 'Y', 'Ş', 'E', "'", 'Y', 'İ', ' ', 'v', 'e', ' ', 'A', 'N', 'N', 'E', 'M', '<|NamedEntity|>', '<|Acc|>', ' ', 'e', 'V', 'e', ' ', 'ç', 'a', 'ğ', 'ı', 'r', 'D', 'I'])
    test_generation("TDK'ye, UNKNOWN'a, TÜİK'e ve ALİ'ye göre olan hjKŞFh şeyler", tokenizer, ['T', 'D', 'K', "'", 'y', 'e', ',', ' ', 'U', 'N', 'K', 'N', 'O', 'W', 'N', '<|NamedEntity|>', '<|Dat|>', ',', ' ', 'T', 'Ü', 'İ', 'K', '<|NamedEntity|>', '<|Dat|>', ' ', 'v', 'e', ' ', 'A', 'L', 'İ', '<|NamedEntity|>', '<|Dat|>', ' ', 'g', 'ö', 'r', 'e', ' ', 'o', 'l', '<|Verb|>', '<|PresPart|>', ' ', 'h', 'j', 'K', 'Ş', 'F', 'h', ' ', 'ş', 'e', 'y', '<|Noun|>', '<|A3pl|>'])
    test_generation("Annem, BABAM ve   kardeşlerime\ngöre\tdoğru olandır. ", tokenizer, ['A', 'n', 'n', 'e', '<|Noun|>', '<|P1sg|>', ',', ' ', 'B', 'A', 'B', 'A', '<|Noun|>', '<|P1sg|>', ' ', 'v', 'e', ' ', ' ', ' ', 'k', 'a', 'r', 'd', 'e', 'ş', '<|Noun|>', '<|A3pl|>', '<|P1sg|>', '<|Dat|>', '\n', 'g', 'ö', 'r', 'e', '\t', 'd', 'o', 'ğ', 'r', 'u', ' ', 'o', 'l', '<|Verb|>', '<|PresPart|>', '<|Cop|>', '.', ' '])

    test_generation("Annem 11'de veya 12.00'da burada olur.", tokenizer, ['A', 'n', 'n', 'e', '<|Noun|>', '<|P1sg|>', ' ', '1', '1', '<|Noun|>', '<|Loc|>', ' ', 'v', 'e', 'y', 'a', ' ', '1', '2', '.', '0', '0', '<|Noun|>', '<|Loc|>', ' ', 'b', 'u', 'r', 'a', '<|Noun|>', '<|Loc|>', ' ', 'o', 'l', '<|Verb|>', '<|Aor|>', '.'])
    
    # unsupported 👇
    test_generation("Örnek2'nin 3/4'ü oldu.", tokenizer, ['Ö', 'r', 'n', 'e', 'k', '2', '\'', 'n', 'i', 'n', ' ', '3', '/', '4', '\'', 'ü', ' ', 'o', 'l', '<|Verb|>', '<|Past|>', '.'])
    print("All tests completed!")