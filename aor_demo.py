from zemberek.morphology.generator.word_generator import WordGenerator
from utils import get_morphotactics
from zemberek.morphology.lexicon.dictionary_item import DictionaryItem
from zemberek.morphology.analysis.attributes_helper import AttributesHelper
from zemberek.core.turkish.primary_pos import PrimaryPos
from zemberek.core.turkish.secondary_pos import SecondaryPos
from zemberek.core.turkish.root_attribute import RootAttribute
from zemberek.morphology.morphotactics.stem_transition import StemTransition
from dictionary import morpheme_map

morphotactics = get_morphotactics()
generator = WordGenerator(morphotactics)

root = "koş"

p_pos = PrimaryPos.Verb
s_pos = SecondaryPos.None_
# Add Aorist_A attribute to allow Aorist generation for single-syllable verb
dummy_item = DictionaryItem(root, root, p_pos, s_pos, attributes={RootAttribute.Aorist_A})
start_state = morphotactics.verbRoot_S
phonetic_attrs = AttributesHelper.get_morphemic_attributes(root)
candidate = StemTransition(root, dummy_item, phonetic_attrs, start_state)

# Test Past
res_past = generator.generate(morphemes=tuple([morpheme_map["Past"]]), candidates=tuple([candidate]))
print(f"Past: {[w.surface for w in res_past]}")

# Test Aorist
res_aor = generator.generate(morphemes=tuple([morpheme_map["Aor"]]), candidates=tuple([candidate]))
print(f"Aorist: {[w.surface for w in res_aor]}")