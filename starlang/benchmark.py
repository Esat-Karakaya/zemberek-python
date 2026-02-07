import sys
from pathlib import Path

# Add the parent directory to sys.path to allow importing from the root
sys.path.append(str(Path(__file__).resolve().parent.parent))

import time
import starlang
from zemberek.morphology import TurkishMorphology

def benchmark():
    sentence = "Bugün hava çok güzel ama yarın yağmur yağabilir." * 10
    
    print("Initializing Zemberek...")
    start = time.time()
    morphology = TurkishMorphology.create_with_defaults()
    print(f"Zemberek initialized in {time.time() - start:.2f}s")
    
    print("Initializing Starlang...")
    start = time.time()
    starlang.init()
    print(f"Starlang initialized in {time.time() - start:.2f}s")
    
    print("\nBenchmarking Zemberek analyze_sentence...")
    start = time.time()
    for _ in range(100):
        morphology.analyze_sentence(sentence)
    z_time = time.time() - start
    print(f"Zemberek took: {z_time:.4f}s")
    
    print("\nBenchmarking Starlang analyze...")
    start = time.time()
    for _ in range(100):
        starlang.analyze(sentence)
    s_time = time.time() - start
    print(f"Starlang took: {s_time:.4f}s")
    
    print(f"\nSpeedup: {z_time / s_time:.2f}x")

    # Correctness check
    print("\nSample Output:")
    sample = "Gidiyorum."
    z_res = morphology.analyze_sentence(sample)
    s_res = starlang.analyze(sample)
    
    print(f"Input: {sample}")
    print(f"Zemberek: {[a.inp for a in z_res] if z_res else 'None'}")
    print(f"Starlang: {s_res}")

if __name__ == "__main__":
    try:
        benchmark()
    except Exception as e:
        print(f"Error during benchmark: {e}")
