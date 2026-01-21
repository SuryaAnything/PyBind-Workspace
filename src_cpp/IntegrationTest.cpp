#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <algorithm>
#include "../Core/ws_core.hpp"

class BaseSystem {
public:
    int sys_id;
    BaseSystem(int id) : sys_id(id) {}
    virtual void reset() { sys_id = 0; }
};

class ComputeNode : public BaseSystem {
private:
    std::vector<float> buffer;

public:
    ComputeNode() : BaseSystem(100), buffer{0.0f, 0.0f} {}

    ComputeNode(const std::vector<float>& init_data) 
        : BaseSystem(200), buffer(init_data) 
    {}

    void process(float factor) {
        for(auto& x : buffer) x *= factor;
    }

    void process(float factor, int iterations) {
        for(int i=0; i<iterations; ++i) process(factor);
    }

    // [TEST 4] Operator Overloading
    ComputeNode operator+(const ComputeNode& other) const {
        ComputeNode result;
        
        result.buffer.clear(); 
        
        size_t n = std::min(buffer.size(), other.buffer.size());
        for(size_t i=0; i<n; ++i) {
            result.buffer.push_back(buffer[i] + other.buffer[i]);
        }
        return result;
    }

    float get_average() const {
        if(buffer.empty()) return 0.0f;
        float sum = 0.0f;
        for(float f : buffer) sum += f;
        return sum / buffer.size();
    }

    static std::string version() { return "v1.0.4-alpha"; }

    void forbidden_method() = delete;
};

extern_py_lib(integration_test, BaseSystem, ComputeNode)