#!/bin/bash
# Greatest common divisor 
# Uses Euclid's algorithm
# 辗转相除法

#  Euclid's algorithm uses successive division.
#    In each pass,
#+      dividend <---  divisor
#+      divisor  <---  remainder
#+   until remainder = 0.
#    The gcd = dividend, on the final pass.

# Argument check
ARGS=2
E_BADARGS=85

if [ $# -ne "$ARGS" ]
then
  echo "Usage: `basename $0` first-number second-number"
  exit $E_BASARGS
fi

gcd() {
  dividend=$1
  divisor=$2
  remainder=1
  
  until [ "$remainder" -eq 0 ]
  do
    let "remainder = $dividend % $divisor"
    dividend=$divisor
    divisor=$remainder
  done
}

gcd $1 $2

echo; echo "GCD of $1 and $2 = $dividend"; echo

exit 0
