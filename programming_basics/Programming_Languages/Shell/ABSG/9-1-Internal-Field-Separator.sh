#!/bin/bash

var1="a+b+c"
var2="d-e-f"
var3="g,h,i"

IFS=+
echo "$var1"
echo "$var2"
echo "$var3"

echo

IFS="-"
echo "$var1"
echo "$var2"
echo "$var3"

echo

IFS=","
echo "$var1"
echo "$var2"
echo "$var3"

echo

IFS=" "
echo "$var1"
echo "$var2"
echo "$var3"

echo

# ======================================================= #
# $IFS treats whitespace differently than other characters.

output_args_one_per_line() {
  for arg
  do
    echo "[$arg]"
  done
}

echo; echo "IFS=\" \""

IFS=" "
var4=" a  b c   "
output_args_one_per_line $var4
# [a]
# [b]
# [c]


echo; echo "IFS=:"

IFS=:
var5=":a::b:c:::"
output_args_one_per_line $var5
# []
# [a]
# []
# [b]
# [c]
# []
# []

exit 0
