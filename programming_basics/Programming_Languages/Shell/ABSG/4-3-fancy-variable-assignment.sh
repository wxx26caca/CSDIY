#!/bin/bash

a=`echo Hello!`
echo $a

#  Note that including an exclamation mark (!) within a
#+ command substitution construct will not work from the command-line,
#+ since this triggers the Bash "history mechanism."
#  Inside a script, however, the history functions are disabled by default.

a=`ls -l`         # Assigns result of 'ls -l' command to 'a'
echo $a           # Unquoted, however, it removes tabs and newlines.
echo
echo "$a"         # The quoted variable preserves whitespace.

R=$(cat /etc/redhat-release)    # Variable assignment using the $(...) mechanism
arch=$(uname -m)

exit 0
