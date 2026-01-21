#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <algorithm>
#include "ws_core.hpp"

// ------------------------------------------------------------------
// Base Class: Verifies Inheritance Detection
// ------------------------------------------------------------------
class BaseSystem {
public:
    int sys_id;
    
    BaseSystem(int id) : sys_id(id) {}
    
    virtual void reset() {
        sys_id = 0;
    }
};

// ------------------------------------------------------------------
// Derived Class: Verifies Complex Parsing Features
// ------------------------------------------------------------------
class ComputeNode : public BaseSystem {
private:
    std::vector<float> buffer;

public:
    // [TEST 1] Initializer List Parsing (ignoring : BaseSystem(0))
    ComputeNode() : BaseSystem(100), buffer{0.0f, 0.0f} {}

    // [TEST 2] Constructor with STL Arguments
    ComputeNode(const std::vector<float>& init_data) 
        : BaseSystem(200), buffer(init_data) 
    {}

    // [TEST 3] Method Overloading (Requires py::overload_cast)
    void process(float factor) {
        for(auto& x : buffer) x *= factor;
    }

    void process(float factor, int iterations) {
        for(int i=0; i<iterations; ++i) process(factor);
    }

    // [TEST 4] Operator Overloading (Should map to __add__)
    ComputeNode operator+(const ComputeNode& other) const {
        ComputeNode result;
        // Simple element-wise addition for demo
        size_t n = std::min(buffer.size(), other.buffer.size());
        for(size_t i=0; i<n; ++i) {
            result.buffer.push_back(buffer[i] + other.buffer[i]);
        }
        return result;
    }

    // [TEST 5] Const Correctness (Requires py::const_)
    float get_average() const {
        if(buffer.empty()) return 0.0f;
        float sum = 0.0f;
        for(float f : buffer) sum += f;
        return sum / buffer.size();
    }

    // [TEST 6] Deleted Functions (Must be SKIPPED by Parser)
    // If generated, this will cause a compile error.
    ComputeNode(const ComputeNode&) = delete;
    void operator=(const ComputeNode&) = delete;

    // [TEST 7] Static Method
    static std::string version() {
        return "v1.0.4-alpha";
    }
};

// Expose classes to Python
extern_py_lib(integration_test, BaseSystem, ComputeNode)