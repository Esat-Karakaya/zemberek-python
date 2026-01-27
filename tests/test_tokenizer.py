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
        output+=f"Root: {root} ({pos}), Suffixes: {suffix_ids} -> Result: {tokens}, Expected: {expected}\033[0m"
        print(output)

if __name__ == "__main__":
    tokenizer = MorphTokenizer("<|", "|>")
    test_generation("Ayşeyi, Ahmet'i Veli'yi ve ghim'i eve çağırdı.", tokenizer, [['Ayşe', '<|Noun|>', '<|Acc|>'], [','], [' '], ['Ahmet', '<|NamedEntity|>', '<|Acc|>'], [' '], ['Veli', '<|NamedEntity|>', '<|Acc|>'], [' '], ['ve'], [' '], ['ghim', '<|NamedEntity|>', '<|Acc|>'], [' '], ['ev', '<|Noun|>', '<|Dat|>'], [' '], ['çağır', '<|Verb|>', '<|Past|>'], ['.']])
    test_generation("kitapçı 2 kglik yani kg'lik TR'li eşya getirirmiş", tokenizer, [['kitap', '<|Noun|>', '<|Agt|>'], [' '], ['2'], [' '], ['kg', '<|Noun|>', '<|Ness|>'], [' '], ['yani'], [' '], ['kg', '<|NamedEntity|>', '<|Ness|>'], [' '], ['TR', '<|NamedEntity|>', '<|With|>'], [' '], ['eşya'], [' '], ['getir', '<|Verb|>', '<|Aor|>', '<|Narr|>']])
    test_generation("Burnu burnu havadadır onun.", tokenizer, [['Burun', '<|Noun|>', '<|P3sg|>'], [' '], ['burun', '<|Noun|>', '<|P3sg|>'], [' '], ['hava', '<|Noun|>', '<|Loc|>', '<|Cop|>'], [' '], ['o', '<|Noun|>', '<|Gen|>'], ['.']])
    test_generation("Yerisimi'ye gelirmiş.", tokenizer, [['Yerisimi', '<|NamedEntity|>', '<|Dat|>'], [' '], ['gel', '<|Verb|>', '<|Aor|>', '<|Narr|>'], ['.']])

    test_generation("AYŞE'Yİ ve ANNEM'i eVe çağırDI", tokenizer, [["AYŞE'Yİ"], [' '], ['ve'], [' '], ['ANNEM', '<|NamedEntity|>', '<|Acc|>'], [' '], ['eVe'], [' '], ['çağırDI']])
    test_generation("TDK'ye, UNKNOWN'a, TÜİK'e ve ALİ'ye göre olan hjKŞFh şeyler", tokenizer, [["TDK'ye"], [','], [' '], ['UNKNOWN', '<|NamedEntity|>', '<|Dat|>'], [','], [' '], ['TÜİK', '<|NamedEntity|>', '<|Dat|>'], [' '], ['ve'], [' '], ['ALİ', '<|NamedEntity|>', '<|Dat|>'], [' '], ['göre'], [' '], ['ol', '<|Verb|>', '<|PresPart|>'], [' '], ['hjKŞFh'], [' '], ['şey', '<|Noun|>', '<|A3pl|>']])
    test_generation("Annem, BABAM ve   kardeşlerime\ngöre\tdoğru olandır. ", tokenizer, [['Anne', '<|Noun|>', '<|P1sg|>'], [','], [' '], ['BABA', '<|Noun|>', '<|P1sg|>'], [' '], ['ve'], ['   '], ['kardeş', '<|Noun|>', '<|A3pl|>', '<|P1sg|>', '<|Dat|>'], ['\n'], ['göre'], ['\t'], ['doğru'], [' '], ['ol', '<|Verb|>', '<|PresPart|>', '<|Cop|>'], ['.']])

    test_generation("Annem 11'de veya 12.00'da burada olur.", tokenizer, [['Anne', '<|Noun|>', '<|P1sg|>'], [' '], ['11', '<|Noun|>', '<|Loc|>'], [' '], ['veya'], [' '], ['12.00', '<|Noun|>', '<|Loc|>'], [' '], ['bura', '<|Noun|>', '<|Loc|>'], [' '], ['ol', '<|Verb|>', '<|Aor|>'], ['.']])
    
    # unsupported 👇
    test_generation("Örnek2'nin 3/4'ü oldu.", tokenizer, [["Örnek2'nin"], [' '], ["3/4'ü"], [' '], ['ol', '<|Verb|>', '<|Past|>'], ['.']])
    print("All tests completed!")