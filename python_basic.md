# Python基础

## Python基础

### 三元运算

### 什么是 GIL 全局解释器锁

### 解释一下 Python 中的继承

### help() 和 dir() 函数

### 什么是猴子补丁

### *args 和 **kwargs 的含义

### 正索引和负索引

### join() 和 split() 函数

### 怎么移除一个字符串的前导、后导空格

### Python 中的闭包、装饰器是什么

### Python 中的数据类型

### Python 中的不可变集合 (frozenset) 是什么

### 什么是 lambda 表达式

### 什么是递归、生成器、迭代器以及它们之间的区别

### yield 的用法

### Python 的参数传递机制

### 元类

## 参考答案

- 三元运算符

    [on true] if [expression] else [on false]

    如果 expression 为 true 则返回前面 [on true],否则返回 [on false]

- GIL -- Global Interpreter Lock

    计算机程序设计语言解释器用于同步线程的一种机制，它使得**任何时候仅有一个线程在执行**，即便在多核处理器上，使用 GIL 的解释器也只允许同一时间执行一个线程。（CPython）

- Python 中的继承

    - 子类会继承父类的所有类成员（属性和方法）
    - MRO（Method Resolution Order），**Python 允许一个类继承多个父类**，他们的继承顺序可以查看`classname.__mro__` 或者 `classname.mro()`得到

- help() 和 dir()

    help() -- 一个内置函数，用来查看函数或者模块的说明

    dir() -- 内置函数，不带参数时候，返回当前范围内的变量、方法和定义的类型列表；带参数时，返回参数的属性、方法列表

- 猴子补丁

    **动态的属性的替换，即运行时动态改变方法、类的方法**

    ```python
    class A:
        def func(self):
            print("Hi")
    	def monkey(self):
        	print("Hi monkey")
    a = A()
    A.func = A.monkey
    a.func()
    # output: Hi monkey
    ```

- join() 和 split()

    join() 将指定字符添加到字符串

    ```
    # example
    a = ('test', 'db')
    x = "#".join(a)
    
    # definition
    string.join(iterable)
    
    # CPython source code /Objects/stringlib/join.h
    ```

    split() 用指定字符分割字符串

    ```c
    # example
    txt = "welcome to the jungle"
    x = txt.split()
    
    # definition
    string.split(separator, maxsplit)
    
    # CPython source code
    # https://stackoverflow.com/questions/40332743/source-code-for-str-split
    
    {
    i = j = 0;
    while (maxcount-- > 0) {
        /* 每遇到一个前导空格，计数器 i 就加 1 */
        while (i < str_len && STRINGLIB_ISSPACE(str[i]))
            i++;
        /* 如果字符串只包含空白，退出循环 */
        if (i == str_len) break;
    
        /* 前导空格之后,遇到非空格字符的时候，计数器 i 加 1
           如果在 i == str_len 之前结束,则说明它指向了一下空白字符 */
        j = i; // 将 i 赋值给 j，保存 i 的位置
        i++;
        while (i < str_len && !STRINGLIB_ISSPACE(str[i]))
            i++;
    #ifndef STRINGLIB_MUTABLE
        /* 如果不能拆分则返回字符串本身 */
        if (j == 0 && i == str_len && STRINGLIB_CHECK_EXACT(str_obj)) {
            /* 没有空格，直接返回 list[0] */
            Py_INCREF(str_obj);
            PyList_SET_ITEM(list, 0, (PyObject *)str_obj);
            count++;
            break;
        }
    #endif
        /* Make the split based on the incremented counters. */
        SPLIT_ADD(str, j, i);
    }
    
    if (i < str_len) {
            /* Only occurs when maxcount was reached */
            /* Skip any remaining whitespace and copy to end of string */
            while (i < str_len && STRINGLIB_ISSPACE(str[i]))
                i++;
            if (i != str_len)
                SPLIT_ADD(str, i, str_len);
        }
        FIX_PREALLOC_SIZE(list);
        return list;
    
      onError:
        Py_DECREF(list);
        return NULL;
    }
    
    #define SPLIT_APPEND(data, left, right)         \
        sub = STRINGLIB_NEW((data) + (left),        \
                            (right) - (left));      \
        if (sub == NULL)                            \
            goto onError;                           \
        if (PyList_Append(list, sub)) {             \
            Py_DECREF(sub);                         \
            goto onError;                           \
        }                                           \
        else                                        \
            Py_DECREF(sub);
    
    #define SPLIT_ADD(data, left, right) {          \
        sub = STRINGLIB_NEW((data) + (left),        \
                            (right) - (left));      \
        if (sub == NULL)                            \
            goto onError;                           \
        if (count < MAX_PREALLOC) {                 \
            PyList_SET_ITEM(list, count, sub);      \
        } else {                                    \
            if (PyList_Append(list, sub)) {         \
                Py_DECREF(sub);                     \
                goto onError;                       \
            }                                       \
            else                                    \
                Py_DECREF(sub);                     \
        }                                           \
        count++; }
    ```

