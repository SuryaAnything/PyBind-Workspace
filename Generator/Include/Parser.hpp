// Parser.hpp

#pragma once
#include "Types.hpp"
#include <string>
#include <vector>

class Parser {
public:
    static ClassInfo ParseClass(const std::string& content,
        const std::string& class_name, const std::string& file_name);
private:
    static std::vector<std::string> ParseArgs(const std::string& raw_args);
};