#!/bin/bash
# Cleanup, version 3

LOG_DIR=/var/log
ROOT_UID=0     # Only users with $UID 0 have root privileges.
LINES=50       # Default number of lines saved.
E_XCD=86       # Can't change directory?
E_NOTROOT=87   # Non-root exit error.

# Run as root, of course.
if [ "$UID" -ne "$ROOT_UID" ]
then
  echo "Must be root to run this script."
  exit $E_NOTROOT
fi

# Test whether command-line argument is present (non-empty).
if [ -n "$1" ]
then
  lines=$1
else
  lines=$LINES  # Default, if not specified on command-line.
fi

# a better way of checking command-line arguments,
#
#    E_WRONGARGS=85  # Non-numerical argument (bad argument format).
#
#    case "$1" in
#    ""      ) lines=50;;
#    *[!0-9]*) echo "Usage: `basename $0` lines-to-cleanup";
#     exit $E_WRONGARGS;;
#    *       ) lines=$1;;
#    esac
#
#* Skip ahead to "Loops" chapter to decipher all this.

cd $LOG_DIR

if [ `pwd` != "$LOG_DIR" ]
then
  echo "Can't change to $LOG_DIR."
  exit $E_XCD
fi

# Far more efficient is:
#
# cd /var/log || {
#   echo "Cannot change to necessary directory." >&2
#   exit $E_XCD;
# }

tail -n $lines messages > mesg.temp  # Save last section of message log file.
mv mesg.tmp messages                 # Rename it as system log file

cat /dev/null > wtmp  #  ': > wtmp' and '> wtmp'  have the same effect.
echo "Log files cleaned up."

exit 0
#  A zero return value from the script upon exit indicates success
#+ to the shell.
