# Constants used when drawing gates in ascii visualization
PLUS2_ASCII =       ["  +----+  ",
                     "--| +2 |--",
                     "  +----+  "]
PLUS1_ASCII =       ["  +----+  ",
                     "--| +1 |--",
                     "  +----+  "]
ID_ASCII =          ["  +----+  ",
                     "--| ID |--",
                     "  +----+  "]
ONE_TWO_ASCII =     ["  +----+  ",
                     "--| 12 |--",
                     "  +----+  "]
ZERO_TWO_ASCII =    ["  +----+  ",
                     "--| 02 |--",
                     "  +----+  "]
ZERO_ONE_ASCII =    ["  +----+  ",
                     "--| 01 |--",
                     "  +----+  "]
CONTROL_ASCII =     ["          ",
                     "----O-----",
                     "    |     "]
CONTROL_ASCII_REV = ["    |     ",
                     "----O-----",
                     "          "]
WIRE_ASCII =        ["          ",
                     "----------",
                     "          "]
LINE_ASCII =        ["    |     ",
                     "----|-----", 
                     "    |     "]
BARRIER_ASCII =     ["    ||    ",
                     "----||----", 
                     "    ||    "]
def custom_ascii(name): # Function that generates the ascii representation of a custom gate 
    return ["  +----+  ",f"--|{name:^4}|--","  +----+  "]
