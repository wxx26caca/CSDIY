#!/bin/bash

echo ""

echo "This will print
as two lines."
# This will print
# as two lines.

echo "This will print \
as one line."
# This will print as one line.

echo ; echo

echo "\v\v\v\v"      # \v\v\v\v
echo "VERTICAL TABS"
echo -e "\v\v\v\v"   # Prints 4 vertical tabs.
echo "QUOTATION MARK"
echo -e "\042"       # Prints " (quote, octal ASCII character 42).

# The $'\X' construct makes the -e option unnecessary.
echo ; echo "NEWLINE and (maybe) BEEP"
echo $'\n'           # Newline.
echo $'\a'           # Alert (beep).
                     # May only flash, not beep, depending on terminal.

echo "Introducing the \$\' ... \' string-expansion construct . . . "
echo ". . . featuring more quotation marks."

# '\nnn' is an octal value.
# '\xhhh' is a hexadecimal value.
echo $'\t \042 \t'   # Quote (") framed by tabs.
echo $'\t \x22 \t'   # Quote (") framed by tabs.

echo

quote=$'\042'        # " assigned to a variable.
echo "$quote Quoted string $quote and this lies outside the quotes."
# " Quoted string " and this lies outside the quotes.

echo

triple_underline=$'\137\137\137'  # 137 is octal ASCII code for '_'.
echo "$triple_underline UNDERLINE $triple_underline"
# ___ UNDERLINE ___

echo

ABC=$'\101\102\103\010'           # 101, 102, 103 are octal A, B, C.
echo $ABC                         # ABC

echo

escape=$'\033'                    # 033 is octal for escape.
echo "\"escape\" echoes as $escape"
#                                   no visible output.

echo

exit 0
