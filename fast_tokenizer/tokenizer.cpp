#include "tokenizer.hpp"
#include <cwctype>
#include <locale>
#include <codecvt>

namespace fast_tokenizer {

// A simple and fast tokenizer for Turkish.
// It splits by whitespace, preserves words/numbers with apostrophes (e.g., "11'de", "Ali'ye"),
// and treats other punctuation as individual tokens.
std::vector<std::string> tokenize(const std::string& text) {
    std::vector<std::string> tokens;
    if (text.empty()) return tokens;

    // Convert UTF-8 to UTF-32 for easier character-level processing
    std::wstring_convert<std::codecvt_utf8<char32_t>, char32_t> converter;
    std::u32string u32text = converter.from_bytes(text);

    size_t i = 0;
    size_t n = u32text.length();

    while (i < n) {
        char32_t c = u32text[i];

        // Skip whitespace
        if (std::iswspace(static_cast<wint_t>(c))) {
            i++;
            continue;
        }

        // Alphanumeric word (including potential apostrophes)
        if (std::iswalnum(static_cast<wint_t>(c))) {
            size_t start = i;
            while (i < n) {
                char32_t current = u32text[i];
                if (std::iswalnum(static_cast<wint_t>(current))) {
                    i++;
                } else if (current == '\'' || current == 0x2019 || current == '-') { // Apostrophe or hyphen
                    // Check if symbol is followed by an alphanumeric character
                    if (i + 1 < n && std::iswalnum(static_cast<wint_t>(u32text[i + 1]))) {
                        i++; // Include symbol
                    } else {
                        break; 
                    }
                } else {
                    break;
                }
            }
            tokens.push_back(converter.to_bytes(u32text.substr(start, i - start)));
        } else {
            // Punctuation or other characters
            tokens.push_back(converter.to_bytes(u32text.substr(i, 1)));
            i++;
        }
    }

    return tokens;
}

} // namespace fast_tokenizer

extern "C" {
    void tokenize_to_callback(const char* text, TokenCallback callback) {
        if (!text || !callback) return;
        std::vector<std::string> tokens = fast_tokenizer::tokenize(text);
        for (const auto& token : tokens) {
            callback(token.c_str());
        }
    }
}
