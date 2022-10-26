#!/bin/bash
#  Tip:
#  If you're unsure how a certain condition might evaluate,
#+ test it in an if-test.

echo "Testing \"0\""
if [ 0 ]
then
  echo "0 is true."
else
  echo "0 is false."
fi

echo

echo "Testing \"1\""
if [ 1 ]
then
  echo "1 is true."
else
  echo "1 is false."
fi

echo

echo "Testing \"-1\""
if [ -1 ]
then
  echo "-1 is true."
else
  echo "-1 is false."
fi

echo

echo "Testing \"NULL\""
if [ ]
then
  echo "NULL is true."
else
  echo "NULL is false."
fi

echo

echo "Testing \"xyz\""
if [ xyz ]
then
  echo "Random string is true."
else
  echo "Random string is false."
fi

echo

# Tests if $xyz is null, it's an uninitialized variable.
echo "Testing \"\$xyz\""
if [ $xyz ]
then
  echo "Uninitialized variable is true."
else
  echo "Uninitialized variable is false."
fi

echo

echo "Testing \"-n \$xyz\""
if [ -n "$xyz" ]
then
  echo "Uninitialized variable is true."
else
  echo "Uninitialized variable is false."
fi

echo

xyz=          # Initialized, but set to null value.

echo "Testing \"-n \$xyz\""
if [ -n "$xyz" ]
then
  echo "Null variable is true."
else
  echo "Null variable is false."
fi

echo

echo "Testing \"false\""
if [ "false" ]
then
  echo "\"false\" is true."
else
  echo "\"false\" is false."
fi

echo

echo "Testing \"\$false\""
if [ "$false" ]
then
  echo "\"\$false\" is true."
else
  echo "\"\$false\" is false."
fi

echo

echo "Testing \"\$true\""
if [ "$true" ]
then
  echo "\"\$true\" is true."
else
  echo "\"\$true\" is false."
fi

exit 0

# output
# Testing "0"
# 0 is true.

# Testing "1"
# 1 is true.

# Testing "-1"
# -1 is true.

# Testing "NULL"
# NULL is false.

# Testing "xyz"
# Random string is true.

# Testing "$xyz"
# Uninitialized variable is false.

# Testing "-n $xyz"
# Uninitialized variable is false.

# Testing "-n $xyz"
# Null variable is false.

# Testing "false"
# "false" is true.

# Testing "$false"
# "$false" is false.

# Testing "true"
# "true" is true.

# Testing "$true"
# "$true" is false.
