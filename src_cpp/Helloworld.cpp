#include "../Core/ws_core.hpp"
#include <string>

class HelloWorld {
private:
    std::string msg;
public:
    HelloWorld(const std::string& message) : msg(message) {}
    std::string greet() {
        return msg;
    }
};

extern_py_lib(helloworld, HelloWorld)