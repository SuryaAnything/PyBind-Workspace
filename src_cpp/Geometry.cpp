#include "ws_core.hpp"
#include <string>
#include <iostream>

class Point {
public: 
    // FIXED: Added implementation {}
    void move(int x, int y) {
        std::cout << "Point moved to " << x << ", " << y << std::endl;
    }
};

class Rect {
public: 
    // FIXED: Added implementation
    int area() {
        return 100; // Dummy value
    }

    static std::string print() {
        return "Rect Class";
    }
};

extern_py_lib(ws_geometry_type1, Point, Rect)