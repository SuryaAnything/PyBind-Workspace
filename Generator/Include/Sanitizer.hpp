// Sanitizer.hpp

#pragma once
#include <string>

class Sanitizer {
public:
    // Removes comments, strings, and function bodies
    static std::string Clean(const std::string& raw_code);
};