#include "../Include/Sanitizer.hpp"

std::string Sanitizer::Clean(const std::string& raw) {
    std::string clean = raw;
    int n = clean.size();

    bool in_string = false, in_char = false, in_line_comment = false, in_block_comment = false;
    int brace_depth = 0;

    for (int i = 0; i < n; ++i) {
        char c = clean[i];
        
        // 1. Handle Comments & Strings (Unchanged)
        if (in_line_comment) { if (c == '\n') in_line_comment = false; else clean[i] = ' '; continue; }
        if (in_block_comment) { 
            if (c == '*' && i+1 < n && clean[i+1] == '/') { clean[i]=' '; clean[i+1]=' '; in_block_comment = false; i++; } 
            else clean[i] = ' '; 
            continue; 
        }
        if (in_string) { if (c == '\\') i++; else if (c == '"') in_string = false; else clean[i] = ' '; continue; }
        if (in_char) { if (c == '\\') i++; else if (c == '\'') in_char = false; else clean[i] = ' '; continue; }

        if (c == '/' && i+1 < n) {
            if (clean[i+1] == '/') { in_line_comment = true; clean[i]=' '; clean[i+1]=' '; i++; continue; }
            if (clean[i+1] == '*') { in_block_comment = true; clean[i]=' '; clean[i+1]=' '; i++; continue; }
        }
        if (c == '"') { in_string = true; continue; }
        if (c == '\'') { in_char = true; continue; }

        // 2. Handle Bodies (IMPROVED)
        if (c == '{') { 
            brace_depth++; 
            // If we are entering a method body (depth 2), replace '{' with ';'
            // This turns "void func() { ... }" into "void func(); ... }"
            // allowing the regex to match it as a declaration.
            if (brace_depth == 2) clean[i] = ';'; 
            else if (brace_depth > 2) clean[i] = ' '; 
            continue; 
        }
        if (c == '}') { 
            if (brace_depth > 1) clean[i] = ' '; 
            brace_depth--; 
            continue; 
        }
        
        if (brace_depth >= 2) clean[i] = ' ';
    }
    return clean;
}