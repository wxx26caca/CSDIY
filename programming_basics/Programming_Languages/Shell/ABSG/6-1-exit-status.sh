#!/bin/bash
#  By convention, an 'exit 0' indicates success,
#+ while a non-zero exit value means an error or anomalous condition.

echo hello
echo $?    # Exit status 0 returned because command executed successfully.

lasdf
echo $?    # Non-zero exit status returned -- command failed to execute.

exit 113   # Will return 113 to shell.
           # To verify this, type "echo $?" after script terminates.
