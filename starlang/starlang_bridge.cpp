#include <iostream>
#include <string>
#include <vector>
#include <cwctype>
#include <locale>
#include <codecvt>
#include <unistd.h>
#include "../TurkishMorphologicalAnalysis-CPP-master/src/FsmMorphologicalAnalyzer.h"
#include "../TurkishMorphologicalAnalysis-CPP-master/src/FsmParseList.h"

namespace starlang {

static FsmMorphologicalAnalyzer* analyzer = nullptr;

void init(const char* fsm_path, const char* dict_path, const char* data_dir) {
    if (!analyzer) {
        if (data_dir && data_dir[0] != '\0') {
            if (chdir(data_dir) != 0) {
                std::cerr << "Warning: Could not change directory to " << data_dir << std::endl;
            }
        }
        analyzer = new FsmMorphologicalAnalyzer(dict_path, fsm_path);
    }
}

// Helper to convert UTF-8 string to UTF-32
std::u32string utf8_to_utf32(const std::string& utf8) {
    std::u32string utf32;
    for (size_t i = 0; i < utf8.length(); ) {
        unsigned char c = utf8[i];
        char32_t cp = 0;
        size_t len = 0;
        if (c <= 0x7f) { cp = c; len = 1; }
        else if ((c & 0xe0) == 0xc0) { cp = c & 0x1f; len = 2; }
        else if ((c & 0xf0) == 0xe0) { cp = c & 0x0f; len = 3; }
        else if ((c & 0xf8) == 0xf0) { cp = c & 0x07; len = 4; }
        else { i++; continue; }

        if (i + len > utf8.length()) break;
        for (size_t j = 1; j < len; j++) {
            cp = (cp << 6) | (utf8[i + j] & 0x3f);
        }
        utf32.push_back(cp);
        i += len;
    }
    return utf32;
}

// Helper to convert single UTF-32 char to UTF-8 string
std::string utf32_to_utf8(char32_t cp) {
    std::string utf8;
    if (cp <= 0x7f) {
        utf8 += static_cast<char>(cp);
    } else if (cp <= 0x7ff) {
        utf8 += static_cast<char>(0xc0 | (cp >> 6));
        utf8 += static_cast<char>(0x80 | (cp & 0x3f));
    } else if (cp <= 0xffff) {
        utf8 += static_cast<char>(0xe0 | (cp >> 12));
        utf8 += static_cast<char>(0x80 | ((cp >> 6) & 0x3f));
        utf8 += static_cast<char>(0x80 | (cp & 0x3f));
    } else if (cp <= 0x10ffff) {
        utf8 += static_cast<char>(0xf0 | (cp >> 18));
        utf8 += static_cast<char>(0x80 | ((cp >> 12) & 0x3f));
        utf8 += static_cast<char>(0x80 | ((cp >> 6) & 0x3f));
        utf8 += static_cast<char>(0x80 | (cp & 0x3f));
    }
    return utf8;
}

// Helper to convert UTF-32 string to UTF-8
std::string utf32_to_utf8(const std::u32string& utf32) {
    std::string utf8;
    for (char32_t cp : utf32) {
        utf8 += utf32_to_utf8(cp);
    }
    return utf8;
}

std::vector<std::string> tokenize(const std::string& text) {
    std::vector<std::string> tokens;
    if (text.empty()) return tokens;

    try {
        std::u32string u32text = utf8_to_utf32(text);

        size_t i = 0;
        size_t n = u32text.length();

        while (i < n) {
            char32_t c = u32text[i];
            if (std::iswspace(static_cast<wint_t>(c))) {
                i++;
                continue;
            }

            if (std::iswalnum(static_cast<wint_t>(c))) {
                size_t start = i;
                while (i < n) {
                    char32_t current = u32text[i];
                    if (std::iswalnum(static_cast<wint_t>(current))) {
                        i++;
                    } else if (current == '\'' || current == 0x2019 || current == '-') {
                        if (i + 1 < n && std::iswalnum(static_cast<wint_t>(u32text[i + 1]))) {
                            i++;
                        } else {
                            break;
                        }
                    } else {
                        break;
                    }
                }
                tokens.push_back(utf32_to_utf8(u32text.substr(start, i - start)));
            } else {
                tokens.push_back(utf32_to_utf8(u32text.substr(i, 1)));
                i++;
            }
        }
    } catch (...) {
        // Fallback for encoding errors
    }
    return tokens;
}

std::string analyze_text(const std::string& text) {
    if (!analyzer) return "ERROR: Analyzer not initialized";
    
    std::vector<std::string> tokens = tokenize(text);
    std::string result;
    
    for (const auto& token : tokens) {
        FsmParseList parses = analyzer->morphologicalAnalysisGreedy(token);
        if (parses.size() > 0) {
            FsmParse best = parses.getParseWithLongestRootWord();
            result += token + "|" + best.transitionlist();
        } else {
            result += token + "|UNKNOWN";
        }
        result += "\n";
    }
    return result;
}

} // namespace starlang

extern "C" {
    void starlang_init(const char* fsm_path, const char* dict_path, const char* data_dir) {
        starlang::init(fsm_path, dict_path, data_dir);
    }

    const char* starlang_analyze(const char* text) {
        static std::string last_result;
        last_result = starlang::analyze_text(text);
        return last_result.c_str();
    }
}
