#!/bin/bash
# Using 'shift' to step through all the positional parameters.

until [ -z "$1" ]      # Until all parameters used up
do
  echo -n "$1 "
  shift
done

echo

echo "$2"              #  Nothing echoes!
#  When $2 shifts into $1 (and there is no $3 to shift into $2)
#+ then $2 remains empty.
#  So, it is not a parameter *copy*, but a *move*.

#  Attempting a 'shift' past the number of 
#+ positional parameters ($#) returns an exit status of 1,
#+ and the positional parameters themselves do not change.
#  This means possibly getting stuck in an endless loop.
#
#  For example:
#      until [ -z "$1" ]
#      do
#         echo -n "$1 "
#         shift 20    #  If less than 20 pos params,
#      done           #+ then loop never ends!
#
# When in doubt, add a sanity check. . . .
#           shift 20 || break
#                    ^^^^^^^^

exit
