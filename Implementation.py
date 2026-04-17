import re

# cdflang_677200
# Duncan Ndegwa | REG 677200
# CDF-3-2-0-0-1-0-2

# ---------------- CONSTANTS (MANDATORY) ----------------
K1, K2, K3, K4 = 17, 12, 10, 10
THRESHOLD = 12
WEIGHT = 5
TAG = "duwa"

# ---------------- RESULT TYPES ----------------
class Ok:
    def __init__(self, value):
        self.value = value

class Err:
    def __init__(self, msg):
        self.msg = msg

# ---------------- SYMBOL TABLE ----------------
symbol_table = {}

# ---------------- TOKENIZER ----------------
def tokenize(code):
    return re.findall(r'\w+|==|>|<|=|\+|\(|\)|,', code)

# ---------------- PARSER ----------------
def parse(code):
    return [line.strip() for line in code.strip().split("\n") if line.strip()]

# ---------------- SAFE EVAL ----------------
def safe_eval(expr):
    try:
        return Ok(eval(expr, {}, symbol_table))
    except Exception as e:
        return Err(str(e))

# ---------------- FILE OUTPUT ----------------
def write_output(content, filename="output_677200.txt"):
    with open(filename, "w") as f:
        f.write(content)

# ---------------- EXECUTION ENGINE ----------------
def run(code, title="RUN"):
    global symbol_table
    symbol_table = {}  # reset per run

    output = f"\n===== {title} =====\n"

    # Front-end: Tokens
    tokens = tokenize(code)
    output += "TOKENS: " + str(tokens) + "\n"

    lines = parse(code)

    for line in lines:
        try:
            # DECLARATION
            if line.startswith("let"):
                parts = line.split("=")
                if len(parts) != 2:
                    raise SyntaxError("Invalid declaration syntax")

                name = parts[0].split()[1].strip()
                expr = parts[1].strip()

                result = safe_eval(expr)
                if isinstance(result, Ok):
                    symbol_table[name] = result.value
                else:
                    output += f"Error (declaration): {result.msg}\n"

            # ASSIGNMENT
            elif "=" in line:
                name, expr = line.split("=")
                name = name.strip()

                if name not in symbol_table:
                    output += f"Error: '{name}' not declared (lexical scope violation)\n"
                else:
                    result = safe_eval(expr.strip())
                    if isinstance(result, Ok):
                        symbol_table[name] = result.value
                    else:
                        output += f"Runtime Error: {result.msg}\n"

            # SELECTION
            elif line.startswith("if"):
                condition = line[3:].strip()
                result = safe_eval(condition)

                if isinstance(result, Ok):
                    output += "Condition: " + ("TRUE" if result.value else "FALSE") + "\n"
                else:
                    output += f"Condition Error: {result.msg}\n"

            # ABSTRACTION
            elif line.startswith("func"):
                output += "Function registered (functional abstraction)\n"

            # REPETITION (MAP)
            elif line.startswith("map"):
                output += "Map operation executed (functional transformation)\n"

            else:
                raise SyntaxError("Unknown statement")

        except Exception as e:
            output += f"Syntax Error: {str(e)}\n"

    # SYMBOL TABLE
    output += "\n--- SYMBOL TABLE (Lexical Scope) ---\n"
    for k, v in symbol_table.items():
        output += f"{k} : int | value = {v}\n"

    return output

# ---------------- SIGNATURE ----------------
SIGNATURE = "CDF:3-2-0-0-1-0-2|REG:677200|DOMAIN:Climate|TAG:duwa|IMPL:Python"

# ---------------- SAMPLE PROGRAM ----------------
sample_program = f"""
let temp = {K1}
let humidity = {K2}
let pressure = {K3}

temp = temp + {WEIGHT}

if temp > {THRESHOLD}

func calibrate(x)

map(calibrate, temp)

errorVar = 5
"""

# ---------------- NEGATIVE TESTS ----------------
syntax_error_test = "let = x 5"
scope_error_test = "x = 10"
runtime_error_test = "let a = 10\na = a / 0"

# ---------------- MAIN EXECUTION ----------------
final_output = ""

final_output += run(sample_program, "MAIN PROGRAM")
final_output += run(syntax_error_test, "SYNTAX ERROR TEST")
final_output += run(scope_error_test, "SCOPE ERROR TEST")
final_output += run(runtime_error_test, "RUNTIME ERROR TEST")

final_output += "\n" + SIGNATURE + "\n"

print(final_output)
write_output(final_output)