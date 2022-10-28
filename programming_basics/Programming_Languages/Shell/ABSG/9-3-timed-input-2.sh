#!/bin/bash

INTERVAL=5

timedout_read() {
  timeout=$1
  name=$2
  old_tty_settings=`stty -g`
  stty -icanon min 0 time ${timeout}0
  eval read $name      # or just  read $name
  stty "$old_tty_settings"
  # See man page for "stty."
}

echo; echo -n "What's your name? Quick! "
timedout_read $INTERVAL your_name

echo

if [ ! -z "$your_name" ]
then
  echo "your name is $your_name"
else
  echo "Timed out."
fi

echo

exit 0