- string.lstrip() and string.rstrip()

- 闭包、装饰器

    当一个嵌套函数在其外部区域引用了一个值时，该嵌套函数就是一个闭包，与装饰器联系

    ```python
    from functools import wraps
    
    def decorator(func, *args, **kwargs):
        @warps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
        return wrapper
    ```

- 数据类型

    Numbers（数字）、Strings（字符串）、List（列表）、Tuples（元组）、Dictionary（字典）、Set 

- 集合

    集合是无序的，所以无法索引它。不可变集合是不可变的，无法改变它的值，所以也无法作为字典的键值

- lambda 表达式

    如果我们只需要一个单一表达式的函数，可以匿名它

    ```python
    (lambda a,b: a if (a>b) else b)(3,4)
    fib = (lambda n: n if n<=2 else fib(n-1)+fib(n-2))
    ```

- 生成器和迭代器的区别

    - 使用生成器时，我们创建一个函数；使用迭代器时，使用内置函数iter()和next() 

    - 生成器中，我们使用关键字`yield`来每次生成/返回一个对象。每次 `yield` 暂停循环时，生成器会保存本地变量的状态
    - 迭代器并不会使用局部变量，它只需要一个可迭代对象进行迭代
    - 使用类可以实现你自己的迭代器，但无法实现生成器
    - 生成器运行速度快，语法简洁，更简单；迭代器更能节约内存

- yield 的用法

    yield 其实就是一个生成器，这样的函数记住上次返回时在函数体中的位置，下一次执行时，从该位置的下一行代码开始执行

- Python 的参数传递机制

    Python使用按**引用传递**（pass-by-reference）将参数传递到函数中。如果你改变一个函数内的参数，会影响到函数的调用。这是Python的默认操作。不过，如果我们传递字面参数，比如字符串、数字或元组，它们是按值传递，这是因为它们是不可变的

    python不允许程序员选择采用传值还是传引用。Python参数传递采用的肯定是“传对象引用”的方式。这种方式相当于传值和传引用的一种综合。如果函数**收到的是一个可变对象**（比如字典或者列表）的引用，就能修改对象的原始值，**相当于通过“传引用”来传递对象**。如果函数**收到的是一个不可变对象**（比如数字、字符或者元组）的引用，就不能直接修改原始对象，**相当于通过“传值'来传递对象**

- 元类

    默认的元类为 type

    如果我们想控制类的创建，需要将类的元类指为我们自定义的元类，这个自定义的元类需要继承type元类。

    ```python
    class Base:
        a = 1
        b = 2
        print('class defined')
        def __new__(cls, *args, **kwargs):
            print(cls.__name__, 'class instance created')
            return super().__new__(cls)
        def __init__(self):
            print(type(self).__name__, 'class instance inited')
        def hello(self):
            print("Hello")
    b = Base()
    ```


## Python内存管理

在 Python 中，内存管理涉及到一个**包含所有 Python 对象和数据结构的私有堆**（heap）。这个私有堆的管理由内部的 Python 内存管理器保证。Python 内存管理器有不同的组件来处理各种动态存储管理方面的问题，如共享，分割，预分配或缓存。

在最底层，一个原始内存分配器通过与操作系统的内存管理器交互，确保私有堆中有足够的空间来存储所有与 Python 相关的数据。在原始内存分配器的基础上，几个对象特定的分配器在同一堆上运行，并根据每种对象类型的特点实现不同的内存管理策略。eg：整数对象不同于字符串、元组或字典

Python **堆内存的管理是由解释器来执行，用户对它没有控制权**，即使他们经常操作指向堆内内存块的对象指针。

