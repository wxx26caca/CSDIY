# Chapter2: Building Abstractions with Data
## 2.1 Introduction
### 2.1.1 Native Data Types
Every value in Python has a *class* that determines what type of value it is.
Native data types have following properties:
1. There are expressions that evaluate to values of native types, called *literals*.
2. There are built-in functions and operators to manipulate values of native types.
Python includes thress native numberic types: integers `int`, real numbers `float` and complex numbers `complex`.
```python
>>> type(2)
<class 'int'>
>>> type(1.2)
<class 'float'>
>>> type(1+2j)
<class 'complex'>
```
`float` values should be treated as approximations to real values. These approximations have only a finite amount of precision.
```python
>>> 7 / 3 * 3
7.0
>>> 1 / 3 * 7 * 3
6.999999999999999
>>> 1 / 3 == 0.3333333333333333 # Beware of float approximation
True
```
## 2.2 Data Abstraction
The basic idea of data abstraction is to structure programs so that they operate on abstract data.
### 2.2.1 Example: Rational Numbers
A rational number is typically written as: `numerator/denominator`.
Actually dividing integers produces a `float` approximation, losing the exact precision of integers.
Assume that the constructor and selectors are available as the following three functions:
- `rational(n, d)` returns the rational number with numerator `n` and denominator `d`.
- `numer(x)` returns the numerator of the rational number `x`.
- `denom(x)` returns the denominator of the rational number `x`.
```python
def add_rationals(x, y):
    nx, dx = numer(x), denom(x)
    ny, dy = numer(y), denom(y)
    return rational(nx * dy + ny * dx, dx * dy)

def mul_rationals(x, y):
    return rational(numer(x) * numer(y), denom(x) * denom(y))

def print_rationals(x):
    print(numer(x), '/', denom(x))

def rationals_are_equal(x, y):
    return numer(x) * denom(y) == numer(y) * denom(x)
```
### 2.2.2 Pairs
A compound structure called a `list`, which can be constructed by placing expressions within square brackets separated by commas.
```python
>>> pair = [10, 20]
>>> x, y = pair
>>> x
10
>>> y
20
>>> pair[0]
10
>>> pair[1]
20
>>> from operator import getitem
>>> getitem(pair, 0)
10
>>> getitem(pair, 1)
20
```
We can represent a rational number as a pair of two integers.
```python
def rational(n, d):
    return [n, d]

def number(x):
    return x[0]

def denom(x):
    return x[1]

# use gcd library
from fractions import gcd
def rational(n, d):
    g = gcd(n, d)
    return (n//g, d//g)
```
> floor division operator, `//` expresses integer division, which rounds down the fractional part of the result of division.
### 2.2.3 Abstraction Barriers
An abstraction barrier violation occurs whenever a part of the program that can use a higher level function instead uses a function in a lower level.
Abstraction barriers make programs easier to maintain and to modify.
```python
def square_rational(x):
    return mul_rational(x, x)

def square_rational_violating_once(x):
    return rational(numer(x) * numer(x), denom(x) * denom(x))

def square_rational_violating_twice(x):
    return [x[0] * x[0], x[1] * x[1]]
```
### 2.2.4 The Properties of Data
## 2.3 Sequences
A sequence is an ordered collection of values. There are many kinds of sequences, but they all share common behavior.
- **Length**. A sequence has a finite length. An empty sequence has length 0.
- **Element selection**. Starting at 0 for the first element.
### 2.3.1 List
- The built-in `len` function returns the length of a sequence.
- List can be added together and multiplied by integers.
- List can including another list.
```python
>>> digits = [1, 2, 8]
>>> len(digits)
3
>>> digits[2]
8
>>> [3, 4] + digits * 2
[3, 4, 1, 2, 8, 1, 2, 8]
>>> pairs = [[10, 20], [30, 40]]
>>> pairs[0]
[10, 20]
>>> pairs[0][1]
20
```
### 2.3.2 Sequence Iteration
```python
def count(s, value):
    """count the number of occurrences of value in sequence s."""
    total, index = 0, 0
    while index < len(s):
        if s[index] == value:
            total = total + 1
        index = index + 1
    return total
```
```python
def count(s, value):
    """count the number of occurrences of value in sequence s."""
    total = 0
    for elem in s:
        if elem == value:
            total = total + 1
    return total
```
A `for` statement consists of a single clause with the form:
```
for <name> in <expression>:
    <suite>
```
A `for` statement is executed by the following procedure:
1. Evaluate the header `<expression>`, which must yield an iterable value.
2. For each element value in that iterable value, in order:
   1. Bind `<name>` to that value in the current frame.
   2. Execute the `<suite>`.
