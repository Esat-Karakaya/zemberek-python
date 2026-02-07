CXX = g++
CXXFLAGS = -O3 -fPIC -std=c++20 \
           -I../TurkishMorphologicalAnalysis-CPP-master/src \
           -I../deps/Dictionary-CPP/src \
           -I../deps/Corpus-CPP/src \
           -I../deps/XmlParser-CPP/src \
           -I../deps/Util-CPP/src \
           -I../deps/DataStructure-CPP/src \
           -I../deps/DataStructure-CPP/src/Cache \
           -I../deps/Math-CPP/src

# Source files from TurkishMorphologicalAnalysis
MORPH_SRC_DIR = ../TurkishMorphologicalAnalysis-CPP-master/src
MORPH_SOURCES = $(MORPH_SRC_DIR)/DisambiguatedWord.cpp \
                $(MORPH_SRC_DIR)/DisambiguationCorpus.cpp \
                $(MORPH_SRC_DIR)/MetamorphicParse.cpp \
                $(MORPH_SRC_DIR)/InflectionalGroup.cpp \
                $(MORPH_SRC_DIR)/State.cpp \
                $(MORPH_SRC_DIR)/Transition.cpp \
                $(MORPH_SRC_DIR)/MorphologicalParse.cpp \
                $(MORPH_SRC_DIR)/FsmParse.cpp \
                $(MORPH_SRC_DIR)/FsmParseList.cpp \
                $(MORPH_SRC_DIR)/FiniteStateMachine.cpp \
                $(MORPH_SRC_DIR)/FsmMorphologicalAnalyzer.cpp \
                $(MORPH_SRC_DIR)/MorphotacticEngine.cpp

# Dependency sources
DEPS_DIR = ../deps
DEP_SOURCES = $(DEPS_DIR)/Dictionary-CPP/src/Dictionary/Word.cpp \
              $(DEPS_DIR)/Dictionary-CPP/src/Dictionary/TxtWord.cpp \
              $(DEPS_DIR)/Dictionary-CPP/src/Dictionary/Dictionary.cpp \
              $(DEPS_DIR)/Dictionary-CPP/src/Dictionary/TxtDictionary.cpp \
              $(DEPS_DIR)/Dictionary-CPP/src/Dictionary/Trie/Trie.cpp \
              $(DEPS_DIR)/Dictionary-CPP/src/Dictionary/Trie/TrieNode.cpp \
              $(DEPS_DIR)/Util-CPP/src/StringUtils.cpp \
              $(DEPS_DIR)/XmlParser-CPP/src/XmlDocument.cpp \
              $(DEPS_DIR)/XmlParser-CPP/src/XmlElement.cpp \
              $(DEPS_DIR)/Dictionary-CPP/src/Dictionary/VectorizedDictionary.cpp \
              $(DEPS_DIR)/Corpus-CPP/src/Corpus.cpp \
              $(DEPS_DIR)/Corpus-CPP/src/Sentence.cpp \
              $(DEPS_DIR)/Math-CPP/src/Vector.cpp \
              $(DEPS_DIR)/Math-CPP/src/VectorSizeMismatch.cpp \
              $(DEPS_DIR)/Dictionary-CPP/src/Dictionary/VectorizedWord.cpp \
              $(DEPS_DIR)/Corpus-CPP/src/Paragraph.cpp \
              $(DEPS_DIR)/Dictionary-CPP/src/Dictionary/ExceptionalWord.cpp \
              $(DEPS_DIR)/XmlParser-CPP/src/XmlAttribute.cpp \
              $(DEPS_DIR)/Corpus-CPP/src/SentenceSplitter.cpp \
              $(DEPS_DIR)/Corpus-CPP/src/TurkishSplitter.cpp \
              $(DEPS_DIR)/Corpus-CPP/src/TurkishChecker.cpp

# Our bridge
SOURCES = starlang_bridge.cpp $(MORPH_SOURCES) $(DEP_SOURCES)
OBJECTS = $(SOURCES:.cpp=.o)
TARGET = libstarlang.so

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CXX) -shared -o $@ $(OBJECTS) $(LDFLAGS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJECTS) $(TARGET)
