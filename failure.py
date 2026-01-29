from utils import get_morphology
morphology = get_morphology()

# SINGLE WORD MORPHOLOGICAL ANALYSIS
results = morphology.analyze("tr'li") # correct analysis
for result in results:
    print(result)
print("\n")

results = morphology.analyze("11'de") # prints nothing
for result in results:
    print(result)
print("\n")