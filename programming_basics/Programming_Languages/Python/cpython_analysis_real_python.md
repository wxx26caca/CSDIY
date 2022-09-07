# Your Guide to the CPython Source Code

## Part 1: Introduction to CPython

runtimes: CPython, PyPy, Cython, Jython...

CPython contains both a **runtime** and **shared language specification** that all Python runtimes use.

Python language specification is the document that description of the Python language.

### cpython subdirectories

```
cpython/
|
|--- Doc		<- Source for the documentation
|--- Grammar	<- The computer-readable language definition
|--- Include	<- The C header files
|--- Lib		<- Standard library modules written in Python
|--- Mac		<- macOS support files
|--- Misc		<- Miscellaneous files
|--- Modules	<- Standard library modules written in C
|--- Objects	<- Core types and the object model
|--- Parser		<- The Python parser source code
|--- PC			<- Windows build support files
|--- PCbuild	<- Windows build support files for older Windows versions
|--- Programs	<- Source code for the python executable and other binaries
|--- Python		<- The CPython interpreter source code
|--- Tools		<- Standalone tools useful for building or extending Python
```

Focus on these subdirectories when analyzing CPython source code:

```
Include	<- The C header files
Lib		<- Standard library modules written in Python
Modules	<- Standard library modules written in C
Objects	<- Core types and the object model
```

```
## Python parser and interpreter
Parser		<- The Python parser source code
Programs	<- Source code for the python executable and other binaries
Python		<- The CPython interpreter source code
```

Compiling CPython (macOS, Linux, Windows)

The purpose of a compiler is to **convert one language into another**. Internally, the CPython runtime does compile your code.

