#!/bin/bash

echo

var1="'(]\\{}\$\""
echo $var1                   # '(]\{}$"
echo "$var1"                 # '(]\{}$"

echo

IFS='\'
echo $var1                   # '(] {}$"
echo "$var1"                 # '(]\{}$"

echo

var2="\\\\\""
echo $var2                   #   "
echo "$var2"                 # \\"
# var2="\\\\"" is illegal

echo

var3='\\\\'
echo $var3                   # 
echo "$var3"                 # \\\\

echo "$(echo '"')"           # "

var4="Two bits"
echo "\$var1 = "$var1""      # $var1 = Two bits

exit 0
