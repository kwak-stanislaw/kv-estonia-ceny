"""
pdb

alternatively: pdbp, pdbpp(colors), ipdb

Navigation
| Command         | Shortcut | Description |
| `next`          |   `n`    |   Execute the current line; step **over** function calls |
| `step`.         |   `s`    |   Execute the current line; step **into** function calls |
| `return`        |   `r`    |   Continue until the current function returns |
| `continue`      |   `c`    |   Resume execution until the next breakpoint |
| `until [line]`  |   `unt`  | Run until a specific line number (or past a loop) |
| `jump <line>`   |   `j`    |   Jump to a specific line (skip or repeat code) |
| `quit`          |   `q`    |   Exit the debugger and terminate the program |
| `where`         |   `w`    |   Print the call stack (traceback) |
| `up`            |   `u`    |   Move up one level in the call stack |
| `down`          |   `d`    |   Move down one level in the call stack |

Inspection
| Command          | Shortcut |  Description |
| `list`           |   `l`    |  Show source code around the current line |
| `list .`         |   `l .   |  Show source code at current position (reset view) |
| `longlist`       |   `ll`   |  Show the entire current function's source |
| `print <expr>`.  |   `p`    |  Evaluate and print an expression |
| `pretty print`   |   `pp`   |  Pretty-print a complex object (dicts, lists) |
| `whatis <expr>`  |    —     |  Print the type of an expression |
| `args`           |   `a`    |  Print the arguments of the current function |
| `display <expr>` |    —     |  Auto-display expression every time execution stops |
| `undisplay`      |    —     |  Remove a display expression |


"""


# import pdb

rang = 5
# try to change rang value
breakpoint() # pdb.set_trace()


for i in range(rang): # try display "i"
    print(i) # try skip only this loop

i = 5 # try go to line 34

print(i*2)

def func1(x,y,z):
    def func2(x,y,z):
        def func3(x,y,z):
            def func4(x,y,z):
                def func5(x,y,z):
                    def func6(x,y,z):
                        func_val = x+y**z
                        return func_val
                    return func6(x,y,z)
                return func5(x,y,z)
            return func4(x,y,z)
        return func3(x,y,z)
    return func2(x,y,z)


val = func1(5, z=2, y= 1) # try go to func6 in call stack, and run "where", "l", "args"


print(val)



def long_func():
    x = 1
    x += 2
    x += 1
    x += 1
    x += 2
    x += 1
    x += 2
    x += 1
    x += 1
    x += 2
    x += 1
    x += 3
    x += 1
    x += 1 # p x
    x += 1
    x += 1
    x += 1
    x += 1
    x += 3
    return x
x = long_func()
print(x)


import json

data = json.loads("""{"a":1}""")
print(data)
