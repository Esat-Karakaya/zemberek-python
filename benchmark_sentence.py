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
Jazz bir kediydi. Arkadaşları vardı: Pamuk, Minnoş ve Tekir. Onlar dans etmeyi çok severdi. Bir gün, zor bir dans öğrendiler. Her gün dans ettiler. Sabah, öğle ve akşam.\n\nİlk başlarda çok zorlandılar. Ayakları karıştı, düştüler ve güldüler. Ama pes etmediler. Her gün daha iyi oldular. Jazz, Pamuk, Minnoş ve Tekir birlikte çalıştılar.\n\nSonunda, dansı öğrendiler! Çok mutluydular. Şimdi dans etmeyi biliyorlardı. Dans ederken zıpladılar, döndüler ve kahkaha attılar.\n\nArtık her zaman dans ediyorlardı. Parkta, bahçede ve evde. Jazz ve arkadaşları dans etmeyi çok seviyorlardı!
"""


print(f"Starting benchmark for morphology.analyze_sentence on paragraph...")
start_time = time.perf_counter()

total_words = 0
results = morphology.analyze_sentence(paragraph)
total_words += len(results)

end_time = time.perf_counter()
duration = end_time - start_time

print("-" * 30)
print(f"Total time: {duration:.4f} seconds")
print(f"Total words analyzed: {total_words}")
if duration > 0:
    print(f"Speed: {total_words / duration:.2f} words/second")
print("-" * 30)
