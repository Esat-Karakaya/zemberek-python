from zemberek.morphology.generator.word_generator import WordGenerator
from utils import get_morphotactics
from zemberek.morphology.lexicon.dictionary_item import DictionaryItem
from zemberek.morphology.analysis.attributes_helper import AttributesHelper
from zemberek.core.turkish.primary_pos import PrimaryPos
from zemberek.core.turkish.secondary_pos import SecondaryPos
from zemberek.morphology.morphotactics.stem_transition import StemTransition
from dictionary import morpheme_map

morphotactics = get_morphotactics()
generator = WordGenerator(morphotactics)

root = "koş"

p_pos=PrimaryPos.Verb
s_pos = SecondaryPos.None_
dummy_item = DictionaryItem(root, root, p_pos, s_pos)
start_state = morphotactics.verbRoot_S if p_pos == PrimaryPos.Verb else morphotactics.noun_S
phonetic_attrs = AttributesHelper.get_morphemic_attributes(root)
candidate = StemTransition(root, dummy_item, phonetic_attrs, start_state)

# Test Past
res_past = generator.generate(morphemes=tuple([morpheme_map["Past"], morpheme_map["A3sg"]]), candidates=tuple([candidate]))
print(f"Past (A3sg): {res_past[0].surface if len(res_past)>0 else res_past}")

# Test Aorist
res_aor = generator.generate(morphemes=tuple([morpheme_map["Aor"], morpheme_map["A1pl"]]), candidates=tuple([candidate]))
print(f"Aorist (A1pl): {res_aor[0].surface if len(res_aor)>0 else res_aor}")