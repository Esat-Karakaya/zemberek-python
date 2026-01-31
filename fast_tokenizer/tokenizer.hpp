#ifndef TOKENIZER_HPP
#define TOKENIZER_HPP

#include <string>
#include <vector>

namespace fast_tokenizer {

std::vector<std::string> tokenize(const std::string& text);

} // namespace fast_tokenizer

extern "C" {
    typedef void (*TokenCallback)(const char*);
    void tokenize_to_callback(const char* text, TokenCallback callback);
}

#endif // TOKENIZER_HPP
