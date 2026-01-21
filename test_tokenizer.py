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
    print_test("TDK'ye, UNKNOWN'a ve TÜİK'e göre olan hjKŞFh şeyler", tokenizer)

    # loss of info: where and what were the whitespaces?
    print_test("Annem, babam ve   kardeşlerime\ngöre\tdoğru olandır. ", tokenizer)