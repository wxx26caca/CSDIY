#!/bin/bash
# Manipulating a variable, C-style, using the (( ... )) construct.

echo

(( a = 32 ))
echo "a (initial value) = $a"

(( a++ ))
echo "a (after a++) = $a"

(( a-- ))
echo "a (after a--) = $a"

(( ++a ))
echo "a (after ++a) = $a"

(( --a ))
echo "a (after --a) = $a"

echo

#  Note that, as in C, pre- and post-decrement operators
#+ have different side-effects.

n=1; let --n && echo "True" || echo "False"  # False
n=1; let n-- && echo "True" || echo "False"  # True

(( t = a<45?1:2 ))
echo "t = $t"

echo

# "for" and "while" loops also can use the (( ... )) construct.
# These work only with version 2.04 or later of Bash.

exit
