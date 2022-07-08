# Chapter 1: Building Abstractions with Functions
## 1.2 Elements of Programming
### 1.2.6 The Non-Pure Print Function
**The value that `print` returns is always `None`**.
The interactive Python interpreter doesn't automatically print the value `None`.  
## 1.6 Higher-Order Functions
Functions that manipulate functions are called higher-order functions.  
### 1.6.1 Functions as Arguments
```python
def summation(n, term):
    total, k = 0, 1
    while k <= n:
        total, k = total + term(k), k + 1
    return total

def cube(x):
    return x * x * x

def sum_cubes(n):
    return summation(n, cube)
```
### 1.6.2 Functions as General Methods
Some functions express general methods of computation, independent of the particular functions they call.
```python
def improve(update, close, guess=1):
    while not close(guess):
        guess = update(guess)
    return guess

def golden_update(guess):
    return 1/guess + 1

def square_close_to_successor(guess):
    return approx_eq(guess * guess, guess + 1)

def approx_eq(x, y, tolerance=1e-3):
    return abs(x-y) < tolerance

phi = improve(golden_update, square_close_to_successor)
```
This example illustrates two related big ideas in computer science.
1. naming and functions allow us to abstract away a vast amount of complexity.
2. it is only by virtue of the fact that we have an extermely general evaluation procedure for the Python language that small components can be composed into complex processes.
### 1.6.3 Nested Definitions
Above examples have two problems
- One is that the global frame becomes cluttered with names of small functions, which must all be unique.
- Another is that we are constrained by particular function signatures: the `update` argument to `improve` must take exactly one argument.
```python
def sqrt(a):
    def sqrt_update(x):
        return average(x, a/x)
    def sqrt_close(x):
        return approx_eq(x*x, a)
    return improve(sqrt_update, sqrt_close)
```
We require two extensions to our environment model to enable lexical scoping.
1. Each user-defined function has a parent environment: the environment in which it was defined.
2. When a user-defined function is called, its local frame extends its parent environment.
The parent of a function value is the first frame of the environment in which that function was defined.
An environment can consist of an arbitrarily long chain of frames, which always concludes with the global frame.
Two key advantages of lexical scoping in Python.
- The names of a local function do not interfere with names external to the function in which it is defined, because the local function name will be bound in the current local environment in which it was defined, rather than the global environment.
- A local function can access the environment of the enclosing function, because the body of the local function is evaluated in an environment that extends the evaluation environment in which it was defined.
Because they "enclose" information in this way, locally defined functions are often called *closures*.
### 1.6.4 Functions as Returned Values
```python
def square(x):
    return x * x

def successor(x):
    return x + 1

def compose1(f, g):
    def h(x):
        return f(g(x))
    return h

def f(x):
    """Never called"""
    return -x

square_successor = compose1(square, successor)
result = square_successor(12)
```
### 1.6.5 Example: Newton's Method
Newton's method is a classic iterative approach to finding the arguments of a mathematical function that yield a return value of 0. These values are called the *zeros* of the function.
```python
def newton_update(f, df):
    def update(x):
        return x - f(x) / df(x)
    return update

def find_zero(f, df):
    def near_zero(x):
        return approx_eq(f(x), 0)
    return improve(newton_update(f, df), near_zero)

def square_root_newton(a):
    """f(x) = x^2 -a, df(x) = 2*x"""
    def f(x):
        return x * x - a
    def df(x):
        return 2 * x
    return find_zero(f, df)

def power(x, n):
    product, k = 1, 0
    while k <= n:
        product, k = product * x, k + 1
    return product

def nth_root_of_a(n, a):
    """ f(x) = x^n -a, df(x) = n * x^(n-1)"""
    def f(x):
        return power(x, n) - a
    def df(x):
        return n * power(x, n - 1)
    return find_zero(f, df)
```
Newton's method is a powerful general computational method for solving differentiable equations. Very fast algorithms for logarithms and large integer division employ variants of the technique in modern computers.
### 1.6.6 Currying
Given a function `f(x, y)` define a function `g` such that `g(x)(y)` is equivalent to `f(x, y)`. This transformation is called *currying*.
```python
def curried_pow(x):
    """
    >>> curried_pow(2)(3)
    18
    """
    def h(y):
        return pow(x, y)
    return h
``` 
```python
def curry2(f):
    """
    >>> curry2(pow)(2)(5)
    32
    """
    def g(x):
        def h(y):
            return f(x, y)
        return h
    return g

def uncurry2(g):
    """
    >>> uncurry2(curry2(pow))(2, 5)
    def f(x, y):
        return g(x)(y)
    return f
```
### 1.6.7 Lambda Expressions
A lambda expression evaluates to a function that has a single return expression as its body. Assignment and control statements are not allowed.
```python
def compose1(f, g):
    return lambda x: f(g(x))
```
> lambda x: f(g(x)) == A function that takes x and returns f(g(x))
### 1.6.9 Function Decorators
```python
def trace(fn):
    def wrapped(x):
        printf('-> ', fn, '(', x, ')')
        return fn(x)
    return wrapped

@trace
def triple(x):
    return 3 * x

triple(12)
# output:
# -> <function triple at xxxxx> ( 12 ) 
# 36
```
## 1.7 Recursive Functions
A function is called *recursive* if the body of the function calls the function itself, either directly or indirectly.
The operators `%` and `//` can be used to separate a number into two parts: its last digit and all but its last digit.
```
>>> 18181 % 10
1
>>> 18181 // 10
1818
```
```python
def sum_digits(n):
    """Return the sum of the digits of positive integer n."""
    if n < 10:
        return n:
    else:
        all_but_last, last = n // 10, n % 10
        return sum_digit(all_but_last) + last
```
### 1.7.1 The Anatomy of Recursive Functions
A common pattern can be found in the body of many recursive functions.
- begins with a *base case*.
- followed by one or more *recursive calls*.
```python
#iterative function
def fact_iter(n):
    total, k = 1, 1
    while k <= n:
        total , k = total * k, k + 1
    return total

#recursive function
def fact(n):
    if n == 1:
        return 1
    else:
        return n * fact(n - 1)
```
### 1.7.2 Mutual Recursion
When a recursive procedure is divided among two functions that call each other, the functions are said to be *mutually recursive*.
```python
"""Determine whether a number is even or odd."""
def is_even(n):
    if n == 0:
        return True
    else:
        return is_odd(n-1)

def is_odd(n):
    if n == 1:
        return True
    else:
        return is_even(n-1)
```
Turn into a single recursive
```python
def is_even(n):
    if n == 0:
        return True
    else:
        if (n - 1) == 0:
            return False
        else:
            return is_even((n-1)-1)
```
### 1.7.4 Tree Recursion
A function calls itself more than noce.
```python
#Fibonacci numbers
def fib(n):
    if n == 1:
        return 0
    if n == 2:
        return 1
    else:
        return fib(n-2) + fib(n-1)
```
### 1.7.5 Example: Partitions
The number of partitions of a positive integer `n`, using parts up to size `m`, is the number of ways in which `n` can be expressed as the sum of positive integer parts up to `m` in increasing order.
> The number of ways to partition `n` using integers up to `m` equals
1. the number of ways to partition `n-m` using integers up to `m`
2. the number of ways to partition `n` using integers up to `m-1`
```python
def count_partition(n, m):
    if n == 0:
        return 1
    elif n < 0:
        return 0
    elif m == 0:
        return 0
    else:
        return count_partition(n-m, m) + count_partition(n, m - 1)
```
# Appendix
REPL - Read, Evaluate, Print, Loop
