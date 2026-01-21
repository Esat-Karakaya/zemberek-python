from morph_tokenizer import MorphTokenizer

def print_test(sentence: str, tokenizer: MorphTokenizer):
    tokens = tokenizer._MorphTokenizer__tokenize_sentence(sentence)
    print(f"Tokens: {tokens}")
    print()

if __name__ == "__main__":
    tokenizer = MorphTokenizer("<|", "|>")
    print_test("Ayşe'yi eve çağırdı.", tokenizer)
    print_test("kitapçı eve gelirmiş.", tokenizer)
    print_test("Burnu havadadır onun.", tokenizer)
    print_test("burnu havadadır onun.", tokenizer)
    print_test("Yerisimi'ye gelirmiş.", tokenizer)

    print_test("AYŞE'Yİ eVe çağırDI", tokenizer)
    print_test("TDK'ye göre olan şeyler", tokenizer)
    print_test("TÜİK'e göre olan şeyler", tokenizer)
    print_test("UNKNOWN'a göre olan şeyler", tokenizer)
    # output tokens: [['Ayşe', '<|Acc|>'], ['ev', '<|Dat|>'], ['çağır', '<|Past|>']]
    # should've created three tokens with PrimaryPosition Unknown