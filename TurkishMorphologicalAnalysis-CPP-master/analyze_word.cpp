/*
run:

cd /home/esat/Desktop/zemberek-python/TurkishMorphologicalAnalysis-CPP-master/build
make AnalyzeWord
./AnalyzeWord
*/


#include <iostream>
#include <string>
#include "src/FsmMorphologicalAnalyzer.h"
#include "src/FsmParseList.h"

int main() {
    try {
        std::cout << "Loading Morphological Analyzer..." << std::endl;
        // Paths to dictionary and FSM (Correct order: dictionary, fsm)
        FsmMorphologicalAnalyzer analyzer("turkish_dictionary.txt", "turkish_finite_state_machine.xml");
        std::cout << "Analyzer loaded successfully!\n" << std::endl;
        
        std::string word;
        std::cout << "Enter a Turkish word to analyze (or 'exit' to quit): ";
        while (std::cin >> word && word != "exit") {
            FsmParseList parses = analyzer.morphologicalAnalysis(word);
            if (parses.size() == 0) {
                std::cout << "No analyses found for '" << word << "'." << std::endl;
            } else {
                std::cout << "Analyses for '" << word << "' (" << parses.size() << " found):" << std::endl;
                for (int i = 0; i < parses.size(); ++i) {
                    std::cout << "  [" << i + 1 << "] " << parses.getFsmParse(i).transitionlist() << std::endl;
                }
            }
            std::cout << "\nEnter word: ";
        }
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    return 0;
}
