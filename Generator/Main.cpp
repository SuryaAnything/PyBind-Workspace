#include <iostream>
#include <fstream>
#include <sstream>
#include <filesystem>
#include <unordered_map>
#include <regex>

#include "Include/Sanitizer.hpp"
#include "Include/Parser.hpp"
#include "Include/Emitter.hpp"

namespace fs = std::filesystem;

// Configuration
const std::string SRC_DIR = "src_cpp";
const std::string BINDERS_DIR = "Binders";

std::string read_file(const std::string& path) {
    std::ifstream t(path);
    std::stringstream buffer;
    buffer << t.rdbuf();
    return buffer.str();
}

int main() {
    std::cout << "[Overseer] Agents Initialized.\n";
    if (!fs::exists(SRC_DIR)) {
        std::cerr << "[Error] Source directory missing: " << SRC_DIR << "\n";
        return 1;
    }

    std::unordered_map<std::string, std::vector<ClassInfo>> registry;

    // 1. SCANNING PHASE
    for (const auto& entry : fs::directory_iterator(SRC_DIR)) {
        if (entry.path().extension() != ".cpp") continue;
        
        std::string raw = read_file(entry.path().string());
        
        // Find Targets first to avoid sanitizing irrelevant files
        std::regex macro_re(R"(extern_py_lib\s*\(([^)]+)\))");
        auto start = std::sregex_iterator(raw.begin(), raw.end(), macro_re);
        auto end = std::sregex_iterator();

        if (start == end) continue;

        // 2. SANITIZATION AGENT
        std::string clean = Sanitizer::Clean(raw);

        // 3. PARSING AGENT
        for (auto i = start; i != end; ++i) {
            std::string args = (*i)[1];
            std::stringstream ss(args); std::string seg; std::vector<std::string> p;
            while(std::getline(ss, seg, ',')) {
                size_t f = seg.find_first_not_of(" \t\n");
                if (f != std::string::npos) p.push_back(seg.substr(f, seg.find_last_not_of(" \t\n")-f+1));
            }
            if (p.size() < 2) continue;
            
            std::string lib = p[0];
            for (size_t k = 1; k < p.size(); ++k) {
                std::cout << "  [Scan] Found Target: " << p[k] << "\n";
                registry[lib].push_back(Parser::ParseClass(clean, p[k], entry.path().filename().string()));
            }
        }
    }

    // 4. EMITTER AGENT
    if (registry.empty()) std::cout << "[Overseer] No targets found.\n";
    else {
        for (const auto& pair : registry) {
            Emitter::Write(pair.first, pair.second, BINDERS_DIR, SRC_DIR);
        }
    }

    return 0;
}