Python 对象和其他内部缓冲区的堆空间分配是由 Python 内存管理器按需通过 Python/C API 函数进行的。

某些情况下，Python 内存管理器可能会触发或不触发适当操作，如垃圾回收、内存压缩或者其他预防性操作。

### 内存池机制

Python 中分为大内存和小内存，以 256K 作为界限，大内存使用 malloc 函数进行分配，free 函数进行释放；小内存使用内存池进行分配，调用 malloc 函数分配内存，每次只会分配 256K 大小的内存，不会调用 free 函数释放内存，将该内存块留在内存池中以便下次使用。

最底层是操作系统分配内存，最上层是用户对 Python 对象的直接操作。

### 垃圾回收

Python 中主要通过**引用计数**进行垃圾回收

```c
typedef struct_object{
    int ob_refcnt;
    struct_typeobject *ob_type;
}PyObject;
```

引用计数加一的情况：对象被创建（a=2）、对象被引用（b=a）、对象被作为参数传入一个函数、对象作为一个元素存储在容器中

引用计数减一的情况：对象别名被显示销毁（del）、对象别名被赋予新的对象、一个对象离开了它的作用域、对象所在的容器被销毁或者是从容器中删除对象

```python
import sys
sys.getrefcount(a)
```

引用计数的缺点：逻辑简单，但实现麻烦；在某些场景，比如释放一个大的字典的时候，会比较慢；循环引用

### 标记清除

Python 采用**标记清除**解决容器对象可能产生的循环引用问题，比如列表、字典、用户自定义类的对象、元组等。

该算法在进行垃圾回收时分成了两步，分别是：

- A）标记阶段，遍历所有的对象，如果是可达的（reachable），也就是还有对象引用它，那么就标记该对象为可达；
- B）清除阶段，再次遍历对象，如果发现某个对象没有标记为可达，则就将其回收。

在标记清除算法中，为了追踪容器对象，需要每个容器对象维护两个额外的指针，用来将容器对象组成一个双端链表，指针分别指向前后两个容器对象，方便插入和删除操作。python解释器(Cpython)维护了两个这样的双端链表，**一个链表存放着需要被扫描的容器对象，另一个链表存放着临时不可达对象**。

**垃圾回收的阶段，会暂停整个应用程序，等待标记清除结束后才会恢复应用程序的运行。**

### 分代回收

在循环引用对象的回收中，整个应用程序会被暂停，为了减少应用程序暂停的时间，Python 通过**分代回收**以空间换时间的方法提高垃圾回收效率。

分代回收是基于这样的一个统计事实，对于程序，存在一定比例的内存块的生存周期比较短，而剩下的内存块，生存周期比较长，甚至会从程序开始一直持续到程序结束。生存周期较短的对象比例通常在 80%~90%之间，也就是说**对象存在时间越长，越不可能是垃圾，应该越少去收集。这样在标记清除算法时可以有效减小遍历的对象数，从而提高垃圾回收的速度**。

python gc给对象定义了三种世代(0,1,2),每一个新生对象在generation zero中，如果它在一轮gc扫描中活了下来，那么它将被移至generation one,在那里他将较少的被扫描，如果它又活过了一轮gc,它又将被移至generation two，在那里它被扫描的次数将会更少。

gc的扫描的触发条件：**当某一世代中被分配的对象与被释放的对象之差达到某一阈值的时候，就会触发gc对某一世代的扫描。**值得注意的是**当某一世代的扫描被触发的时候，比该世代年轻的世代也会被扫描。**也就是说如果世代2的gc扫描被触发了，那么世代0,世代1也将被扫描，如果世代1的gc扫描被触发，世代0也会被扫描。

```python
import gc
gc.get_threshold() 
# gc模块中查看阈值的方法,default (200,10,10)
# gc.set_threshold(threashold0[,threashold1[,threashold2]])
# gc.get_threshold(threashold0,threashold1,threashold2)
gc.collect()       # 手动启动垃圾回收
```

[参考文章1](https://andrewpqc.github.io/2018/10/08/python-memory-management/)

[参考文章2](https://www.cnblogs.com/geaozhang/p/7111961.html)

## GIL:全局解释器锁

## 深拷贝和浅拷贝

## 数据类型对比

## 进程、线程、协程

## 上下文管理 with

## 几个高阶函数 map reduce filter sorted

## 设计模式

