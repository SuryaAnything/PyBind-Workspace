// Emitter.hpp

#pragma once
#include "Types.hpp"
#include <vector>

class Emitter {
public:
    static void Write(const std::string& lib_name,
        const std::vector<ClassInfo>& classes,
        const std::string& output_dir, const std::string& src_dir);
};