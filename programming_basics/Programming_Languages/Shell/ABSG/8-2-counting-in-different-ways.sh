#!/bin/bash
# Counting to 11 in 10 different ways.

n=1; echo -n "$n "

let "n = $n + 1"
echo -n "$n "

: $((n = $n + 1))
#  ":" necessary because otherwise Bash attempts
#+ to interpret "$((n = $n + 1))" as a command.
echo -n "$n "

(( n = n + 1 ))
# A simpler alternative to the method above.
echo -n "$n "

n=$(($n+1))
echo -n "$n "

: $[ n = $n + 1 ]
#  ":" necessary because otherwise Bash attempts
#+ to interpret "$[ n = $n + 1 ]" as a command.
#  Works even if "n" was initialized as a string.
echo -n "$n "

n=$[ $n + 1 ]
#  Works even if "n" was initialized as a string.
#* Avoid this type of construct, since it is obsolete and nonportable.
echo -n "$n "

# For C-style increment operators.
# n++ and ++n both work.
let "n++"
echo -n "$n "

(( n++ ))
echo -n "$n "

: $(( n++ ))
echo -n "$n "

: $[ n++ ]
echo -n "$n "

echo

exit 0
