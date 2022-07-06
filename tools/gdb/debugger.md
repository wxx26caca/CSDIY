## preping for the debugger
gcc -g a.c -o test
**-g** flag is important (to create symbol table)
## starting
gdb ./test
## run
## break
- `break <function_name>` or `b <function_name>`
- `break <filename>:<line of code to stop in>` e.g. `b test.c:5`
## next
execute next line of code, shorthand `n`
## step
next line of code, stepping into functions, shorthand `s`
## continue
go to next breakpoint
## print
print out a variables/expressions contents, shorthand `p`
e.g. `p x`
## display
print out a variables/expressions value every step
e.g. `disp x`
## undisplay
cancel a display command
e.g. `undisplay 3`
## list
show code at a certain location
## set
set variable x = 12
## cond
conditional
`cond <breakpoint> <condition>`
e.g. `cond 1 val>0`
stop at breakpoint 1 when val becomes greater then 0
