from zemberek.morphology.lexicon.root_lexicon import RootLexicon
from zemberek.core.turkish.root_attribute import RootAttribute
import logging

def extract_exceptions():
    print("Loading full lexicon...")
    lexicon = RootLexicon.get_default()
    print(f"Loaded {len(lexicon)} items.")

    exception_attributes = {
        RootAttribute.Voicing,
        RootAttribute.InverseHarmony,
        RootAttribute.Doubling,
        RootAttribute.LastVowelDrop,
        RootAttribute.ProgressiveVowelDrop,
        RootAttribute.CompoundP3sg,
        RootAttribute.Aorist_I, # Optional: strictly speaking morphology parameter, but often irregular
        RootAttribute.Aorist_A,
    }

    exceptions = []
    
    for item in lexicon:
        if item.attributes and not item.attributes.isdisjoint(exception_attributes):
             exceptions.append(item)
    
    # Sort for consistent output
    exceptions.sort(key=lambda x: x.lemma)
    
    output_file = "exceptions.txt"
    print(f"Found {len(exceptions)} exceptions. Writing to {output_file}...")
    
    with open(output_file, "w", encoding="utf-8") as f:
        for item in exceptions:
            # Format: word <TAB> primary_pos
            f.write(f"{item.lemma}\t{item.primary_pos.value}\n")
            
    print("Done.")

if __name__ == "__main__":
    extract_exceptions()
