#!/bin/bash
# Queries an rpm file for description, listing,
# and whether it can be installed.
# Saves output to a file.

SUCCESS=0
E_NOARGS=65

if [ -z "$1" ]
then
  echo "Usage `basename $0` rpm-file"
  exit $E_NOARGS
fi

{ # Begin the code block.
  echo
  echo "Archive description:"
  rpm -qpi $1  # Query description.
  echo
  echo "Archive listing:"
  rpm -qpl $1  # Query listing.
  echo
  rpm -i --test $1  # Query whether rpm file can be installed.
  if [ "$?" -ne $SUCCESS ]
  then
    echo "$1 can be installed."
  else
    echo "$1 cannot be installed."
  fi
  echo
} > "$1.test"  # Redirects output of everything in block to file.

echo "Results of rpm test in file $1.test"

exit 0
