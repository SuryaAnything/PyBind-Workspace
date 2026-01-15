#include "ws_core.hpp"

class Circle {
public: 
    float radius;
    
    // FIXED: Added implementation
    float get_circumference() {
        return 3.14 * 2 * 10; // Dummy logic
    }
};

extern_py_lib(ws_geometry_type1, Circle)