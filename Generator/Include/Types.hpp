#pragma once
#include <string>
#include <vector>

struct MethodInfo {
    std::string name;
    bool is_static;
    bool is_constructor;
    bool is_const;
    std::vector<std::string> args;
    std::string operator_name;
};

struct ClassInfo {
    std::string name;
    std::string parent_name;
    std::string source_file;
    std::vector<MethodInfo> methods;
};