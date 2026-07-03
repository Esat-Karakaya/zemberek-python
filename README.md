This project is derived from the Python port of Zemberek by Loodos, which is itself based on the original Zemberek Java project by Ahmet A. Akın and Mehmet D. Akın.

# Goal of pre_bpe_morph
This package recognizes verbs, nouns, and named entities and their suffixes. Before BPE, this package removes suffixes and replaces them with their respective special tokens for identifiability. It also precedes a word type (Verb/Noun/NamedEntity) before any set of suffixes. The goal is to simplify Turkish grammar rules for small language models.

## Usage
```python
from pre_bpe_morph_tr.morph_tokenizer import MorphTokenizer
tokenizer=MorphTokenizer("<|", "|>")

tokenizer.tokenize("gülüveriniz")
# response: ['g', 'ü', 'l', '<|Verb|>', '<|Hastily|>', '<|Req|>']

tokenizer.detokenize(['k', 'o', 'ş', '<|Verb|>', '<|Fut|>', '<|A1sg|>'])
# response: "koşacağım"
```

## Developed for language model
Since this is developed for LM training, I tried to avoid preprocessing text (like converting "hal" to "hâl", or lowercasing words). The text should remain unchanged when encoded and then decoded.

## Notes
Keep in mind that this was created for research only and is kind of slow.
If you come across an error that says "ModuleNotFoundError: No module named 'pkg_resources'" that you have to install setuptools. Run:
```bash
pip install setuptools==81.0.0 # Newer versions may not work
```