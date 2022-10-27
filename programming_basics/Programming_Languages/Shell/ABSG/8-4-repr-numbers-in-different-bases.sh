#!/bin/bash
# Representation of numbers in different bases.

echo

# Decimal: the default
let "dec = 32"
echo "decimal number = $dec"

# Octal: numbers preceded by '0' 
let "oct = 032"
echo "Octal number = $oct"

# Hexadecimal: numbers preceded by '0x' or '0X'
let "hex = 0x32"
echo "Hexadecimal number = $hex"

echo $((0x9abc))
# output: 39612
# double-parentheses arithmetic expansion/evaluation
# Expresses result in decimal.

# Other bases: BASE#NUMBER
# BASE between 2 and 64.
# NUMBER must use symbols within the BASE range

let "bin = 2#111100111001101"
echo "binary number = $bin"     # 31181

let "b32 = 32#77"
echo "base-32 number = $b32"    # 231

let "b64 = 64#@_"
echo "base-64 number = $b64"
# This notation only works for a limited range (2 - 64) of ASCII characters.
# 10 digits + 26 lowercase characters + 26 uppercase characters + @ + _

echo

echo $((36#zz)) $((2#10101010)) $((16#AF16)) $((53#1aA))
# 1295 170 44822 3375

#  Using a digit out of range of the specified base notation
#+ gives an error message.
let "bad_oct = 081"
# error message: value too great for base

exit $?
