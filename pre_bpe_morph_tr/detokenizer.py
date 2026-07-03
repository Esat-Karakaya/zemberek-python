from typing import List
from collections import OrderedDict

from pre_bpe_morph_tr.word_generator import CustomWordGenerator

class MorphDetokenizer:
    def __init__(self, tk_start: str = "<|", tk_end: str = "|>", cache_limit: int = 100):
        self.tk_start = tk_start
        self.tk_end = tk_end
        self.tk_start_len = len(tk_start)
        self.tk_end_len = len(tk_end)
        self.pos_tags = {"Noun", "Verb", "NamedEntity"}
        self.generator = CustomWordGenerator()
        self.generation_cache = OrderedDict()
        self.cache_limit = cache_limit

    def _is_special_token(self, token: str) -> bool:
        return token.startswith(self.tk_start) and token.endswith(self.tk_end)

    def _strip_token(self, token: str) -> str:
        return token[self.tk_start_len : -self.tk_end_len]

    def _is_word_char(self, token: str) -> bool:
        return token.isalnum()

    def _collect_suffixes(self, tokens: List[str], start_idx: int) -> tuple[List[str], int]:
        """Collect all contiguous suffix tokens starting at start_idx."""
        suffixes = []
        n = len(tokens)
        i = start_idx
        while i < n and self._is_special_token(tokens[i]):
            suffix_inner = self._strip_token(tokens[i])
            # If we hit a word type POS tag, stop collecting suffixes
            if suffix_inner in self.pos_tags:
                break
            suffixes.append(suffix_inner)
            i += 1
        return suffixes, i

    def _reconstruct_and_append(self, word_type: str, suffixes: List[str], current_chars: List[str], result_parts: List[str]):
        """Reconstruct the word from the root and suffixes and append it to result_parts."""
        root = "".join(current_chars)
        cache_key = (root, word_type, tuple(suffixes))
        
        if cache_key in self.generation_cache:
            reconstructed = self.generation_cache[cache_key]
            self.generation_cache.move_to_end(cache_key)
        else:
            reconstructed = self.generator.generate_word(root, word_type, suffixes)
            self.generation_cache[cache_key] = reconstructed
            if len(self.generation_cache) > self.cache_limit:
                self.generation_cache.popitem(last=False)
            
        result_parts.append(reconstructed)

    def detokenize(self, tokens: List[str]) -> str:
        result_parts = []
        current_chars = []
        
        i = 0
        n = len(tokens)
        while i < n:
            token = tokens[i]
            
            if self._is_special_token(token):
                inner = self._strip_token(token)
                
                if inner in self.pos_tags:
                    # Case 1: POS tag followed by suffixes
                    suffixes, i = self._collect_suffixes(tokens, i + 1)
                    self._reconstruct_and_append(inner, suffixes, current_chars, result_parts)
                    current_chars = []
                else:
                    # Case 2: Suffix token without a preceding POS tag
                    suffixes, i = self._collect_suffixes(tokens, i + 1)
                    suffixes.insert(0, inner)
                    self._reconstruct_and_append("Noun", suffixes, current_chars, result_parts)
                    current_chars = []
            else:
                # Normal character, whitespace, or punctuation
                if self._is_word_char(token):
                    current_chars.append(token)
                else:
                    if current_chars:
                        result_parts.append("".join(current_chars))
                        current_chars = []
                    result_parts.append(token)
                i += 1
                
        # Append any remaining characters
        if current_chars:
            result_parts.append("".join(current_chars))
            
        return "".join(result_parts)

