#!/bin/bash

# Call this script with at least 10 parameters, for example
# ./scriptname 1 2 3 4 5 6 7 8 9 10

MINPARAMS=10
echo "The name of this script is \"$0\"."
echo "The name of this script is \"`basename $0`\"."
echo

if [ -n "$1" ]
then
  echo "Parameter #1 is $1"
fi

if [ -n "$2" ]
then
  echo "Parameter #2 is $2"
fi

if [ -n "$3" ]
then
  echo "Parameter #3 is $3"
fi

if [ -n "${10}" ]            # Parameters > $9 must be enclosed in {brackets}.
then
  echo "Parameter #10 is ${10}"
fi

echo "-----------------------------------"
echo "All the command-line parameters are: "$*""

if [ $# -lt "$MINPARAMS" ]
then
  echo
  echo "This script needs at least $MINPARAMS command-line arguments"
fi

exit 0
