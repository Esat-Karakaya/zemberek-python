import time
from zemberek import TurkishMorphology, TurkishSentenceExtractor

# Initialize morphology and extractor
# This part is excluded from benchmark timing as it involves loading resources
print("Initializing Zemberek...")
morphology = TurkishMorphology.create_with_defaults()
extractor = TurkishSentenceExtractor()

# Placeholder paragraph - feel free to replace with a longer text
paragraph = """
Zemberek, Türk dili için geliştirilmiş en popüler doğal dil işleme kütüphanelerinden biridir. 
Açık kaynak kodlu ve Java ile yazılmış olan bu kütüphane, Türkiye'deki üniversiteler ve çeşitli kurumlar tarafından yaygın olarak kullanılmaktadır. 
Özellikle morfolojik analiz, yazım denetimi ve cümle ayıklama gibi işlemler Zemberek ile kolayca yapılabilir. 
Bu Python portu da orijinal Zemberek kütüphanesinin yeteneklerini Python ekosistemine kazandırmayı amaçlamaktadır. 
Hız ve doğruluk arasındaki dengeyi en iyi şekilde kurmaya çalışır. 
Ayrıca, zengin bir sözlük yapısına ve gelişmiş bir kural sistemine sahiptir. 
Gelecekte daha fazla özellik eklenmesi planlanmaktadır.
"""

# Extract sentences first
sentences = extractor.from_paragraph(paragraph)

print(f"Starting benchmark for morphology.analyze_sentence on {len(sentences)} sentences...")
start_time = time.perf_counter()

total_words = 0
for sentence in sentences:
    # Benchmark target: analyze_sentence
    results = morphology.analyze_sentence(sentence)
    total_words += len(results)

end_time = time.perf_counter()
duration = end_time - start_time

print("-" * 30)
print(f"Total time: {duration:.4f} seconds")
print(f"Total sentences analyzed: {len(sentences)}")
print(f"Total words analyzed: {total_words}")
if duration > 0:
    print(f"Speed: {total_words / duration:.2f} words/second")
print("-" * 30)
