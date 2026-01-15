import re

# C++ Keywords that usually appear at the end of a type
# If the last word is one of these, we assume it's part of the type, not a variable name.
CPP_KEYWORDS = {
    "int", "char", "bool", "float", "double", "void", "wchar_t", 
    "long", "short", "unsigned", "signed", "const", "auto", 
    "size_t", "int8_t", "int16_t", "int32_t", "int64_t",
    "uint8_t", "uint16_t", "uint32_t", "uint64_t"
}

def split_args(raw_args):
    """
    Splits arguments by comma, but ignores commas inside <...>.
    Example: "int x, std::map<int, int> m" -> ["int x", "std::map<int, int> m"]
    """
    args = []
    current = []
    angle_depth = 0
    
    for char in raw_args:
        if char == '<': angle_depth += 1
        elif char == '>': angle_depth -= 1
        
        if char == ',' and angle_depth == 0:
            args.append("".join(current).strip())
            current = []
        else:
            current.append(char)
            
    if current:
        args.append("".join(current).strip())
        
    return [a for a in args if a]

def clean_type(token):
    """
    Heuristic to extract TYPE from "Type VariableName".
    Examples:
      "int x"          -> "int"
      "const int* p"   -> "const int*"
      "long long"      -> "long long"  (Keyword protection)
      "std::string"    -> "std::string"
    """
    # 1. Remove default values (e.g. = 10)
    token = token.split('=')[0].strip()
    
    # 2. Find the last word in the string
    # Regex finds the last alphanumeric sequence
    match = re.search(r'(\s+)([\w_]+)$', token)
    
    # If no separate last word (e.g. "int*"), it's just a type.
    if not match:
        return token

    separator = match.group(1)
    last_word = match.group(2)
    
    # 3. Keyword Guard
    # If the last word is a known C++ type keyword (like 'long', 'int'), 
    # assume the user wrote a type only (e.g. "unsigned int"). Keep it.
    if last_word in CPP_KEYWORDS:
        return token

    # 4. Strip the Variable Name
    # If it's not a keyword, assume it's a variable name (e.g. "msg", "x", "count")
    # We remove the separator and the word.
    return token[:match.start()].strip()

def extract_methods(content, class_name):
    struct_info = { "constructors": [], "methods": [] }

    # --- 1. Extract Class Body ---
    start_pattern = re.compile(f'class\\s+{class_name}\\s*{{')
    match = start_pattern.search(content)
    if not match: return struct_info

    body_start = match.end()
    brace_count = 1
    class_body = ""
    for char in content[body_start:]:
        if char == '{': brace_count += 1
        elif char == '}': brace_count -= 1
        if brace_count == 0: break
        class_body += char

    # --- 2. Isolate Public Sections ---
    public_code = ""
    is_public = False
    # Use regex split to safely find visibility blocks
    tokens = re.split(r'(public:|protected:|private:)', class_body)
    for token in tokens:
        if token == 'public:': is_public = True
        elif token == 'private:': is_public = False
        elif token == 'protected:': is_public = False
        elif is_public:
            public_code += token + "\n"

    # --- 3. Clean up Initializer Lists ---
    # Removes ": x(10), y(20) {" -> replaces with "{"
    public_code = re.sub(r'\)\s*:[^{]*{', '){', public_code)

    # --- 4. Parse Constructors ---
    # Matches: ClassName ( ... )
    ctor_pattern = re.compile(rf'\b{class_name}\s*\((.*?)\)')
    
    for match in ctor_pattern.finditer(public_code):
        raw_args = match.group(1).strip()
        arg_types = []
        
        if raw_args:
            # Use our Smart Splitter
            for token in split_args(raw_args):
                clean = clean_type(token)
                arg_types.append(clean)
        
        struct_info["constructors"].append(arg_types)

    # --- 5. Parse Methods ---
    # Matches: [static] Type Name ( ... )
    method_pattern = re.compile(r'\s*(static\s+)?([a-zA-Z0-9_<>:\*&]+)\s+(\w+)\s*\(')
    
    for match in method_pattern.finditer(public_code):
        is_static = True if match.group(1) else False
        func_name = match.group(3).strip()
        
        # Skip constructors/destructors
        if func_name == class_name or func_name.startswith('~'): continue
        if func_name in ['if', 'while', 'for', 'switch']: continue

        struct_info["methods"].append({ 'name': func_name, 'is_static': is_static })

    return struct_info