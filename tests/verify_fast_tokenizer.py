import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from zemberek import TurkishTokenizer
import fast_tokenizer.fast_tokenizer as fast
import time

zemberek_tokenizer = TurkishTokenizer.DEFAULT
text = "11'de Ali'ye gidiyoruz. Zemberek-python çok hızlı (mı?)."

print("--- Accuracy Verification ---")
print(f"Text: {text}")

# Zemberek
z_tokens = zemberek_tokenizer.tokenize(text)
z_words = [t.content for t in z_tokens]
print(f"Zemberek: {z_words}")

# Fast Tokenizer
f_words = fast.tokenize(text)
print(f"Fast:     {f_words}")

if z_words == f_words:
    print("SUCCESS: Outputs match!")
else:
    print("FAILURE: Outputs do not match.")
    # Show differences
    import difflib
    diff = difflib.ndiff(z_words, f_words)
    print('\n'.join(diff))

print("\n--- Performance Benchmark ---")
paragraph = """
Zemberek, Türk dili için geliştirilmiş en popüler doğal dil işleme kütüphanelerinden biridir. 
Açık kaynak kodlu ve Java ile yazılmış olan bu kütüphane, Türkiye'deki üniversiteler ve çeşitli kurumlar tarafından yaygın olarak kullanılmaktadır. 
Özellikle morfolojik analiz, yazım denetimi ve cümle ayıklama gibi işlemler Zemberek ile kolayca yapılabilir. 
Bu Python portu da orijinal Zemberek kütüphanesinin yeteneklerini Python ekosistemine kazandırmayı amaçlamaktadır. 
Hız ve doğruluk arasındaki dengeyi en iyi şekilde kurmaya çalışır. 
Ayrıca, zengin bir sözlük yapısına ve gelişmiş bir kural sistemine sahiptir. 
Gelecekte daha fazla özellik eklenmesi planlanmaktadır.
""" * 100 # Repeat to make it longer

start = time.perf_counter()
tokens = zemberek_tokenizer.tokenize(paragraph)
z_words = [t.content for t in tokens]
z_time = time.perf_counter() - start
print(f"Zemberek: {z_time:.4f}s ({len(z_words)} tokens)")

start = time.perf_counter()
f_words = fast.tokenize(paragraph)
f_time = time.perf_counter() - start
print(f"Fast:     {f_time:.4f}s ({len(f_words)} tokens)")

if f_time > 0:
    print(f"Speedup: {z_time / f_time:.2f}x")
