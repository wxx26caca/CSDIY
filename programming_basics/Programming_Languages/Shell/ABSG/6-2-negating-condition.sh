#!/bin/bash

true       # The "true" builtin.
echo "exit status of \"true\" = $?"
# exit status of "true" = 0

! true
echo "exit status of \"! true\" = $?"
# exit status of "! true" = 1
# Note that the "!" needs a space between it and the command.

echo

# The '!' operator prefixing a command invokes the Bash history mechanism
true
!true
# No error this time, but no negation either.
# It just repeats the previous command (true).

echo

# Preceding a _pipe_ with ! inverts the exit status returned.
ls | bogus_command     # bogus_command: command not found
echo $?                # 127

! ls | bogus_command   # bogus_command: command not found
echo $?                # 0

# Note that the ! does not change the execution of the pipe.
# Only the exit status changes.

exit 0