Python code is not compiled into machine-code. It is compiled into a special low-level intermediary language called **bytecode** that only CPython understands. This code is stored in `.pyc` files in a hidden directory and **cached for execution**. (If you run the same Python application twice without changing the source code, it'll always be much faster the second time.)

### Why is CPython written in C and not Python?

There are two types of compiler:

- **Self-hosted compilers** are compilers written in the language they compile, such as Go compiler.
- **Source-to-source compilers** are compilers written in another language that already have a compiler.

CPython kept its C heritage: many of the standard library modules, like the `ssl` module or the `sockets` module, are written in C to access low-level operating system APIs. The APIs in the Windows and Linux kernels for [creating network sockets](https://realpython.com/python-sockets/), [working with the filesystem](https://realpython.com/working-with-files-in-python/) or [interacting with the display](https://realpython.com/python-gui-with-wxpython/) are all written in C. It made sense for Python’s extensibility layer to be focused on the C language. 

self-hosted (自托管的)

### Documentation

Located inside the `Doc/reference` directory are reStructuredText explanations of each of the features in the Python language.

```
cpython/Doc/reference
|
├── compound_stmts.rst
├── datamodel.rst
├── executionmodel.rst
├── expressions.rst
├── grammar.rst
├── import.rst
├── index.rst
├── introduction.rst
├── lexical_analysis.rst
├── simple_stmts.rst
└── toplevel_components.rst
```

Inside `compound_stmts.rst` the documentation for compound statements (复合语句), you can see a simple exampled defining the `with` statement.

For example:

```python
with x():
    pass

with x() as y:
    pass

with x() as y, z() as k:
    pass
```

### Grammar

The Grammar file is written in a context-notation called `Backus-Naur Form (BNF)`.

Python's grammar file uses the Extended-BNF (EBNF) specification with regular expression syntax.

- `*` for repetition
- `+` for at-least-one repetition
- `[]` for optional parts
- `|` for alternatives
- `()` for grouping

A parser table created by a tool called `pgen` is used. `pgen` reads the grammar file and converts it into a parser table. If you make changes to the grammar file, you must regenerate the parser table and recompile Python.

Modify the `Grammar` file and run `make regen-grammar` to run `pgen` over the altered grammar file. You should see an output similar to this, showing that the new `Include/graminit.h` and `Python/graminit.c` files have been generated.

If the code compiled successfully, you can execute your new CPython binary and start a REPL.

[story about pgen parser and the new PEG parser from Guido van Rossum](https://medium.com/@gvanrossum_83706/peg-parsers-7ed72462f97c)

### Tokens

The `Tokens` file contains **each of the unique types found as a leaf node in a parse tree**. Each token also has a name and a generated unique ID. The names are used to make it simpler to refer to in the tokenizer.

To see tokens in action, you can use the `tokenize` module in CPython. located in `Lib/tokenize.py`.

- Create a simple Python script called `test_tokens.py`

    ```python
    # Hello world
    def my_function():
        pass
    ```

- execute below command

    ```shell
    python3 -m tokenize -e test_tokens.py
    ```

- output likes below

    ```
    0,0-0,0:            ENCODING       'utf-8'
    1,0-1,13:           COMMENT        '# Hello world'
    1,13-1,14:          NL             '\n'
    2,0-2,3:            NAME           'def'
    2,4-2,15:           NAME           'my_function'
    2,15-2,16:          LPAR           '('
    2,16-2,17:          RPAR           ')'
    2,17-2,18:          COLON          ':'
    2,18-2,19:          NEWLINE        '\n'
    3,0-3,4:            INDENT         '    '
    3,4-3,8:            NAME           'pass'
    3,8-3,9:            NEWLINE        '\n'
    4,0-4,0:            DEDENT         ''
    4,0-4,0:            ENDMARKER      ''
    ```

    The `ENCODING` token for `utf-8`, and a blank line at the end, giving `DEDENT` to close the function declaration and an `ENDMARKER` to end the file.

**It is best practice to have a blank line at the end of your Python source files**. If you omit it, CPython adds it for you, with a tiny performance penalty.

```
There are two tokenizers in the CPython source code: one written in Python, demonstrated here, and another written in C. 
The tokenizer written in Python is meant as a utility, and the one written in C is used by the Python compiler. 
They have identical output and behavior. The version written in C is designed for performance and the module in Python is designed for debugging.
```

### Memory Management in CPython

`PyArena` object. The code is within `Python/pyarena.c` and contains a wrapper around C's memory allocation and deallocation functions.

Python uses two algorithms: **a reference counter and a garbage collector**.

Whenever an interpreter is instantiated, a `PyArena` is created and attached one of the fields in the interpreter. 

During the lifecycle of a CPython interpreter, many arenas could be allocated, and they are connected with a `linked list`.

Whenever a new Python object is created, a pointer to it is added using `PyArena_AddPyObject()`, this function call stores a pointer in the arena's list.

`PyArena` serves a second function, which is to **allocate and reference a list of raw memory blocks**. For example, `PyArena_Malloc()` for malloc memory.

When an interpreter is stopped, all managed memory blocks can be deallocated in one go using `PyArena_Free()`.

- Allocation of a row memory blocks is done via `PyMem_RawAlloc()`
- The pointers to Python objects are stored within the `PyArena`
- `PyArena` also stores a linked-list of allocated memory blocks

`Py_INCREF()` and `Py_DECREF()` increment and decrement the count of references to that object.

Whenever `Py_DECREF()` is called, and the counter becomes 0, the `PyObject_Free()` function is called. `PyArena_Free()` is called for all of the memory that was allocated.

The garbage collection algorithm is a lot more complex than the reference counter, it doesn't happen all the time. It happens periodically, after a set number of operations.

`gc` module for garbage collector.

```
>>> import gc
>>> gc.get_threshold()
(700, 10, 10)
>>> gc.get_count()
(126, 4, 1)
>>> gc.collect()
0
```

`collect()` inside the `Modules/gcmodule.c` file which contains the implementation of the garbage collector algorithm.

## Part 2: The Python Interpreter Process

### Establishing Runtime Configuration

Five ways the `python` binary can be called:

- To run a single command with `-c` and a Python command
- To start a module with `-m` and the name of a module
- To run a file with the filename
- To run the `stdin` input using a shell pipe
- To start the REPL and execute commands one at a time

Three source files you need to inspect to see this process are:

- `Programs/python.c` is a simple entry point

- `Modules/main.c` contains the code to bring together the whole process, loading configuration, executing code and clearing up memory.

- `Python/initconfig.c` loads the configuration from the system environment and merges it with any command-line flags.

    below diagram shows how each of those functions is called:

    ![](https://files.realpython.com/media/swim-lanes-chart-1.9fb3000aad85.png)

There is an official style guide for CPython C code, [PEP 7 - Style Guide for C Code](https://peps.python.org/pep-0007/), and some naming standards which help when navigating the source code:

- **Use a `Py` prefix for public functions**, never for static functions. `Py_` for global service routines like `Py_FatalError`, `PyString_` for string functions.
- **Public functions and variables use MixedCase with underscores**, like: `PyObject_GetAttr`, `Py_BuildValue`
- Occasionally an 'internal' function has to be visible to the loader. Use `_Py` prefix, like, `_PyObject_Dump`
- **Macros should have a MixedCase prefix and then use upper case**, for example `PyString_AS_STRING`

The configuration of the runtime is a data structure defined in `Include/cpython/initconfig.h` named `PyConfig` used by the **CPython runtime to enable and disable various features**. Includes things like:

- **Runtime flags** for various modes like debug and optimized mode
- **Execution mode**, such as whether a filename was passed, `stdin` was provided or a module name
- **Extended option**, specified by `-X <option>`
- **Environment variables** for runtime settings

Python will print messages to the screen when modules are loaded use `-v` flag.

```
$ python3 -v -c "print('HELLO WORLD')"
import _frozen_importlib # frozen
import _imp # builtin
import sys # builtin
import '_warnings' # <class '_frozen_importlib.BuiltinImporter'>
import '_thread' # <class '_frozen_importlib.BuiltinImporter'>
import '_weakref' # <class '_frozen_importlib.BuiltinImporter'>
import '_frozen_importlib_external' # <class '_frozen_importlib.FrozenImporter'>
import '_io' # <class '_frozen_importlib.BuiltinImporter'>
import 'marshal' # <class '_frozen_importlib.BuiltinImporter'>
import 'posix' # <class '_frozen_importlib.BuiltinImporter'>
import _thread # previously loaded ('_thread')
import '_thread' # <class '_frozen_importlib.BuiltinImporter'>
import _weakref # previously loaded ('_weakref')
import '_weakref' # <class '_frozen_importlib.BuiltinImporter'>
# installing zipimport hook
import 'zipimport' # <class '_frozen_importlib.BuiltinImporter'>
# installed zipimport hook
...
Python 3.6.9 (default, Jan 26 2021, 15:33:00)
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
HELLO WORLD
# clear builtins._
# clear sys.path
# clear sys.argv
...
```

In `Python/initconfig.c`, the logic for reading settings from environment variables and runtime command-line flags is established.

Within a Python session, you can access the runtime flags, like verbose mode, quiet mode, using the `sys.flags` named tuple. The `-X` flags are all available inside the `sys._xoptions` dictionary

```
$ python3 -X dev -q
>>> import sys
>>> sys.flags
sys.flags(debug=0, inspect=0, interactive=0, optimize=0, dont_write_bytecode=0, no_user_site=0, no_site=0, ignore_environment=0, verbose=0, bytes_warning=0, quiet=1, hash_randomization=1, isolated=0)
>>> sys._xoptions
{'dev': True}
```

There is also the build configuration, which is located inside `pyconfig.h` in the root folder. This file is created dynamically in the `configure` step in the build process, or by Visual Studio for Windows.

You can see the build configuration by running

```
$ python3 -m sysconfig
```

### Reading Files/Input

Once CPython has the **runtime configuration** and the **command-line arguments**, it can establish what it needs to execute.

This task is handled by the `pymain_main` function inside `Modules/main.c`.

#### Input via -c

```
python3 -c "print("Hi")"
```

Below is the full flowchart of how this happens:

![](https://files.realpython.com/media/pymain_run_command.f5da561ba7d5.png)

```c
static int
pymain_run_command(wchar_t *command, PyCompilerFlags *cf)
{
    PyObject *unicode, *bytes;
    int ret;

    unicode = PyUnicode_FromWideChar(command, -1);
    if (unicode == NULL) {
        goto error;
    }

    if (PySys_Audit("cpython.run_command", "O", unicode) < 0) {
        return pymain_exit_err_print();
    }

    bytes = PyUnicode_AsUTF8String(unicode);
    Py_DECREF(unicode);
    if (bytes == NULL) {
        goto error;
    }

    ret = PyRun_SimpleStringFlags(PyBytes_AsString(bytes), cf);
    Py_DECREF(bytes);
    return (ret != 0);

error:
    PySys_WriteStderr("Unable to decode the command from the command line:\n");
    return pymain_exit_err_print();
}
```

- The `pymain_run_command()` function is executed inside `Modules/main.c` taking the command passed in `-c` as an argument in the C type `wchar_t *`.

- Convert `wchar_t` to unicode, bytes, and then a string. Equivalent to the following:

    ```
    unicode = str(command)
    bytes_ = bytes(unicode.encode('utf-8'))
    ```

- The `PyRun_SimpleStringFlags()` function is part of `Python/pythonrun.c`. It's purpose is to turn this simple command into Python module and the send it on to be executed.

    ```c
    int
    PyRun_SimpleStringFlags(const char *command, PyCompilerFlags *flags)
    {
        PyObject *m, *d, *v;
        m = PyImport_AddModule("__main__");
        if (m == NULL)
            return -1;
        d = PyModule_GetDict(m);
        v = PyRun_StringFlags(command, Py_file_input, d, d, flags);
        if (v == NULL) {
            PyErr_Print();
            return -1;
        }
        Py_DECREF(v);
        return 0;
    }
    ```

- Once `PyRun_SimpleStringFlags()` has created a module and a dictionary, it calls `PyRun_StringFlags()`, which creates a fake filename and the calls the Python parser to create an AST from the string and return a module

    ```c
    PyObject *
    PyRun_StringFlags(const char *str, int start, PyObject *globals,
                      PyObject *locals, PyCompilerFlags *flags)
    {
        PyObject *ret = NULL;
        mod_ty mod;
        PyArena *arena;
        PyObject *filename;
    
        filename = _PyUnicode_FromId(&PyId_string); /* borrowed */
        if (filename == NULL)
            return NULL;
    
        arena = PyArena_New();
        if (arena == NULL)
            return NULL;
    
        mod = PyParser_ASTFromStringObject(str, filename, start, flags, arena);
        if (mod != NULL)
            ret = run_mod(mod, filename, globals, locals, flags, arena);
        PyArena_Free(arena);
        return ret;
    }
    ```

#### Input via -m

The `-m` flag implies that within the module package, you want to execute whatever is inside `__main__`. It also implies that you want to search `sys.path` for the named module. That is why you don't need to remember where the module located in your filesystem.

This task is handled by `pymain_run_module` inside `Modules/main.c`.

```c
static int
pymain_run_module(const wchar_t *modname, int set_argv0)
{
    PyObject *module, *runpy, *runmodule, *runargs, *result;
    if (PySys_Audit("cpython.run_module", "u", modname) < 0) {
        return pymain_exit_err_print();
    }
    runpy = PyImport_ImportModule("runpy");
    if (runpy == NULL) {
        fprintf(stderr, "Could not import runpy module\n");
        return pymain_exit_err_print();
    }
    runmodule = PyObject_GetAttrString(runpy, "_run_module_as_main");
    if (runmodule == NULL) {
        fprintf(stderr, "Could not access runpy._run_module_as_main\n");
        Py_DECREF(runpy);
        return pymain_exit_err_print();
    }
    module = PyUnicode_FromWideChar(modname, wcslen(modname));
    if (module == NULL) {
        fprintf(stderr, "Could not convert module name to unicode\n");
        Py_DECREF(runpy);
        Py_DECREF(runmodule);
        return pymain_exit_err_print();
    }
    runargs = Py_BuildValue("(Oi)", module, set_argv0);
    if (runargs == NULL) {
        fprintf(stderr,
            "Could not create arguments for runpy._run_module_as_main\n");
        Py_DECREF(runpy);
        Py_DECREF(runmodule);
        Py_DECREF(module);
        return pymain_exit_err_print();
    }
    _Py_UnhandledKeyboardInterrupt = 0;
    result = PyObject_Call(runmodule, runargs, NULL);
    if (!result && PyErr_Occurred() == PyExc_KeyboardInterrupt) {
        _Py_UnhandledKeyboardInterrupt = 1;
    }
    Py_DECREF(runpy);
    Py_DECREF(runmodule);
    Py_DECREF(module);
    Py_DECREF(runargs);
    if (result == NULL) {
        return pymain_exit_err_print();
    }
    Py_DECREF(result);
    return 0;
}
```

The name of the module is passed as the `modname` argument.

- First, CPython import a standard library module, `runpy` using the C API function `PyImport_ImportModule()` which is located in `Python/import.c` file.

    Because `PyImport_ImportModule()` returns a `PyObject*` the core object type, you need to call special functions to get attributes and to call it.

    ```c
    PyObject *
    PyImport_ImportModule(const char *name)
    {
        PyObject *pname;
        PyObject *result;
    
        pname = PyUnicode_FromString(name);
        if (pname == NULL)
            return NULL;
        result = PyImport_Import(pname);
        Py_DECREF(pname);
        return result;
    }
    ```

- Then, using a function call `PyObject_GetAttrString()` which is found in `Objects/object.c`. Finally, it returns `tp->tp_getattro`, which is the attribute of the python object. The same with call `getattr()` in Python.

- Next, check module name and arguments using `PyUnicode_FromWideChar()` and `Py_BuildValue()`

- Final, calls `PyObject_Call()`

If you wanted to run a callable, you would give it parentheses, or you can run the `__call__()` property on any Python object. The `__call__()` method is implemented inside `Objects/object.c`

```
hi = "HI"
hi.upper() == hi.upper.__call__()
```

Through analysis the source code, we can see that execute `python -m <module>` is equivalent to run `python -m runpy <module>`.

`runpy` module is written in pure Python and located in `Lib/runpy.py`.

`runpy` module was created to **abstract the process of locating and executing modules** on an operating system.

`runpy` does a few things to run the target module:

- Calls `__import__()` for the module name you provided
- Sets `__name__()` to a namespace called `__main__`
- Executes the module within the `__main__` namespace

#### Input via Filename

If the first argument to `python` was a filename, such as `python test.py`, then CPython will call `pymain_run_file()` inside `Modules/main.c`. And it will open a file handle, pass the handle to `PyRun_SimpleFileExFlags()` inside `Python/pythonrun.c`.

`PyRun_SimpleFileExFlags()` calls `pyrun_simple_file` which is also found in `Python/pythonrun.c`.

Function `pyrun_simple_file` logic:

- If the file path is a `.pyc` file, it will call `run_pyc_file()`
- If the file path is a script file `.py` it will run `pyrun_file()`

#### Input via File with PyRun_FileExFlags()



#### Input via Compiled Bytecode with run_pyc_file()

The `run_pyc_file()` function inside `Python/pythonrun.c` then marshals (编组) the code object from the `.pyc` file by using the file handle. **Marshaling** is a technical term for **copying the contents of a file into memory and converting them to a specific data structure**.

Once the code object has been marshaled to memory, it is sent to `run_eval_code_obj()`, which calls `Python/ceval.c` to execute the code.

### Lexing and Parsing

Lexing and Parsing (词法分析和解析)

Focus on function `PyParser_ASTFromFileObject()` located in `Python/pythonrun.c` .

```c
mod_ty
PyParser_ASTFromFileObject(FILE *fp, PyObject *filename, const char* enc,
                           int start, const char *ps1,
                           const char *ps2, PyCompilerFlags *flags, int *errcode,
                           PyArena *arena)
{
    mod_ty mod;
    PyCompilerFlags localflags = _PyCompilerFlags_INIT;
    perrdetail err;
    int iflags = PARSER_FLAGS(flags);

    node *n = PyParser_ParseFileObject(fp, filename, enc,
                                       &_PyParser_Grammar,
                                       start, ps1, ps2, &err, &iflags);
    if (flags == NULL) {
        flags = &localflags;
    }
    if (n) {
        flags->cf_flags |= iflags & PyCF_MASK;
        mod = PyAST_FromNodeObject(n, flags, filename, arena);
        PyNode_Free(n);
    }
    else {
        err_input(&err);
        if (errcode)
            *errcode = err.error;
        mod = NULL;
    }
    err_free(&err);
    return mod;
}
```

The `PyParser_ASTFromFileObject()` function will take a file handle, compiler flags and a `PyArena` instance and convert the file object into a node object using `PyParser_ParseFileObject()`.

The `PyParser_ParseFileObject()` inside `Parser/parsetok.c` has two import tasks

```c
node *
PyParser_ParseFileObject(FILE *fp, PyObject *filename,
                         const char *enc, grammar *g, int start,
                         const char *ps1, const char *ps2,
                         perrdetail *err_ret, int *flags)
{
    struct tok_state *tok;

    if (initerr(err_ret, filename) < 0)
        return NULL;

    if (PySys_Audit("compile", "OO", Py_None, err_ret->filename) < 0) {
        return NULL;
    }

    if ((tok = PyTokenizer_FromFile(fp, enc, ps1, ps2)) == NULL) {
        err_ret->error = E_NOMEM;
        return NULL;
    }
    if (*flags & PyPARSE_TYPE_COMMENTS) {
        tok->type_comments = 1;
    }
    Py_INCREF(err_ret->filename);
    tok->filename = err_ret->filename;
    return parsetok(tok, g, start, err_ret, flags);
}
```

- Instantiate a tokenizer state `tok_state` using `PyTokenizer_FromFile()` in `Parser/tokenizer.c`
- Convert the tokens into a concrete parse tree using `parsetok()` in `Parser/parsetok.c`

`tok_state` is a data structure (defined in `Parser/tokenizer.h`) to store all temporary data generated by tokenizer.

Inside `parsetok()`, it will use the `tok_state` structure and make calls to `tok_get()` in a loop until the file is exhausted and no more tokens can be found.

`tok_get()` defined in `Parser/tokenizer.c` behaves like an iterator. It will keep returning the next token in the parse tree.

The `node` type returned by `PyParser_ParseFileObject()` is going to be essential for the next stage, converting a parse tree into an Abstract-Syntax-Tree (AST).

CPython has a standard library module `parser`, which exposes the C functions with a Python API.

```
>>> import parser
>>> from pprint import pprint
>>> st = parser.expr('a+1')
>>> pprint(parser.st2list(st))
[258,
 [331,
  [305,
   [309,
    [310,
     [311,
      [312,
       [315,
        [316,
         [317,
          [318,
           [319,
            [320, [321, [322, [323, [324, [1, 'a']]]]]],
            [14, '+'],
            [320, [321, [322, [323, [324, [2, '1']]]]]]]]]]]]]]]]],
 [4, ''],
 [0, '']]
```

### Abstract Syntax Trees

ASTs are produced inline with the CPython interpreter process, but you can also generate them in both Python using `ast` module in the standard library as well as through the C API.

Install a simple app called `instaviz` to display the AST and bytecode instructions in a Web UI.

```
pip install instaviz
pip install pyreadline
```

```
>>> import instaviz
>>> def example():
...     a = 1
...     b = a + 1
...     return b
...
>>> instaviz.show(example)
Bottle v0.12.19 server starting up (using WSGIRefServer())...
Listening on http://localhost:8080/
Hit Ctrl-C to quit.
```

Jumping then into `PyAST_FromNodeObject()` inside `Python/ast.c`, you can see it receives the `node *` tree, the filename, compiler flags, and the `PyArena`.

The return type `mod_ty` defined in `Include/Python-ast.h`.

```c
typedef struct _mod *mod_ty;

enum _mod_kind {Module_kind=1, Interactive_kind=2, Expression_kind=3,
                 FunctionType_kind=4, Suite_kind=5};
struct _mod {
    enum _mod_kind kind;
    union {
        struct {
            asdl_seq *body;
            asdl_seq *type_ignores;
        } Module;

        struct {
            asdl_seq *body;
        } Interactive;

        struct {
            expr_ty body;
        } Expression;

        struct {
            asdl_seq *argtypes;
            expr_ty returns;
        } FunctionType;

        struct {
            asdl_seq *body;
        } Suite;

    } v;
};
```

...

### Conclusion

This part shows how the CPython interperter takes an input, such as a file or string, and converts it into a logical AST.

## Part 3: The CPython Compiler and Execution Loop

Go deeper to convert the ATS into a set of sequential commands that CPU can understand.

### Compiling

This compilation task is split into 2 parts:

- **Traverse the tree** and **create a control-flow-graph (CFG)** which represents the logical sequence for execution
- **Convert the nodes** in CFG to smaller, executable statements. known as **byte-code**

In part2, we were looking at how files are executed, the resulting module from the call to is sent to `run_mod()` still in `Python/pythonrun.c`.

```c
static PyObject *
run_mod(mod_ty mod, PyObject *filename, PyObject *globals, PyObject *locals,
            PyCompilerFlags *flags, PyArena *arena)
{
    PyCodeObject *co;
    PyObject *v;
    co = PyAST_CompileObject(mod, filename, flags, -1, arena);
    if (co == NULL)
        return NULL;

    if (PySys_Audit("exec", "O", co) < 0) {
        Py_DECREF(co);
        return NULL;
    }

    v = run_eval_code_obj(co, globals, locals);
    Py_DECREF(co);
    return v;
}
```

Continue tracking the code flow, it will call `run_eval_code_obj()` in `Python/pythonrun.c`.

Detail of function`PyAST_CompileObject()` found in `Python/compile.c`.

```c
PyCodeObject *
PyAST_CompileObject(mod_ty mod, PyObject *filename, PyCompilerFlags *flags,
                   int optimize, PyArena *arena)
{
    struct compiler c;
    PyCodeObject *co = NULL;
    PyCompilerFlags local_flags = _PyCompilerFlags_INIT;
    int merged;
    PyConfig *config = &_PyInterpreterState_GET_UNSAFE()->config;

    if (!__doc__) {
        __doc__ = PyUnicode_InternFromString("__doc__");
        if (!__doc__)
            return NULL;
    }
    if (!__annotations__) {
        __annotations__ = PyUnicode_InternFromString("__annotations__");
        if (!__annotations__)
            return NULL;
    }
    if (!compiler_init(&c))
        return NULL;
    Py_INCREF(filename);
    c.c_filename = filename;
    c.c_arena = arena;
    c.c_future = PyFuture_FromASTObject(mod, filename);
    if (c.c_future == NULL)
        goto finally;
    if (!flags) {
        flags = &local_flags;
    }
    merged = c.c_future->ff_features | flags->cf_flags;
    c.c_future->ff_features = merged;
    flags->cf_flags = merged;
    c.c_flags = flags;
    c.c_optimize = (optimize == -1) ? config->optimization_level : optimize;
    c.c_nestlevel = 0;
    c.c_do_not_emit_bytecode = 0;

    if (!_PyAST_Optimize(mod, arena, c.c_optimize)) {
        goto finally;
    }

    c.c_st = PySymtable_BuildObject(mod, filename, c.c_future);
    if (c.c_st == NULL) {
        if (!PyErr_Occurred())
            PyErr_SetString(PyExc_SystemError, "no symtable");
        goto finally;
    }

    co = compiler_mod(&c, mod);

 finally:
    compiler_free(&c);
    assert(co || PyErr_Occurred());
    return co;
}
```

The `PyAST_CompileObject()` function is the main entry point to the CPython compiler.

`compiler` is a struct defined in `Python/compile.c`.

Inside `PyAST_CompileObject()`, there are 11 main steps happening:

- Create an empty `__doc__` property to the module if it doesn't exist. 
- Create an empty `__annotations__` property to the module if it doesn't exist.
- Set the filename of the global compiler state to the filename argument.
- Set the memory allocation arena for the compiler to the one used by the interpreter.
- Copy any `__future__` flags in the module to the future flags in the compiler.
- Merge runtime flags provided by the command-line or environment variables.
- Enable any `__future__` features in the compiler.
- Set the optimization level to the provided argument or default.
- Build a symbol table from the module object.
- Run the compiler with compiler state and return the code object.
- Free any allocated memory by the compiler.

#### Future Flags and Compiler Flags

- The interpreter state, which may have been command-line options, set in `pyconfig.h` or via env.
- The use of `__future__` statements inside the actual source code of the module

```
from __future__ import print_function
// can use print() in python2.7 like python3.6
```

The code after this statement might use unresolved print_function, so the `__future__` statement is required. Otherwise, the module wouldn't import.

#### Symbol Tables

The purpose of the symbol table is to provide a list of namespaces, globals, and locals for the compiler to use for referencing and resolving scopes.

The `symtable` structure in `Include/symtable.h`.

You can provide a string with a Python expression and the `compile_type` of `eval`, or a module, function or class, and the `compile_mode` of `exec` to get a symbol tablb.

```
>>> import symtable
>>> s = symtable.symtable('a+1', filename='test.py', compile_type='eval')
>>> [symbol.__dict__ for symbol in s.get_symbols()]
[{'_Symbol__name': 'a', '_Symbol__flags': 6160, '_Symbol__scope': 3, '_Symbol__namespaces': ()}]
```

The C code behind this is all within `Python/symtable.c` and the primary interface is the `PySymtable_BuildObject()` function.

`PySymtable_BuildObject()` will loop through each statement in the module and call `symtable_visit_stmt()`. The `symtable_visit_stmt()` is a huge switch statement with a case for each statement type.

Once the resulting symtable has been created, it is sent back to be used for the compiler.

#### Core Compilation Process

The purpose of the core compiler is to:

- Convert the state, symtable, and AST into a CFG
- Protect the execution stage from runtime exceptions by catching any logic and code errors and raising them here

Use the built-in function `compile()` can call the CPython compiler. It returns a `code object` instance.

```
>>> compile('a+1', 'test.py', mode='eval')
<code object <module> at 0x7fa49ed2ae40, file "test.py", line 1>
>>> co = compile('a+1', 'test.py', mode='eval')
>>> co.co_code
b'e\x00d\x00\x17\x00S\x00'
```

There is also a `dis` module in the standard library, which **disassembles the bytecode instructions** and can print them on the screen or give you a list of `Instruction` instances.

Ongoing jump to `compiler_mod()`, a function used to switch to different compiler functions depending on the module type. Assume that mode is a Module, and then calls `assemble()` function.

#### Assembly

The assembler state is declared in `Python/compile.c`. Final the assemble will call `makecode()` function.

#### Creating a Code Object

The task of `makecode()` is to go through the compiler state, some of the assembler's properties and to put these into a `PyCodeObject` by calling `PyObject_NEW()`.

![](https://files.realpython.com/media/codeobject.9c054576627c.png)

Bytecode is sent to `PyCode_Optimize()` before it is sent to `PyCode_NewWithPosOnlyArgs()`. `PyCode_Optimize()` is part of the bytecode optimization process in `Python/peephole.c`.

Use `instaviz` module to pull all of these stages together.

```python
import instaviz

def foo():
    a = 2 ** 4
    b = 1 + 5
    c = [1, 2, 3]
    for i in c:
        print(i)
    else:
        print(a)
    return c

instaviz.show(foo)
```

### Execution

Function `run_eval_code_obj()` will pass the globals, locals, PyArena, and compiled PyCodeObject to `PyEval_EvalCode()` in `Python/ceval.c`

This stage forms the execution component of CPython. Each of the bytecode operations is taken and executed using a **“Stack Frame”** based system. (eval - 评估)

> Stack Frames also contain arguments, local variables, and other state information.
>
> Typically, a Stack Frame exists for every function call, and they are stacked in sequence. You can see CPython’s frame stack anytime an exception is unhandled and the stack is printed on the screen.

`PyEval_EvalCode()` is the public API for evaluating a code object. It will construct an execution frame from the top of the stack by calling `_PyEval_EvalCodeWithName()`.

- Kerword and positional arguments are resovled
- The use of `*args and **kwargs` in function definitions are resolved
- Arguments are added as local variables to to scope
- Co-routines and Generators are created, including the Asynchronous Generators.

![](https://files.realpython.com/media/PyFrameObject.8616eee0503e.png)

1. Constructing Thread State

    Before a frame can be executed, it needs to be referenced from a thread. The thread structure is called `PyThreadState` which defined in `Include/cpython/pystate.h`.

    ![](https://files.realpython.com/media/PyThreadState.20467f3689b7.png)

2. Constructing Frames

    ```c
    PyObject *
    _PyEval_EvalCodeWithName(PyObject *_co, PyObject *globals, PyObject *locals,
               PyObject *const *args, Py_ssize_t argcount,
               PyObject *const *kwnames, PyObject *const *kwargs,
               Py_ssize_t kwcount, int kwstep,
               PyObject *const *defs, Py_ssize_t defcount,
               PyObject *kwdefs, PyObject *closure,
               PyObject *name, PyObject *qualname)
    {
        PyCodeObject* co = (PyCodeObject*)_co;
        PyFrameObject *f;
        PyObject *retval = NULL;
        PyObject **fastlocals, **freevars;
        PyObject *x, *u;
        const Py_ssize_t total_args = co->co_argcount + co->co_kwonlyargcount;
        Py_ssize_t i, j, n;
        PyObject *kwdict;
    
        PyThreadState *tstate = _PyThreadState_GET();
        assert(tstate != NULL);
    
        if (globals == NULL) {
            _PyErr_SetString(tstate, PyExc_SystemError,
                             "PyEval_EvalCodeEx: NULL globals");
            return NULL;
        }
    
        /* Create the frame */
        f = _PyFrame_New_NoTrack(tstate, co, globals, locals);
        if (f == NULL) {
            return NULL;
        }
        fastlocals = f->f_localsplus;
        freevars = f->f_localsplus + co->co_nlocals;
    ```

3. Converting Keyword Parameters to a Dictionary

    ```c
        /* Create a dictionary for keyword parameters (**kwags) */
        if (co->co_flags & CO_VARKEYWORDS) {
            kwdict = PyDict_New();
            if (kwdict == NULL)
                goto fail;
            i = total_args;
            if (co->co_flags & CO_VARARGS) {
                i++;
            }
            SETLOCAL(i, kwdict);
        }
        else {
            kwdict = NULL;
        }
    ```

4. Converting Positional Arguments Into Variables

    ```c
        /* Copy all positional arguments into local variables */
        if (argcount > co->co_argcount) {
            n = co->co_argcount;
        }
        else {
            n = argcount;
        }
        for (j = 0; j < n; j++) {
            x = args[j];
            Py_INCREF(x);    // gc won't remove them until the frame has evaluated
            SETLOCAL(j, x);
        }
    ```

5. Packing Position Arguments Into *args

    ```c
        /* Pack other positional arguments into the *args argument */
        if (co->co_flags & CO_VARARGS) {
            u = _PyTuple_FromArray(args + n, argcount - n);
            if (u == NULL) {
                goto fail;
            }
            SETLOCAL(total_args, u);
        }
    ```

6. Loading Keyword Arguments

    ```c
        /* Handle keyword arguments passed as two strided arrays */
        kwcount *= kwstep;
        for (i = 0; i < kwcount; i += kwstep) {
            PyObject **co_varnames;
            PyObject *keyword = kwnames[i];
            PyObject *value = kwargs[i];
            Py_ssize_t j;
    
            if (keyword == NULL || !PyUnicode_Check(keyword)) {
                _PyErr_Format(tstate, PyExc_TypeError,
                              "%U() keywords must be strings",
                              co->co_name);
                goto fail;
            }
    
            /* Speed hack: do raw pointer compares. As names are
               normally interned this should almost always hit. */
            co_varnames = ((PyTupleObject *)(co->co_varnames))->ob_item;
            for (j = co->co_posonlyargcount; j < total_args; j++) {
                PyObject *name = co_varnames[j];
                if (name == keyword) {
                    goto kw_found;
                }
            }
    
            /* Slow fallback, just in case */
            for (j = co->co_posonlyargcount; j < total_args; j++) {
                PyObject *name = co_varnames[j];
                int cmp = PyObject_RichCompareBool( keyword, name, Py_EQ);
                if (cmp > 0) {
                    goto kw_found;
                }
                else if (cmp < 0) {
                    goto fail;
                }
            }
    
            assert(j >= total_args);
            if (kwdict == NULL) {
    
                if (co->co_posonlyargcount
                    && positional_only_passed_as_keyword(tstate, co,
                                                         kwcount, kwnames))
                {
                    goto fail;
                }
    
                _PyErr_Format(tstate, PyExc_TypeError,
                              "%U() got an unexpected keyword argument '%S'",
                              co->co_name, keyword);
                goto fail;
            }
    
            if (PyDict_SetItem(kwdict, keyword, value) == -1) {
                goto fail;
            }
            continue;
    
          kw_found:
            if (GETLOCAL(j) != NULL) {
                _PyErr_Format(tstate, PyExc_TypeError,
                              "%U() got multiple values for argument '%S'",
                              co->co_name, keyword);
                goto fail;
            }
            Py_INCREF(value);
            SETLOCAL(j, value);
        }
    
    ```

7. Checking the Number of Positional Arguments 

    ```c
        /* Check the number of positional arguments */
        if ((argcount > co->co_argcount) && !(co->co_flags & CO_VARARGS)) {
            too_many_positional(tstate, co, argcount, defcount, fastlocals);
            goto fail;
        }
    
    ```

8. Adding Missing Positionnal Arguments

    ```c
        /* Add missing positional arguments (copy default values from defs) */
        if (argcount < co->co_argcount) {
            Py_ssize_t m = co->co_argcount - defcount;
            Py_ssize_t missing = 0;
            for (i = argcount; i < m; i++) {
                if (GETLOCAL(i) == NULL) {
                    missing++;
                }
            }
            if (missing) {
                missing_arguments(tstate, co, missing, defcount, fastlocals);
                goto fail;
            }
            if (n > m)
                i = n - m;
            else
                i = 0;
            for (; i < defcount; i++) {
                if (GETLOCAL(m+i) == NULL) {
                    PyObject *def = defs[i];
                    Py_INCREF(def);
                    SETLOCAL(m+i, def);
                }
            }
        }
    ```

9. Adding Missing Keyword Arguments

    ```c
        /* Add missing keyword arguments (copy default values from kwdefs) */
        if (co->co_kwonlyargcount > 0) {
            Py_ssize_t missing = 0;
            for (i = co->co_argcount; i < total_args; i++) {
                PyObject *name;
                if (GETLOCAL(i) != NULL)
                    continue;
                name = PyTuple_GET_ITEM(co->co_varnames, i);
                if (kwdefs != NULL) {
                    PyObject *def = PyDict_GetItemWithError(kwdefs, name);
                    if (def) {
                        Py_INCREF(def);
                        SETLOCAL(i, def);
                        continue;
                    }
                    else if (_PyErr_Occurred(tstate)) {
                        goto fail;
                    }
                }
                missing++;
            }
            if (missing) {
                missing_arguments(tstate, co, missing, -1, fastlocals);
                goto fail;
            }
        }
    ```

10. Allocate and Initialize Storage for Cell Vars

    ```c
        /* Allocate and initialize storage for cell vars, and copy free
           vars into frame. */
        for (i = 0; i < PyTuple_GET_SIZE(co->co_cellvars); ++i) {
            PyObject *c;
            Py_ssize_t arg;
            /* Possibly account for the cell variable being an argument. */
            if (co->co_cell2arg != NULL &&
                (arg = co->co_cell2arg[i]) != CO_CELL_NOT_AN_ARG) {
                c = PyCell_New(GETLOCAL(arg));
                /* Clear the local copy. */
                SETLOCAL(arg, NULL);
            }
            else {
                c = PyCell_New(NULL);
            }
            if (c == NULL)
                goto fail;
            SETLOCAL(co->co_nlocals + i, c);
        }
    ```

11. Collapsing Closures

    ```c
        /* Copy closure variables to free variables */
        for (i = 0; i < PyTuple_GET_SIZE(co->co_freevars); ++i) {
            PyObject *o = PyTuple_GET_ITEM(closure, i);
            Py_INCREF(o);
            freevars[PyTuple_GET_SIZE(co->co_cellvars) + i] = o;
        }
    ```

12. Creating Generators, Coroutines and Asynchronous Generators

    ```c
        /* Handle generator/coroutine/asynchronous generator */
        if (co->co_flags & (CO_GENERATOR | CO_COROUTINE | CO_ASYNC_GENERATOR)) {
            PyObject *gen;
            int is_coro = co->co_flags & CO_COROUTINE;
    
            /* Don't need to keep the reference to f_back, it will be set
             * when the generator is resumed. */
            Py_CLEAR(f->f_back);
    
            /* Create a new generator that owns the ready to run frame
             * and return that as the value. */
            if (is_coro) {
                gen = PyCoro_New(f, name, qualname);
            } else if (co->co_flags & CO_ASYNC_GENERATOR) {
                gen = PyAsyncGen_New(f, name, qualname);
            } else {
                gen = PyGen_NewWithQualName(f, name, qualname);
            }
            if (gen == NULL) {
                return NULL;
            }
    
            _PyObject_GC_TRACK(f);
    
            return gen;
        }
    ```

13. Call `PyEval_EvalFrameEx(f,0)` as return value.

    The `PyEval_EvalFrameEx()` calls the interpreter's configured frame evaluation function in the `eval_frame` property.

    ```c
    PyObject *
    PyEval_EvalFrameEx(PyFrameObject *f, int throwflag)
    {
        PyInterpreterState *interp = _PyInterpreterState_GET_UNSAFE();
        return interp->eval_frame(f, throwflag);
    }
    ```

#### Frame Execution

There are other usages of frames, like the coroutine decorator, which dynamically generates a frame with the target as a variable.

Frames are executed in the main execution loop inside **`_PyEval_EvalFrameDefault()`**. This function is central function that bridges everything together and brings your code to life.

It contains decades of optimization since even a single line of code can have a significant impact on performance for the whole of CPython.

Everything that gets executed in CPython goes through this function.

#### The Value Stack

This stack is a list of pointers to sequential `PyObject` instances.

For example, if you created a `PyLong` with the value 10 and pushed it onto the value stack:

```c
PyObject *a = PyLong_FromLong(10);
PUSH(a);
```

Use `POP()` macro to take the top value from the stack:

```c
PyObject *a = POP();
```

## Part 4: Objects in CPython

Basic types like strings, lists, tuple, dictionaries, and objects.

All types in Python inhert from `object`, a built-in base type. Even strings, tuples, and list inhert from `object`. `PyObject` is the data structure for the beginning of the Python object's memory.

Much of the base object API is declared in `Objects/object.c`, like `PyObject_Repr()` which the built-in `repr()` function.

```c
PyObject *
PyObject_Repr(PyObject *v)
{
    PyObject *res;
    if (PyErr_CheckSignals())
        return NULL;

    if (v == NULL)
        return PyUnicode_FromString("<NULL>");
    if (Py_TYPE(v)->tp_repr == NULL)
        return PyUnicode_FromFormat("<%s object at %p>",
                                    v->ob_type->tp_name, v);

    /* It is possible for a type to have a tp_repr representation that loops
       infinitely. */
    if (Py_EnterRecursiveCall(" while getting the repr of an object"))
        return NULL;
    res = (*v->ob_type->tp_repr)(v);
    Py_LeaveRecursiveCall();
    if (res == NULL)
        return NULL;
    if (!PyUnicode_Check(res)) {
        PyErr_Format(PyExc_TypeError,
                     "__repr__ returned non-string (type %.200s)",
                     res->ob_type->tp_name);
        Py_DECREF(res);
        return NULL;
    }
    return res;
}
```

If the `tp_repr` field is not set, i.e. the object doesn't declare a custom `__repr__` method, then the default behavior is run, which is to return "<%s object at %p>" with the type name and the ID.

The `ob_type` field for a given `PyObject*` will point to the data structure `PyTypeObject`, defined in `Include/cpython/object.h`. This data structure lists all the built-in functions, as fields and the arguments they should receive.

```c
reprfunc tp_repr;
```

`reprfunc` is a typedef for `typedef PyObject *(*reprfunc)(PyObject *);`

### Base Object Type

A simple way to think of a Python object is consisting of 2 things:

- The core data model, with pointers to compiled functions
- A dictionary with any custom attributes and methods

The core data model is defined in the `PyTypeObject`.

### The Bool and Long Integer Type

#### Bool

```c
PyObject *PyBool_FromLong(long ok)
{
    PyObject *result;

    if (ok)
        result = Py_True;
    else
        result = Py_False;
    Py_INCREF(result);
    return result;
}
```

#### Long

In the transition from Python 2 to 3, CPython dropped support for the `int` type and instead used the `long` type as the primary integer type.

Python's `long` type is quite special in that it can store a variable-length number. The maximum length is set in the compiled binary.

The data structure of a Python `long` consists of the `PyObject` header and a list of digits.

```c
struct _longobject {
    PyObject_VAR_HEAD
    digit ob_digit[1];
};
```

Memory is allocated to a new `long` through `_PyLong_New()`. This function takes a fixed length and make sure it is smaller than `MAX_LONG_DIGITS`. Then it reallocates the memory for `ob_digit` to match the length.

### Generator Type

Generator are functions which return `yield` statement and can be called continually to generate further values.

Commonly they are **used as a more memory efficient way of looping through values in a large block of data**, like a file, a database or over a network.

The `PyGenObject` type is defined in `Include/genobject.h` and there are 3 flavors:

- Generator objects
- Coroutine objects
- Async generateor objects

```c
#define _PyGenObject_HEAD(prefix)                                           \
    PyObject_HEAD                                                           \
    /* Note: gi_frame can be NULL if the generator is "finished" */         \
    struct _frame *prefix##_frame;                                          \
    /* True if generator is being executed. */                              \
    char prefix##_running;                                                  \
    /* The code object backing the generator */                             \
    PyObject *prefix##_code;                                                \
    /* List of weak reference. */                                           \
    PyObject *prefix##_weakreflist;                                         \
    /* Name of the generator. */                                            \
    PyObject *prefix##_name;                                                \
    /* Qualified name of the generator. */                                  \
    PyObject *prefix##_qualname;                                            \
    _PyErr_StackItem prefix##_exc_state;

typedef struct {
    /* The gi_ prefix is intended to remind of generator-iterator. */
    _PyGenObject_HEAD(gi)
} PyGenObject;

typedef struct {
    _PyGenObject_HEAD(cr)
    PyObject *cr_origin;
} PyCoroObject;

typedef struct {
    _PyGenObject_HEAD(ag)
    PyObject *ag_finalizer;

    /* Flag is set to 1 when hooks set up by sys.set_asyncgen_hooks
       were called on the generator, to avoid calling them more
       than once. */
    int ag_hooks_inited;

    /* Flag is set to 1 when aclose() is called for the first time, or
       when a StopAsyncIteration exception is raised. */
    int ag_closed;

    int ag_running_async;
} PyAsyncGenObject;
```

If you call `__next__()` on the generator object, the next value is yielded until eventually a `StopIteration` is raised.

Each time `__next__()` is called, the code object inside the generators `gi_code` field is executed as a new frame and the return value is pushed to the value stack.

Whenever `__next__()` is called on a generator object, `gen_iternext()` is called with the generator instance, which immediately calls `gen_send_ex()` inside `Objects/genobject.c`.

```c
static PyObject *
gen_send_ex(PyGenObject *gen, PyObject *arg, int exc, int closing)
{
    PyThreadState *tstate = _PyThreadState_GET();  // 1. get thread state
    PyFrameObject *f = gen->gi_frame;              // 2. get generator frame object
    PyObject *result;

    if (gen->gi_running) {       // 3. if generator is running, raise a ValueError 
        const char *msg = "generator already executing";
        if (PyCoro_CheckExact(gen)) {
            msg = "coroutine already executing";
        }
        else if (PyAsyncGen_CheckExact(gen)) {
            msg = "async generator already executing";
        }
        PyErr_SetString(PyExc_ValueError, msg);
        return NULL;
    }
    // 4. if frame is empty or frame stack top is empty
    if (f == NULL || f->f_stacktop == NULL) {   
        if (PyCoro_CheckExact(gen) && !closing) {
            /* `gen` is an exhausted coroutine: raise an error,
               except when called from gen_close(), which should
               always be a silent method. */
            PyErr_SetString(
                PyExc_RuntimeError,
                "cannot reuse already awaited coroutine");
        }
        else if (arg && !exc) {
            /* `gen` is an exhausted generator:
               only set exception if called from send(). */
            if (PyAsyncGen_CheckExact(gen)) {
                PyErr_SetNone(PyExc_StopAsyncIteration);
            }
            else {
                PyErr_SetNone(PyExc_StopIteration);
            }
        }
        return NULL;
    }

    // 5. if the last struction in the frame is -1, pass a non-Non argument will raise exception 
    if (f->f_lasti == -1) {
        if (arg && arg != Py_None) {
            const char *msg = "can't send non-None value to a "
                              "just-started generator";
            if (PyCoro_CheckExact(gen)) {
                msg = NON_INIT_CORO_MSG;
            }
            else if (PyAsyncGen_CheckExact(gen)) {
                msg = "can't send non-None value to a "
                      "just-started async generator";
            }
            PyErr_SetString(PyExc_TypeError, msg);
            return NULL;
        }
    } else {
        /* Push arg onto the frame's value stack */
        result = arg ? arg : Py_None;
        Py_INCREF(result);
        *(f->f_stacktop++) = result;
    }  // 6. else, this is the first time it's being called, and push value to stack

    /* Generators always return to their most recent caller, not
     * necessarily their creator. */
    Py_XINCREF(tstate->frame);
    assert(f->f_back == NULL);
    f->f_back = tstate->frame;  // 7. sent return value to the caller

    gen->gi_running = 1;  // 8. mark generator as running
    gen->gi_exc_state.previous_item = tstate->exc_info; // 9. copy exception info
    tstate->exc_info = &gen->gi_exc_state; // 10. set thread state exception info
    result = PyEval_EvalFrameEx(f, exc); // 11. ceval.c 
    tstate->exc_info = gen->gi_exc_state.previous_item; // 12. reset thread state
    gen->gi_exc_state.previous_item = NULL; 
    gen->gi_running = 0; // 13. mark generator as not running

    /* Don't keep the reference to f_back any longer than necessary.  It
     * may keep a chain of frames alive or it could create a reference
     * cycle. */
    assert(f->f_back == tstate->frame);
    Py_CLEAR(f->f_back);

    /* If the generator just returned (as opposed to yielding), signal
     * that the generator is exhausted. */
    if (result && f->f_stacktop == NULL) {
        if (result == Py_None) {
            /* Delay exception instantiation if we can */
            if (PyAsyncGen_CheckExact(gen)) {
                PyErr_SetNone(PyExc_StopAsyncIteration);
            }
            else {
                PyErr_SetNone(PyExc_StopIteration);
            }
        }
        else {
            /* Async generators cannot return anything but None */
            assert(!PyAsyncGen_CheckExact(gen));
            _PyGen_SetStopIterationValue(result);
        }
        Py_CLEAR(result);
    }
    else if (!result && PyErr_ExceptionMatches(PyExc_StopIteration)) {
        const char *msg = "generator raised StopIteration";
        if (PyCoro_CheckExact(gen)) {
            msg = "coroutine raised StopIteration";
        }
        else if PyAsyncGen_CheckExact(gen) {
            msg = "async generator raised StopIteration";
        }
        _PyErr_FormatFromCause(PyExc_RuntimeError, "%s", msg);

    }
    else if (!result && PyAsyncGen_CheckExact(gen) &&
             PyErr_ExceptionMatches(PyExc_StopAsyncIteration))
    {
        /* code in `gen` raised a StopAsyncIteration error:
           raise a RuntimeError.
        */
        const char *msg = "async generator raised StopAsyncIteration";
        _PyErr_FormatFromCause(PyExc_RuntimeError, "%s", msg);
    }

    if (!result || f->f_stacktop == NULL) {
        /* generator can't be rerun, so release the frame */
        /* first clean reference cycle through stored exception traceback */
        exc_state_clear(&gen->gi_exc_state);
        gen->gi_frame->f_gen = NULL;
        gen->gi_frame = NULL;
        Py_DECREF(f);
    }

    return result;
}
```

When a new coroutine is created using `PyCoro_New()`, a new async generator is created with `PyAsyncGen_New()` or a generator with `PyGen_NewWithQualName()`.

 These objects are returned early instead of returning an evaluated frame, which is why you get a generator object after calling a function with a yield statement:

```c
// Python/ceval.c
PyObject *
_PyEval_EvalCodeWithName(PyObject *_co, PyObject *globals, PyObject *locals, ...
...
    /* Handle generator/coroutine/asynchronous generator */
    if (co->co_flags & (CO_GENERATOR | CO_COROUTINE | CO_ASYNC_GENERATOR)) {
        PyObject *gen;
        PyObject *coro_wrapper = tstate->coroutine_wrapper;
        int is_coro = co->co_flags & CO_COROUTINE;
        ...
        /* Create a new generator that owns the ready to run frame
         * and return that as the value. */
        if (is_coro) {
            gen = PyCoro_New(f, name, qualname);
        } else if (co->co_flags & CO_ASYNC_GENERATOR) {
            gen = PyAsyncGen_New(f, name, qualname);
        } else {
            gen = PyGen_NewWithQualName(f, name, qualname);
        }
        ...
        return gen;
    }
...
```

```c
static PyObject *
gen_new_with_qualname(PyTypeObject *type, PyFrameObject *f,
                      PyObject *name, PyObject *qualname)
{
    PyGenObject *gen = PyObject_GC_New(PyGenObject, type);
    if (gen == NULL) {
        Py_DECREF(f);
        return NULL;
    }
    gen->gi_frame = f;
    f->f_gen = (PyObject *) gen;
    Py_INCREF(f->f_code);
    gen->gi_code = (PyObject *)(f->f_code);
    gen->gi_running = 0;
    gen->gi_weakreflist = NULL;
    gen->gi_exc_state.exc_type = NULL;
    gen->gi_exc_state.exc_value = NULL;
    gen->gi_exc_state.exc_traceback = NULL;
    gen->gi_exc_state.previous_item = NULL;
    if (name != NULL)
        gen->gi_name = name;
    else
        gen->gi_name = ((PyCodeObject *)gen->gi_code)->co_name;
    Py_INCREF(gen->gi_name);
    if (qualname != NULL)
        gen->gi_qualname = qualname;
    else
        gen->gi_qualname = gen->gi_name;
    Py_INCREF(gen->gi_qualname);
    _PyObject_GC_TRACK(gen);
    return (PyObject *)gen;
}
```

Bringing this all together you can see how the generator expression is a powerful syntax where a single keyword, **`yield` triggers a whole flow to create a unique object, copy a compiled code object as a property, set a frame, and store a list of variables in the local scope**.

## Part 5: The CPython Standard Library

### Python Modules

The modules written in pure Python are all located in the `Lib/` directory in the source code.

### Python and C Modules

`Modules/` for the C component. 

There are two exceptions to this rule, the `sys` module, found in `Python/sysmodule.c` and the `__builtins__` module, found in `Python/bltinmodule.c`.

 What happens when you type `print("hello world!")`?

- The argument "hello world" was converted from a string constant to a `PyUnicodeObject` by the compiler.
- `builtin_print` was executed with 1 argument, and NULL kwnames
- The `file` variable is set to `PyId_stdout`, the system's stdout handle
- Each argument is sent to `file`
- A line break, `\n` is sent to file

### The CPython Regression Test Suite

The test suite is located in `Lib/test` and written almost entirely in Python.

```
python3 -m test --list-tests
```

## Appendix

Python command-line arguments

```
-c cmd : program passed in as string (terminates option list)
-m mod : run library module as a script (terminates option list)
-v     : verbose (trace import statements);
-X opt : set implementation-specific option, eg: -X dev
```

