#!/bin/bash

echo "method 1 use \$UID"

ROOT_UID=0

if [ "$UID" -eq "$ROOT_UID" ]
then
  echo "You are root."
else
  echo "You are just an ordinary user."
fi

echo

echo "method 2 use id command"
ROOT_NAME="root"
username=`id -nu`

if [ "$username" = "$ROOT_NAME" ]
then
  echo "You are root."
else
  echo "You are just an ordinary user."
fi

exit 0
