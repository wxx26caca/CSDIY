#!/bin/bash

TIMER_INTERRUPT=14
TIMELIMIT=3

PrintAnswer() {
  if [ "$answer" = TIMEOUT ]
  then
    echo $answer
  else
    echo "Your favorite veggie is $answer"
    kill $!      # $! is PID of last job running in background.
  fi
}

TimerOn() {
  sleep $TIMELIMIT && kill -s 14 $$ &
  # Waits 3 seconds, then sends sigalarm to script.
}

Int14Vector() {
  answer="TIMEOUT"
  PrintAnswer
  exit $TIMER_INTERRUPT
}

trap Int14Vector $TIMER_INTERRUPT
# Timer interrupt (14) subverted for our purposes.

echo "What is your favorite vegetable "
TimerOn
read answer
PrintAnswer

exit 0
