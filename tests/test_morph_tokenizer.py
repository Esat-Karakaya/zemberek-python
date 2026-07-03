import sys
from pathlib import Path
import logging
from typing import List
sys.path.append(str(Path(__file__).parent.parent))
import time

from pre_bpe_morph_tr.morph_tokenizer import MorphTokenizer

logging.basicConfig(level=logging.ERROR)

def test_generation(string: str, tokenizer: MorphTokenizer, expected: List[str]):
    t0 = time.time()
    tokens = tokenizer.tokenize(string)
    t1 = time.time()

    output="COMPLETED IN " + str(t1-t0) + " SECONDS\n"
    if tokens != expected:
        output+="\033[31m"
        output+=f"String: {string} ->\n Result: {tokens}\n Expected: {expected}\033[0m\n"
    
    # Test detokenization
    detokenized = tokenizer.detokenize(tokens)
    if detokenized != string:
        output+="\033[31m"
        output+=f"Detokenization failed!\nOriginal: {repr(string)}\nDetokenized: {repr(detokenized)}\033[0m\n"
    else:
        output+="\033[32mDetokenization successful matches original string!\033[0m\n"
    print(output)

if __name__ == "__main__":
    tokenizer = MorphTokenizer("<|", "|>")
    print("initialized!")
    start_time = time.time()
    paragraph=(
        "Ayşeyi, Ahmet'i Veli'yi ve ghim'i eve çağırmış."
        " burnu *Burnu havada kitapçımız 2 kglik yani kg'lik TR'li eşyayı Yerismi'ye getirirmiş."
        "\n\tYarın içinse AYŞE'Yİ ve ANNEM'i eVe çağırDI.   "
        "TDK'ye, UNKNOWN'a, TÜİK'e ve ALİ'ye göre olan hjKŞFh şeyler diyorlar.  "
        " Oysa Annem, BABAM ve   kardeşlerime\ngöre\tdoğru olandır."
        "Onlar 11'de veya 12.00'da burada olur."
        "Sonra level2'nin 3/4'ü biter."
    )
    expected = [
        'A', 'y', 'ş', 'e', '<|Noun|>', '<|Acc|>', ',', ' ', 'A', 'h', 'm', 'e', 't', '<|NamedEntity|>', '<|Acc|>', ' ', 'V', 'e', 'l', 'i', '<|NamedEntity|>', '<|Acc|>', ' ', 'v', 'e', ' ', 'g', 'h', 'i', 'm', '<|NamedEntity|>', '<|Acc|>', ' ', 'e', 'v', '<|Noun|>', '<|Dat|>', ' ', 'ç', 'a', 'ğ', 'ı', 'r', '<|Verb|>', '<|Narr|>', '.',
        ' ', 'b', 'u', 'r', 'u', 'n', '<|Noun|>', '<|P3sg|>', ' ', '*', 'B', 'u', 'r', 'u', 'n', '<|Noun|>', '<|Acc|>', ' ', 'h', 'a', 'v', 'a', '<|Noun|>', '<|Loc|>', ' ', 'k', 'i', 't', 'a', 'p', '<|Noun|>', '<|Agt|>', '<|P1pl|>', ' ', '2', ' ', 'k', 'g', '<|Noun|>', '<|Ness|>', ' ', 'y', 'a', 'n', 'i', ' ', 'k', 'g', '<|NamedEntity|>', '<|Ness|>', ' ', 'T', 'R', '<|NamedEntity|>', '<|With|>', ' ', 'e', 'ş', 'y', 'a', '<|Noun|>', '<|Acc|>', ' ', 'Y', 'e', 'r', 'i', 's', 'm', 'i', '<|NamedEntity|>', '<|Dat|>', ' ', 'g', 'e', 't', 'i', 'r', '<|Verb|>', '<|Aor|>', '<|Narr|>', '.',
        '\n', '\t', 'Y', 'a', 'r', 'ı', 'n', ' ', 'i', 'ç', 'i', 'n', '<|Noun|>', '<|Cond|>', ' ', 'A', 'Y', 'Ş', 'E', "'", 'Y', 'İ', ' ', 'v', 'e', ' ', 'A', 'N', 'N', 'E', 'M', '<|NamedEntity|>', '<|Acc|>', ' ', 'e', 'V', 'e', ' ', 'ç', 'a', 'ğ', 'ı', 'r', 'D', 'I', '.', ' ', ' ', ' ',
        'T', 'D', 'K', "'", 'y', 'e', ',', ' ', 'U', 'N', 'K', 'N', 'O', 'W', 'N', '<|NamedEntity|>', '<|Dat|>', ',', ' ', 'T', 'Ü', 'İ', 'K', '<|NamedEntity|>', '<|Dat|>', ' ', 'v', 'e', ' ', 'A', 'L', 'İ', '<|NamedEntity|>', '<|Dat|>', ' ', 'g', 'ö', 'r', 'e', ' ', 'o', 'l', '<|Verb|>', '<|PresPart|>', ' ', 'h', 'j', 'K', 'Ş', 'F', 'h', ' ', 'ş', 'e', 'y', '<|Noun|>', '<|A3pl|>', ' ', 'd', 'e', '<|Verb|>', '<|Prog1|>', '<|A3pl|>', '.',
        ' ', ' ', ' ', 'O', 'y', 's', 'a', ' ', 'A', 'n', 'n', 'e', '<|Noun|>', '<|P1sg|>', ',', ' ', 'B', 'A', 'B', 'A', '<|Noun|>', '<|P1sg|>', ' ', 'v', 'e', ' ', ' ', ' ', 'k', 'a', 'r', 'd', 'e', 'ş', '<|Noun|>', '<|A3pl|>', '<|P1sg|>', '<|Dat|>', '\n', 'g', 'ö', 'r', 'e', '\t', 'd', 'o', 'ğ', 'r', 'u', ' ', 'o', 'l', '<|Verb|>', '<|PresPart|>', '<|Cop|>', '.',
        'O', '<|Noun|>', '<|A3pl|>', ' ', '1', '1', '<|Noun|>', '<|Loc|>', ' ', 'v', 'e', 'y', 'a', ' ', '1', '2', '.', '0', '0', '<|Noun|>', '<|Loc|>', ' ', 'b', 'u', 'r', 'a', '<|Noun|>', '<|Loc|>', ' ', 'o', 'l', '<|Verb|>', '<|Aor|>', '.',
        'S', 'o', 'n', 'r', 'a', ' ', 'l', 'e', 'v', 'e', 'l', '2', "'", 'n', 'i', 'n', ' ', '3', '/', '4', "'", 'ü', ' ', 'b', 'i', 't', '<|Verb|>', '<|Aor|>', '.'
    ]
    test_generation(paragraph, tokenizer, expected)

    test_generation("Jazz bir kediydi. Arkadaşları vardı: Pamuk, Minnoş ve Tekir. Onlar dans etmeyi çok severdi. Bir gün, zor bir dans öğrendiler. Her gün dans ettiler. Sabah, öğle ve akşam.\n\nİlk başlarda çok zorlandılar. Ayakları karıştı, düştüler ve güldüler. Ama pes etmediler. Her gün daha iyi oldular. Jazz, Pamuk, Minnoş ve Tekir birlikte çalıştılar.\n\nSonunda, dansı öğrendiler! Çok mutluydular. Şimdi dans etmeyi biliyorlardı. Dans ederken zıpladılar, döndüler ve kahkaha attılar.\n\nArtık her zaman dans ediyorlardı. Parkta, bahçede ve evde. Jazz ve arkadaşları dans etmeyi çok seviyorlardı!\n", tokenizer, [])
    test_generation("haftasonu vakti", tokenizer, ['h',  'a',  'f',  't',  'a',  's',  'o',  'n',  '<|Noun|>',  '<|Acc|>',  ' ',  'v',  'a',  'k',  'i', 't', '<|Noun|>',  '<|Acc|>'])

    test_generation("Geldiler. Ama pes etmediler.", tokenizer, ['G', 'e', 'l', '<|Verb|>', '<|Past|>', '<|A3pl|>', '.', ' ', 'A', 'm', 'a', ' ', 'p', 'e', 's', ' ', 'e', 't', '<|Verb|>', '<|Neg|>', '<|Past|>', '<|A3pl|>', '.'])
    test_generation(".burnumuzun ", tokenizer, ['.', 'b', 'u', 'r', 'u', 'n', '<|Noun|>', '<|P1pl|>', '<|Gen|>', ' '])
    print("All tests completed!")