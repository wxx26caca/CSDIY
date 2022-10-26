#!/bin/bash
# Arithmetic Tests using (( ))
# The (( ... )) construct evaluates and tests numerical expressions.
# Exit status opposite from [ ... ] construct!

(( 0 ))
echo "Exit status of \"(( 0 ))\" is $?"          # 1

(( 1 ))
echo "Exit status of \"(( 1 ))\" is $?."         # 0

(( 5 > 4 ))                                      # true
echo "Exit status of \"(( 5 > 4 ))\" is $?."     # 0

(( 5 > 9 ))                                      # false
echo "Exit status of \"(( 5 > 9 ))\" is $?."     # 1

(( 5 == 5 ))                                     # true
echo "Exit status of \"(( 5 == 5 ))\" is $?."    # 0

(( 5 - 5 ))                                      # 0
echo "Exit status of \"(( 5 - 5 ))\" is $?."     # 1

(( 5 / 4 ))                                      # Division o.k.
echo "Exit status of \"(( 5 / 4 ))\" is $?."     # 0

(( 1 / 2 ))                                      # Division result < 1 Rounded off to 0.
echo "Exit status of \"(( 1 / 2 ))\" is $?."     # 1

(( 1 / 0 )) 2>/dev/null                          # Illegal division by 0.
echo "Exit status of \"(( 1 / 0 ))\" is $?."     # 1

(( 1 / 0 ))
# bash: line 33: ((: 1 / 0 : division by 0 (error token is "0 ")
echo "Exit status of \"(( 1 / 0 ))\" is $?."     # 1

# (( ... )) also useful in an if-then test.

var1=5
var2=4

if (( var1 > var2 ))
# Note: Not $var1, $var2. 
# $var1, $var2 in bash 5.0 is ok
then
  echo "$var1 is greater than $var2"
fi

exit 0
