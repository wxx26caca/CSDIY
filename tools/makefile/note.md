## Syntax
```
target: prerequisites
    command
```
> use tab not space
## Variables
```
files := file1 file2
x := dude

some_file: $(files)
    echo "Look at this variable: " $(files)
    touch some_file
read_x:
    echo $(x)
    echo ${x}
```
### Automatic Variables
`$@` - The file name of the target of the rule.
`$%` - The target member name, when the target is an archive member.
`$<` - The name of the first prerequisties.
`$^` - The name of all the prerequisties.
`$?` - The names of all the prerequisites that are newer than the target.
```
hey: one two
    # Outputs "hey", since this is the first target
    echo $@
    # Outputs all prerequisites newer than the target
    echo $?
    # Outputs all prerequisites
    echo $^
one:
    touch one
two:
    touch two
clean:
    rm -rf one two
```

## Wildcards
`*` searches your filesystem for matching filenames.
`%`:
- in matching mode, it matches one or more characters in a string.
- in replacing mode, it take matched result and relaces it in a string.
- most often used in rule definitions and in some specific functions.
## Rules
### Implicit Rules
- Compiling a C program. `$(CC) -c $(CPPFLAGS) $(CFLAGS)`
- Compiling a C++ program. `$(CXX) -c $(CPPFLAGS) $(CXXFLAGS)`
- Linking a single object file. `$(CC) $(LDFLAGS) <.o filename> $(LOADLIBES) $(LDLIBS)`
import variables used by implicit rules:
- `CC`: Program for compiling C programs; default `cc`.
- `CXX`: Program for compiling C++ programs; default `g++`.
- `CFLAGS`: Extra flags to give to the C compiler.
- `CXXFLAGS`: Extra flags to give to the C++ compiler.
- `CPPFLAGS`: Extra flags to give to the C preprocessor.
- `LDFLAGS`: Extra flags to give to compilers when they are supposed to invoke the linker.
```
CC = gcc
CFLAGS = -g

blah: blah.o

blah.c:
    echo "int main() { return 0; }" > blah.c

clean:
    rm -f blah*
```
### Static Pattern Rules
Syntax
```
targets...: target-pattern: prereq-patterns ...
    commands
```
example
```
objects = foo.o bar.o all.o

all: $(objects)

$(objects): %.o: %.c
# equivalent to
# foo.o: foo.c
# bar.o: bar.c
# all.o: all.c

all.c:
    echo "int main() { return 0; }" > all.c

%.c:
    touch $@

clean:
    rm -f *.o *.c all
```
### Static Pattern Rules and Filter
```
obj_files = foo.result bar.o lose.o
src_files = foo.raw bar.c lose.c

.PHONY: all
all: $(obj_files)

$(filter %.o,$(obj_files)): %.o: %.c
    echo "target: $@ prereq: $<"
$(filter %.result,$(obj_files)): %.result: %.raw
    echo "target: $@ prereq: $<"

%.c %.raw:
    touch $@

clean:
    rm -f $(src_files)
```
### Pattern Rules
Pattern rules only used to define your own implicit rules or a simple form of static pattern rules.
```
# Define a pattern rule that compiles every .c file into a .o file.
%.o: %.c
    $(CC) -c $(CFLAGS) $(CPPFLAGS) $< -o $@

# Define a pattern rule that has no pattern in the prerequisites.
%.c:
    touch $@
```
### Double-Colon Rules
> Rarely used, used to allow multiple rules to be defined for the same target.
```
all: blah

blah::
    echo "hello"

blah::
    echo "hello again"
```
> If there were single colons, a warning would be printed and only the second set of commands would run.

## Commands and Execution
```
# Add an @ before a command to stop it from being printe, the output of command exec keep printd
slience:
    @echo "This make line will not be printed"
    echo "This will"

# Each command is run in a new shell.
exec:
    cd ..
    echo `pwd`

    # This cd command affects the next because they are on the same line
    cd ..;echo `pwd`

    # Same as above
    cd ..; \
    echo `pwd`

# default shell is /bin/sh. change it by changing the SHELL variable
SHELL=/bin/bash

b:
    echo "hello from bash"
```
### Error handling with -k, -i and -
- `-k` when running make to continue running even in the face of errors.
- `-` before a command to suppress the error
- `-i` make to have this happen for every command
### Recursive use of make
use the special `$(MAKE)` instead of `make` because it will pass the make flags for you and won't itself to affected by them.
```
new = "hello:\n\ttouch insidefile"

all:
    mkdir -p subdir
    printf $(new) | sed -e 's/^ //' > subdir/makefile
    cd subdir && $(MAKE)

clean:
    rm -rf subdir
```
### Use export for recursive make
```
new = "hello:\n\techo \$$(cool)"

all:
    mkdir -p subdir
    echo $(new) | sed -e 's/^ //' > subdir/makefile
    @echo "---makefile contents---"
    @cd subdir && cat makefile
    @echo "---end makefile contents---"
    cd subdir && $(MAKE)

# Note that variables and exports. They are set/affected globally.
cool = "The sbudir can see me"
export cool
# unexport cool will nullify the line above

clean:
    rm -rf subdir
```
```
# export variables to have them run in the shell
one = "one"
export two = "two"

all:
    @echo $(one)
    @echo $$one
    @echo $(two)
    @echo $$two

# makefile variable -> use a single dollar sign
# shell variable -> use two dollar signs
[Using variables in recipes](https://www.gnu.org/software/make/manual/html_node/Variables-in-Recipes.html)
```
```
LIST = one two three
all:
    for i in $(LIST); do \
        echo $$i; \
    done

```
results in the following command being passed to the shell:
```
for i in one two three; do \
    echo $i; \
done
```
`.EXPORT_ALL_VARIABLES` exports all variables for you.

## Makefile Cookbook
```makefile
TARGET_EXEC := final_program

BUILD_DIR := ./build
SRC_DIRS := ./src

SRCS := $(shell find $(SRC_DIRS) -name '*.cpp' -or -name '*.c' -or -name '*.s')

# String substitution for every C/C++ files. e.g. hello.c -> ./build/hello.o
OBJS := $(SRCS:%=(BUILD_DIR)/%.o)

# String substitution (suffix version without %). e.g. hello.o -> hello.d
DEPS := $(OBJS:.o=.d)

INC_DIRS := $(shell find $(SRC_DIRS) -type -d)
INC_FLAGS := $(addprefix -I,$(INC_DIRS))

CPPFLAGS := $(INC_FLAGS) -MMD -MP

$(BUILD_DIR)/$(TARGET_EXEC): $(OBJS)
    $(CC) $(OBJS) -o $@ $(LDFLAGS)

$(BUILD_DIR)/%.c.o: %.c
    mkdir -p $(dir $@)
    $(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/%.cpp.o: %.cpp
    mkdir -p $(dir $@)
    $(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $< -o $@

.PHONY: clean
clean:
    rm -rf $(BUILD_DIR)

# Include the .d makefiles. The - at the front suppresses the errors of missing
# makefiles. Initially, all the .d files will be missing, and we don't want those
# errors to show up.
-include $(DEPS)
```

[makefile tutorial](https://makefiletutorial.com/)
