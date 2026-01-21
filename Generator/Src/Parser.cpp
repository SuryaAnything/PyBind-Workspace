#include "../Include/Parser.hpp"
#include <regex>
#include <sstream>
#include <unordered_set>

std::string get_operator_python_name(const std::string& cpp_name) {
    if (cpp_name == "operator+") return "__add__";
    if (cpp_name == "operator-") return "__sub__";
    if (cpp_name == "operator*") return "__mul__";
    if (cpp_name == "operator/") return "__truediv__";
    if (cpp_name == "operator+=") return "__iadd__";
    if (cpp_name == "operator-=") return "__isub__";
    if (cpp_name == "operator==") return "__eq__";
    if (cpp_name == "operator!=") return "__ne__";
    return ""; 
}

std::vector<std::string> Parser::ParseArgs(const std::string& raw_args) {
    std::vector<std::string> args;
    std::string current;
    int angle_depth = 0;
    for (char c : raw_args) {
        if (c == '<') angle_depth++; else if (c == '>') angle_depth--;
        if (c == ',' && angle_depth == 0) { if (!current.empty()) args.push_back(current); current = ""; }
        else current += c;
    }
    if (!current.empty()) args.push_back(current);

    static const std::unordered_set<std::string> keywords = {
        "int", "float", "double", "char", "bool", "long", "short", "void", "unsigned", "signed",
        "const", "std::string", "std::vector", "std::map", "auto", "size_t",
        "int8_t", "int16_t", "int32_t", "int64_t", "uint8_t", "uint16_t", "uint32_t", "uint64_t"
    };

    std::vector<std::string> final_types;
    for (auto& arg : args) {
        size_t first = arg.find_first_not_of(" \t");
        if (first == std::string::npos) continue;
        std::string trimmed = arg.substr(first, arg.find_last_not_of(" \t") - first + 1);
        size_t eq_pos = trimmed.find('=');
        if (eq_pos != std::string::npos) trimmed = trimmed.substr(0, eq_pos);
        std::stringstream ss(trimmed); std::string seg; std::vector<std::string> p;
        while(std::getline(ss, seg, ' ')) if (!seg.empty()) p.push_back(seg);
        if (!p.empty()) {
            std::string last = p.back();
            bool is_ptr = (last.find_first_of("*&<>") != std::string::npos);
            bool is_key = (keywords.find(last) != keywords.end());
            if (!is_ptr && !is_key && p.size() > 1) trimmed = trimmed.substr(0, trimmed.rfind(last));
        }
        size_t l = trimmed.find_last_not_of(" \t");
        if (l != std::string::npos) final_types.push_back(trimmed.substr(0, l+1));
        else final_types.push_back(trimmed);
    }
    return final_types;
}

ClassInfo Parser::ParseClass(const std::string& content, const std::string& class_name, const std::string& file_name) {
    ClassInfo info; info.name = class_name; info.source_file = file_name;

    std::regex class_re("class\\s+" + class_name + "\\s*(:\\s*public\\s+([\\w_]+))?\\s*\\{");
    std::smatch match;
    if (!std::regex_search(content, match, class_re)) return info;

    if (match[2].matched) info.parent_name = match[2];

    size_t body_start = match.position() + match.length();
    size_t brace = 1, i = body_start;
    for (; i < content.size(); ++i) {
        if (content[i] == '{') brace++; else if (content[i] == '}') brace--;
        if (brace == 0) break;
    }
    std::string body = content.substr(body_start, i - body_start);

    bool is_public = false; std::string public_code;
    for (size_t j = 0; j < body.size(); ++j) {
        if (body.substr(j).rfind("public:", 0) == 0) { is_public = true; j+=6; continue; }
        if (body.substr(j).rfind("private:", 0) == 0) { is_public = false; j+=7; continue; }
        if (body.substr(j).rfind("protected:", 0) == 0) { is_public = false; j+=9; continue; }
        if (is_public) public_code += body[j];
    }

    // [CRITICAL FIX] 
    // Accept BOTH '{' and ';' as terminators for initializer lists.
    // The Sanitizer turns '{' into ';' for inline constructors, so we must support it.
    std::regex init_list_re(R"(\)\s*:[^{;]*[;\{])"); 
    public_code = std::regex_replace(public_code, init_list_re, ");");

    // Scan Constructors
    // Also matches ending with ; or {
    std::regex ctor_re(R"(\b(explicit\s+)?)" + class_name + R"(\s*\(([^)]*)\)\s*(=.*)?\s*[\{;])");
    auto c_start = std::sregex_iterator(public_code.begin(), public_code.end(), ctor_re);
    for (auto it = c_start; it != std::sregex_iterator(); ++it) {
        std::smatch m = *it;
        std::string suffix = m[3]; 
        if (suffix.find("delete") != std::string::npos) continue;

        MethodInfo ctor; ctor.name = class_name; ctor.is_constructor = true; ctor.is_static = false; ctor.is_const = false;
        ctor.args = ParseArgs(m[2]);
        info.methods.push_back(ctor);
    }

    // Scan Methods
    std::regex m_re(R"(\s*(static\s+)?([a-zA-Z0-9_<>*&]+)\s+([\w_+=\-*/!]+)\s*\(([^)]*)\)\s*(const)?\s*(=.*)?\s*[;\{])");
    auto m_start = std::sregex_iterator(public_code.begin(), public_code.end(), m_re);
    for (auto it = m_start; it != std::sregex_iterator(); ++it) {
        std::smatch m = *it;
        std::string name = m[3];
        std::string suffix = m[6]; 

        if (suffix.find("delete") != std::string::npos) continue;
        if (name == "if" || name == "while" || name == "for" || name == "switch" || name == "return") continue;
        if (name == class_name || name.rfind("~", 0) == 0) continue;
        
        MethodInfo method; 
        method.name = name; 
        method.is_static = m[1].matched; 
        method.is_constructor = false;
        method.is_const = m[5].matched;
        method.args = ParseArgs(m[4]);
        method.operator_name = get_operator_python_name(name);
        
        info.methods.push_back(method);
    }
    return info;
}