The pattern of binding multiple names to multiple values in a fixed-length sequence is called *sequence unpacking*.
A `range` is another built-in type of sequence of Python, [first, end).
A common convention is to use a *single underscore* character for the name in the `for` header if the name is unused in the suite.
### 2.3.3 Sequence Processing
**List Comprehensions**. Many sequence processing operations can be expressed by evaluating a fixed expression for each element in a sequence and collecting the resulting values in a result sequence.
The general form of a list comprehension is:
`[<map expression> for <name> in <sequence expression> if <filter expression>]`
```python
>>> odds = [1, 3, 5, 7, 9]
>>> [x+1 for x in odds]
[2, 4, 6, 8, 10]
>>> [x for x in odds if 25 % x == 0]
[1, 5]
```
**Aggregation**. Another common sequence processing is to aggregate all values in a sequence into a single value. The built-in functions `sum`, `min` and `max` are all examples of aggregation functions.
```python
>>> def divisors(n):
        return [1] + [x for x in range(2, n) if n % x == 0]
>>> divisors(12)
[1, 2, 3, 4, 6]
>>> [n for n in range(1, 1000) if sum(divisors(n)) == n]
[6, 28, 496]
```
**Higher-order Functions**. The common patterns we have observed in sequence processing can be expressed using higher-order functions.
```python
def apply_to_all(map_fn, s):
    return [map_fn(x) for x in s]

def keep_if(filter_fn, s):
    return [x for x in s if filter_fn(x)]

def reduce(reduce_fn, s, initial):
    reduced = initial
    for x in s:
        reduced = reduce_fn(reduced, x)
    return reduced

def divisors_of(n):
    divides_n = lamda x: n % x == 0
    return [1] + keep_if(divides_n, range(2, n))

from operator import add
def sum_of_divisors(n):
    return reduce(add, divisors_of(n), 0)

reduce(mul, [2, 4, 8], 1)
# output: 64
```
**Conventional Names**. In Python, the built-in `map` and `filter` are generalizations of these functions that do not return lists.
```python
apply_to_all = lambda map_fn, s: list(map(map_fn, s))
keep_if = lambda filter_fn, s: list(filter(filter_fn, s))
```
### 2.3.4 Sequence Abstraction
**Membership**. Python has two operators `in` and `not in` that evaluate to `True` or `False` depending on whether an element appears in a sequence.
**Slicing**. 
### 2.3.5 Strings
### 2.3.6 Trees
```python
def tree(root_label, branches=[]):
    for branch in branches:
        assert is_tree(branch), 'branches must be trees'
    return [root_label] + list(branches)

def label(tree):
    return tree[0]

def branches(tree):
    return tree[1:]

def is_tree(tree):
    if type(tree) != list or len(tree) < 1:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True

def is_leaf(tree):
    return not branches(tree)
```
The nth Fibonacci tree has a root label of the nth Fibonacci number and, for `n > 1`, two branches that are also Fibonacci trees.
```python
def fib_tree(n):
    if n == 0 or n == 1:
        return tree(n)
    else:
        left, right = fib_tree(n-2), fib_tree(n-1)
        fib_n = label(left) + label(right)
        return tree(fib_n, [left, right])
```
```python
def count_leaves(tree):
    """Count the leaves of a tree"""
    if is_leaf(tree):
        return 1
    else:
        branch_counts = [count_leaves(b) for b in branches(tree)]
        return sum(branch_counts)
```
**Partition trees**. A partition tree for `n` using parts up to size `m` is a binary (two branch) tree that represents the choices taken during computation. In a non-leaf partition tree:
- the left (index 0) branch contains all ways of partitioning `n` using at least one `m`
- the rgith (index 1) branch containts partitions using parts up to `m-1`
- the root label is `m`
The labels at the leaves of a partition tree express whether the path from the root of the tree to the leaf represents a successful partition of `n`.
```python
def partition_tree(n, m):
    """Return a partition tree of n using parts of up to m."""
    if n == 0:
        return tree(True)
    elif n < 0 or m == 0:
        return tree(False)
    else:
        left = partition_tree(n-m, m)
        right = partition_tree(n, m-1)
        return tree(m, [left, right])
```
Printing the partitions from a partition ree is another tree-recursive process that traverses the tree, constructing each partition as a list. Whenever a `True` leaf is reached, the partition is printed.
```python
def print_parts(tree, partition=[]):
    if is_leaf(tree):
        if label(tree):
            print(' + '.join(partition))
    else:
        left, right = branches(tree)
        m = str(label(tree))
        print_parts(left, partition + [m])
        print_parts(right, partition)
```
### 2.3.7 Linked Lists
```python
# define a value 'empty' represents an empty linked list.

empty = 'empty'
def is_link(s):
    """s is a linked list if it is empty or a (first, rest) pair."""
    return s == empty or (len(s) == 2 and is_link(s[1]))

def link(first, rest):
    """Construct a linked list from its first element and the rest."""
    assert is_link(rest), "rest must be a linked list."
    return [first, rest]

def first(s):
    """Return the first element of a linked list s."""
    assert is_link(s), "first only applies to linked lists."
    assert s != empty, "empty linked list has no first element."
    return s[0]

def rest(s):
    """Return the rest of the elements of a linked list s."""
    assert is_link(s), "rest only applies to linked lists."
    assert s != empty, "empty linked list has no rest."
    return s[1]

def len_link(s):
    """Return the length of linked list s."""
    length = 0
    while s != empty:
        s, length = rest(s), length + 1
    return length

def getitem_link(s, i):
    """Return the element at index i of linked list s."""
    while i > 0:
        s, i = rest(s), i - 1
    return first(s)
```
**Recursive manipulation**.
```python
def len_link_recursive(s):
    """Return the length of a linked list s."""
    if s == empty:
        return 0
    return 1 + len_link_recursive(rest(s))

def getitem_link_recursive(s, i):
    """Return the element at index i of linked list s."""
    if i == 0:
        return first(s)
    return getitem_link_recursive(rest(s), i - 1)
```
Transforming and combining linked lists use recursion.
```python
def extend_link(s, t):
    """Return a list with the elements of s followed by those of t."""
    assert is_link(s) and is_link(t)
    if s == empty:
        return t
    else:
        return link(first(s), extend_link(rest(s), t))

def apply_to_all_link(f, s):
    """Apply f to each element of s."""
    assert is_link(s)
    if s == empty:
        return s
    else:
        return link(f(first(s)), apply_to_all_link(f, rest(s)))

def keep_if_link(f, s):
    """Return a list with elements of s for which f(element) is true."""
    assert is_link(s)
    if s == empty:
        return s
    else:
        kept = keep_if_link(f, rest(s))
        if f(first(s)):
            return link(first(s), kept)
        else:
            return kept

def join_link(s, separator):
    """Return a string of all elements in s separated by separator."""
    if s == empty:
        return ""
    elif rest(s) == empty:
        return str(first(s))
    else:
        return str(first(s) + separator + join_link(rest(s), separator))

def partitions(n, m):
    """Return a linked list of partition of n using parts of up to m.
    Each partition is represented as a linked list.
    """
    if n == 0:
        return link(empty, empty)
    elif n < 0 or m == 0:
        return empty
    else:
        using_m = partitions(n-m, m)
        with_m = apply_to_all_link(lambda s: link(m, s), using_m)
        without_m = partitions(n, m-1)
        return extend_link(with_m, without_m)

def print_partitions(n, m):
    lists = partitions(n, m)
    strings = apply_to_all_link(lambda s: join_link(s, "+"), lists)
    print(join_link(strings, "\n"))
```
