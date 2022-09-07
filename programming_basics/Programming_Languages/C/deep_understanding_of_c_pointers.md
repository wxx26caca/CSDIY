# C pointer

## 1. 认识指针

### 1.1 指针和内存

#### 1.1.8 null 的概念

- null 概念
- null 指针常量
- NULL 宏
- ASCII 字符 NUL
- null 字符串
- null 语句

void 指针 - 可以用来存放任何数据类型的引用。

- void 指针具有和 char 指针相同的形式和内存对齐方式
- void 指针和别的指针永远不会相等，不过，两个赋值为 NULL 的 void 指针是相等的。

任何指针都可以被赋给 void 指针，它可以被转换回原来的指针类型。

### 1.2 指针的类型和长度

#### 1.2.2 指针相关的预定义类型

- size_t - 用于安全地表示长度

    ```c
    #ifdef __SIZE_T
    #define __SIZE_T
    typedef unsigned int size_t;
    #endif
    ```

    `sizeof` 操作符可以用来判断指针的长度。

    ```c
    printf("size of *char: %d\n", sizeof(char*));
    printf("size of *int: %ld\n", sizeof(int*));
    ```

- ptrdiff_t - 用于处理指针算术运算

- intptr_t 和 uintptr_t - 用于存储指针地址。uintptr_t 是 intptr_t 的无符号版本

    ```c
    int num;
    intptr_t *p = &num;
    //uintptr_t *pu = &num; // error, invalid conversion from int* to uintptr_t*
    uintptr_t *pu = (uintptr_t *)&num;
    ```

### 1.3 指针操作符

| 操作符       | 名称                           | 含义                     |
| ------------ | ------------------------------ | ------------------------ |
| *            |                                | 声明指针                 |
| *            | 解引用                         | 解引指针                 |
| ->           | 指向                           | 访问指针引用的结构的字段 |
| +            | 加                             | 对指针做加法             |
| -            | 减                             | 对指针做减法             |
| ==, !=       | 相等，不等                     | 比较两个指针             |
| >, >=, <, <= | 大于，大于等于，小于，小于等于 | 比较两个指针             |
| (数据类型)   | 转换                           | 改变指针的类型           |

| 数据类型 | 长度(字节) |
| -------- | ---------- |
| byte     | 1          |
| char     | 1          |
| short    | 2          |
| int      | 4          |
| float    | 4          |
| long     | 8          |
| double   | 8          |

### 1.4 指针的常见用法

- 多层间接引用
- 常量指针

#### 1.4.1 多层间接引用

```c
char *titles[] = {"A Tale of Two Cities", "Don Quixote", "Odyssey", "Hamlet"}

char **bestBooks[3];
char **englisthBooks[4];

bestBooks[0] = &titles[0];
bestBooks[1] = &titles[2];
bestBooks[2] = &titles[3];

englishBooks[0] = &titles[0];
englishBooks[1] = &titles[1];
englishBooks[2] = &titles[2];
englishBooks[3] = &titles[3];
```

#### 1.4.2 常量指针

- 指向常量的指针

    指针是可变的，但是它指向的数据是不可变的

    ```c
    const int limit = 500;
    
    const int *p = &limit;
    
    p = &num; // 可以赋值
    *p = 200; // error, 不能用指针来修改这个整数
    ```

- 指向非常量的常量指针

    指针是不可变的，但是它指向的数据是可变的

    ```c
    int num;
    int *const p = &num;
    ```

- 指向常量的常量指针

    本身不能修改，它指向的数据也不能修改

    ```c
    const int * const p = &num;
    ```

## 2. C 的动态内存管理

### 2.1 动态内存分配

在 C 语言中动态内存分配的基本步骤有：

1. 用 malloc 类的函数分配内存
2. 用这些内存支持应用程序
3. 用 free 函数释放内存

```c
int *p = (int *)malloc(sizeof(int));
*p = 5;
printf("%d %p\n", *p, p);
free(p);
```

内存泄漏

- 丢失内存地址

    ```c
    char *name = (char*)malloc(strlen("Susan") + 1);
    strcpy(name, "Susan");
    while (*name != 0) {
        printf("%c", *name);
        name++;
    }
    // 每次迭代 name 都会增加 1，最后 name 会指向字符串结尾的 NUL 字符，分配内存的起始地址丢失了？
    ```

- 应该调用 free 函数却没有调用（隐式泄漏）

    - 程序应该释放内存而实际却没有释放，也会发生内存泄漏。
    - 释放用 struct 关键字创建的结构体时也可能发生内存泄漏。如果**结构体包含指向动态分配内存的指针**，那么需要在释放结构体之前先释放这些指针。

### 2.2 动态内存分配函数

`stdlib.h` 中包含了 malloc，realloc，calloc，free 函数

| 函数    | 功能                                                         |
| ------- | ------------------------------------------------------------ |
| malloc  | 从堆上分配内存                                               |
| realloc | 在之前分配的内存块的基础上，将内存重新分配为更大或者更小的部分 |
| calloc  | 从堆上分配内存并清零                                         |
| free    | 将内存块返回堆                                               |

分配的内存会根据指针的数据类型对齐。

#### 2.2.1 malloc

函数原型

```c
void* malloc(size_t);
```

- 如果内存不足，就会返回 NULL。
- 如果传入的参数是负数，也会引发问题。有的系统中，参数是负数会返回 NULL。
- 如果传入的参数是 0，可能返回 NULL 指针，也可能返回一个指向分配了 0 字节区域的指针。
- 如果传入的参数是 NULL，会生成一个警告，返回 0 字节。

典型用法

```c
int *p = (int*)malloc(sizeof(int));
```

执行 malloc 函数时

1. 从堆上分配内存
2. 内存不会被修改或是清空
3. 返回首字节的地址

推荐做法

```c
int *p = (int*)malloc(sizeof(int));
if (p != NULL) { 
	...
} else {
	...
}
```

注意事项

- 显式类型转换可以说明 malloc 函数的用以，可以和 C++ 兼容，推荐。需要引用 malloc 的头文件 **stdlib.h**，否则编译器会报 warning。

    ```
    warning: implicit declaration of function ‘malloc’ [-Wimplicit-function-declaration]
    warning: incompatible implicit declaration of built-in function ‘malloc’
    note: include ‘<stdlib.h>’ or provide a declaration of ‘malloc’
    ```

- 如果声明了一个指针，但没有在使用之前为它指向的地址分配内存，会导致一个无效内存引用。

    ```c
    char *name;
    printf("Enter a name: ");
    scanf("%s", name);
    printf("%s", name);
    
    // output
    // Enter a name: sss
    // (null)
    // 正确做法 char *name = (char*)malloc(sizeof(char));
    ```

    name 所引用的内存，看起来似乎可以正确执行，实际上这块内存还没有分配。

- malloc 函数分配的字节数是由它的参数指定的，所以尽量使用 sizeof 操作符。

- 静态、全局指针

    **初始化**静态或全局变量时候不能调用 malloc 函数。

    ```c
    static int *p = malloc(sizeof(int)); 
    // complile error,  error: initializer element is not constant
    ```

    静态变量可以通过在后面用一个单独的语句给变量分配内存来避免这个问题。

    ```c
    static int *p;
    p = malloc(sizeof(int)); 
    ```

    > 在编译器看来，作为初始化操作符的 = 和作为赋值操作符的 = 不一样。

#### 2.2.2 calloc 函数

分配内存的同时清空内存。清空内存意思是**将其内容置为二进制 0** 。

函数原型

```c
void *calloc(size_t numElements, size_t elementSize);
```

根据 numElements 和 elementSize 的乘积来分配内存，并返回一个指向内存的第一个字节的指针。如果不能分配内存，返回 NULL。

```c
int *p = calloc(5, sizeof(int)); //为 p 分配 20 字节。

int *p = malloc(5 * sizeof(int));
memset(p, 0, 5 * sizeof(int));
```

> 内存需要清零可以使用 calloc，不过执行 calloc 可能比执行 malloc 慢。

#### 2.2.3 realloc 函数

重新分配内存

函数原型

```c
void *realloc(void *ptr, size_t size);
```

第一个参数是指向原来内存块的指针，第二个参数是请求的大小。返回指向重新分配的内存的指针。

| 第一个参数 | 第二个参数   | 行为                                         |
| ---------- | ------------ | -------------------------------------------- |
| 空         | 无           | 同 malloc                                    |
| 非空       | 0            | 原内存块被释放                               |
| 非空       | 比原内存块小 | 利用当前的块分配更小的块                     |
| 非空       | 比原内存块大 | 要么在当前位置，要么在其他位置，分配更大的块 |

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
    char *string1;
    char *string2;
    string1 = (char*) malloc(16);
    strcpy(string1, "0123456789AB");
    string2 = realloc(string1, 8);
    printf("string1 Value: %p [%s]\n", string1, string1);
    printf("string2 Value: %p [%s]\n", string2, string2);
    return 0;
}

/*
output
string1 Value: 0x7ffff19c5260 [0123456789AB]
string2 Value: 0x7ffff19c5260 [0123456789AB]
*/
```

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
    char *string1;
    char *string2;
    string1 = (char*) malloc(16);
    strcpy(string1, "0123456789AB");
    string2 = realloc(string1, 64);
    printf("string1 Value: %p [%s]\n", string1, string1);
    printf("string2 Value: %p [%s]\n", string2, string2);
}

/*
output
string1 Value: 0x7fffbe18e260 [0123456789AB]
string2 Value: 0x7fffbe18e260 [0123456789AB]
*/ 
```

> 与书上结果不符，string2 和 string2 还是分配在一个内存块。

#### 2.2.4 alloca 函数和变长数组

alloca 函数在函数的栈帧上分配内存，函数返回后会自动释放内存。

C99 引入了变长数组（VLA），允许函数内部声明和创建其长度由变量决定的数组。

```c
void compute(int size) {
    char* buffer[size];
    ...
}
```

> 上面这种方式，内存分配在运行时完成，且将内存作为栈帧的一部分来分配。

> VLA 的长度一经分配就固定了。

### 2.3 free

函数原型

```c
void free(void *ptr);
```

> 尽管指针仍然指向这块区域，但是我们应该把它看成指向垃圾数据。

如果传递给 free 的是空指针，它什么都不做。如果传递给 free 的是未经过 malloc 的指针，它的行为将是未定义的。

```c
int main() {
    int num;
    int *p = &num;
    free(p);
}

/*
output
munmap_chunk(): invalid pointer
Aborted (core dumped)
*/
```

> 应该在同一层管理内存的分配和释放。比如，在函数内分配，就应该在函数内释放它。

#### 2.3.1 free 后赋值给指针 NULL

```c
int main() {
    int *p = (int*) malloc(sizeof(int));
    free(p);
    p = NULL;
}
```

> 这样做的目的是为了解决迷途指针类问题。但是不推荐将 NULL 赋给指针。

#### 2.3.2 重复释放

```c
int main() {
    int *p = (int*) malloc(sizeof(int));
    *p = 5;
    free(p);
    free(p);
}

/*
output
free(): double free detected in tcache 2
Aborted (core dumped)
*/
```

```c
int main() {
    int *p1 = (int*) malloc(sizeof(int));
    int *p2 = p1;
    free(p1);
    free(p2);
}

/*
output
free(): double free detected in tcache 2
Aborted (core dumped)
*/
```

堆一般利用操作系统的功能来管理内存。堆的大小可能在程序创建后就固定不变了，也可能可以增长。

是否要在程序终止前释放内存取决于具体的应用程序。

### 2.4 迷途指针

如果**内存已经释放，而指针还在引用原始内存**，这样的指针就称为迷途指针。

可能导致的问题

- 如果访问内存，则行为不可预期
- 如果内存不可访问，则是段错误
- 潜在的安全隐患

#### 2.4.1 示例

```c
int main() {
    int *p1 = (int*) malloc(sizeof(int));
    *p1 = 5;
    printf("address of p1: %p, value: %d\n", p1, *p1);
    free(p1);
    *p1 = 10; // 迷途指针
    printf("address of p1: %p, value: %d\n", p1, *p1);
}

/*
ouput
address of p1: 0x7fffe5266260, value: 5
address of p1: 0x7fffe5266260, value: 10
*/
```

```c
// 指针别名
int main() {
	int *p1 = (int*)malloc(sizeof(int));
    *p1 = 5;
    int *p2;
    p2 = p1;
    free(p1);
    *p2 = 10; // 迷途指针
}
```

```c
// 块语句
int *p1;

void foo(){
    int tmp = 5;
    p1 = &tmp;
}
// 这里 p1 变成了迷途指针
foo()
```

#### 2.4.2 处理迷途指针

- 释放指针后置为 NULL，后续使用这个指针会终止应用程序。
- 写一个特殊函数代替 free 函数。
- 第三方工具检测迷途指针。

#### 2.4.3 调试器对检测内存泄漏的支持

Mudflap 库为 GCC 编译器提供了类似功能，它的运行时库支持对内存泄漏的检测和其它功能，这种检测是通过**监控指针解引操作**来实现的。

### 2.5 动态内存分配技术

- C 的垃圾回收技术

    Boehm-Weiser Collector

- 资源获取即初始化（Resource Acquisition Is Initialization，RAII），用来解决 C++ 中资源的分配和释放。

    GNU 编译器用到 `RAII_VARIABLE` 宏

- 使用异常处理函数

    ```c
    void exceptionExample() {
        int *p = NULL;
        __try {
            p = (int*)malloc(sizeof(int));
            *p = 5;
            printf("p = %d\n", *p);
        }
        __finally {
            free(p);
        }
    }
    ```

## 3. 指针和函数

### 3.1 程序的栈和堆

#### 3.1.1 程序栈

> **局部变量**和**函数参数**分配在栈帧上。

程序栈存放栈帧（stack frame），栈帧有时候也称为活跃记录（activation record）或者活跃帧（activation frame）。

#### 3.1.2 栈帧的组成

- **返回地址** - 函数完成后要返回的程序内部地址

- **局部数据**存储 - 为局部变量分配的内存

- **函数参数**存储 - 为函数参数分配的内存

- **栈指针和基指针** - 运行时系统用来管理栈的指针

    栈指针通常指向栈顶部，基指针通常存在并指向栈帧内部的地址，比如返回地址。

系统在创建栈帧的时候，局部变量，函数参数等是**有序**推入栈中的。

将栈帧推到程序栈上时，系统可能会耗尽内存，这种情况称为栈溢出，通常会导致程序非正常终止。（栈到底有多大呢？）

**每一个线程都有自己的程序栈**。一个或者多个线程访问内存中的同一个对象可能会导致冲突。

### 3.2 通过指针传递和返回数据

#### 3.2.1 用指针传递数据

用指针传递数据的一个主要原因是**函数可以修改数据**。

```c
#include <stdio.h>

void swap(int *p1, int *p2)
{
    int tmp;
    tmp = *p1;
    *p1 = *p2;
    *p2 = tmp;
}

int main()
{
    int n1 = 5;
    int n2 = 10;
    swap(&n1, &n2);
    printf("n1 = %d, n2 = %d\n", n1, n2);
    return 0;
}
```

#### 3.2.2 传递指向常量的指针

- 只传递数据的地址，能避免某些情况下复制大量内存。
- 只传指针，数据就能被修改。
- 如果不希望数据被修改，可以传递指向常量的指针。

```c
#include <stdio.h>

void passingAddressOfConstants(const int *n1, int *n2)
{
    *n2 = *n1;
}

int main()
{
    const int limit = 100;
    int result = 5;
    passingAddressOfConstants(&limit, &result);
    printf("limit = %d, result = %d\n", limit, result);
    return 0;
}
```

#### 3.2.3 返回指针

从函数返回对象时经常用到以下两种技术

- 使用 malloc 在函数内部分配内存并返回其地址。调用者负责释放返回的内存。
- 传递一个对象给函数并让函数修改它。这样分配和释放对象的内存都是调用者的责任。

```c
#include <stdio.h>
#include <stdlib.h>

int* allocateArray(int size, int value)
{
    int *array = (int*)malloc(size * sizeof(int));
    for (int i = 0; i < size; i++)
        array[i] = value;
    return array;
}

int main()
{
    int* vector = allocateArray(5, 45);
    for (int i = 0; i < 5; i++)
        printf("%d\n", vector[i]);
    free(vector); // 调用者 main 需要负责释放内存，否则容易发生内存泄漏
    return 0;
}
```

从函数返回指针可能存在几个潜在问题

- 返回未初始化的指针
- 返回指向无效地址的指针
- 返回局部变量指针
- 返回指针但是没有释放内存

#### 3.2.4 局部数据指针

```c
int* allocateArray(int size, int value)
{
    int array[size];
    for (int i = 0; i < size; i++)
        array[i] = value;
    return array;
}

/*
 warning: function returns address of local variable [-Wreturn-local-addr]
     return array;
            ^~~~~
Segmentation fault (core dumped)
*/
```

上述代码，一旦函数返回，返回的数组地址就无效了，因为函数的栈帧弹出了。后续可能别的函数会覆写变量值。

可以将 array 变量声明为 static。这样会把变量的作用域限制在函数内部，但是分配在栈帧外面，避免其它函数覆写变量值。

静态数组也有不好之处，它限制了函数处理变长数组的能力。

但是如果返回的是不可能被修改的错误码之类的，这么做很有用。

#### 3.2.5 传递空指针

```c
int* allocateArray(int* arr, int size, int value)
{
    if (arr != NULL)
    {
        for (int i = 0; i < size; i++)
        	arr[i] = value;
    }
    return arr;
}

int main()
{
    int* vector = (int*)malloc(5 * sizeof(int));
    allocateArray(vector, 5, 45);
    for (int i = 0; i < 5; i++)
        printf("%d\n", vector[i])
    free(vector);
    return 0;
}
```

如果指针是 NULL，那么什么都不会发生，程序继续执行，不会非正常终止。

#### 3.2.6 传递指针的指针

想修改原指针而不是指针的副本，需要传递指针的指针。

```c
#include <stdio.h>
#include <stdlib.h>

void allocateArray(int **array, int size, int value)
{
    *array = (int*)malloc(size * sizeof(int));
    if (*array != NULL) {
        for (int i = 0; i < size; i++)
            *(*array + i) = value;
    }
}

int main()
{
    int* vector = NULL;
    allocateArray(&vector, 5, 45);
    for (int i = 0; i < 5; i++)
        printf("%d\n", vector[i]);
    free(vector);
    return 0;
}
```

#### 3.2.7 实现自己的 free 函数

free 函数存在一些问题

- 不会检查传入的指针是否为 NULL
- 不会在返回前把指针置为 NULL

```c
void saferFree(void **pp)
{
    if (pp != NULL && *p != NULL)
    {
        free(*pp);
        *pp = NULL;
    }
}

#define safeFree(p) saferFree((void*)&(p))
```

```c
#include <stdio.h>
#include <stdlib.h>
#define safeFree(p) saferFree((void*)&(p))

void saferFree(void **p)
{
    if(p != NULL && *p != NULL)
    {
        free(*p);
        *p = NULL;
    }
}

int main()
{
    int* p = NULL;
    p = (int*)malloc(sizeof(int));
    *p = 5;
    printf("Before: %d %p\n", *p, p);
    safeFree(p);
    printf("After: %d %p\n", *p, p);
    safeFree(p);
    return (EXIT_SUCCESS);
}
```

### 3.3 函数指针

函数指针是指**持有函数地址**的指针。

函数指针可能会导致程序运行变慢，处理器可能无法配合流水线做分支预测。

> 流水线 - 提升处理器性能的硬件技术，通过重叠指令的执行来实现
>
> 分支预测 - 处理器用来推测哪块代码会被执行的技术

#### 3.3.1 声明函数指针

```
void (*foo)()
  ^      ^
  |      |  
返回类型  函数指针变量的名字
```

> 使用函数指针要小心，因为 C 不会检查参数传递是否正确

```c
int* f1();    // f1 是一个函数，返回 int*
int (*f2)();  // f2 是一个函数指针，返回 int
int* (*f3)(); // f3 是一个函数指针，返回 int*
```

#### 3.3.2 使用函数指针

```c
int (*fptr1)(int);

int square(int num)
{
    return num * num;
}

int main()
{
    int num = 5;
    fptr1 = square;
    printf("%d square is %d", num, fptr1(num));
    return 0;
}
```

> 和数组名一样，用函数本身的名字，它会返回函数的地址。

函数会分配在跟程序栈所用段不同的段上。

```c
typedef int (*function)(int);  // 为函数指针声明一个类型定义

int square(int num)
{
    return num * num;
}

int main()
{
    int num = 5;
    function fptr1;  // 使用类型定义
    fptr1 = square;
    printf("%d square is %d", num, fptr1(num));
    return 0;
}
```

#### 3.3.3 传递函数指针

```c
#include <stdio.h>

int add(int num1, int num2)
{
    return num1 + num2;
}

int subtract(int num1, int num2)
{
    return num1 - num2;
}

typedef int (*operator)(int, int);

int compute(operator op, int num1, int num2)
{
    return op(num1, num2);
}

int main()
{
    printf("%d\n", compute(add, 1, 2));
    printf("%d\n", compute(subtract, 1, 2));
    return 0;
}
```

#### 3.3.4 返回函数指针

```c
fptrOperation select(char opcode)
{
    switch(opcode)
    {
        case '+': return add;
        case '-': return subtract;
    }
}

int evaluate(char opcode, int num1, int num2)
{
    fptrOpeartion operation = select(opcode);
    return operation(num1, num2);
}

printf("%d\n", evaluate('+', 1, 3));
printf("%d\n", evaluate('-', 1, 3));
```

#### 3.3.5 使用函数指针数组

```c
typedef int (*operation)(int, int);
operation operation[128] = {NULL};

// or

int (*operation[128])(int, int) = {NULL};
```

#### 3.3.6 比较函数指针

```c
fptrOperation operation = add;
if (operation == add)
{
    printf("operation is add function\n");
} 
else
{
    printf("operation is not add function\n");
}
```

> 比较函数指针用处的一个更现实的例子是，用函数指针数组表示一系列任务步骤的情况。

#### 3.3.7 转换函数指针

> 无法保证函数指针和数据指针相互转换后正常工作。

```c
typedef void (*fptrBase)();

// fptrBase 声明为一个不接受参数也不返回结果的函数指针
```

## 4. 指针和数组

```c
int vector[5];
int vector[5] = {1, 2, 3, 4, 5};
int matrix[2][3] = {{1, 2, 3}, {4, 5, 6}};
int arr3d[3][2][4] = {
	{{1, 2, 3, 4}, {5, 6, 7, 8}},
	{{9, 10, 11, 12}, {13, 14, 15, 16}},
	{{17, 18, 19, 20}, {21, 22, 23, 24}}
};
```

### 4.1 指针表示法和数组

```c
int vector[5] = {1, 2, 3, 4, 5};
int *p = vector;
```

> p 指向的是数组第一个元素而不是指向数组本身的地址
>
> p 的值是第一个元素的地址

只用数组名字，也可以对数组的第一个元素用取地址操作符。

```c
#include <stdio.h>
#include <stdlib.h>

int main()
{
    int vector[5] = {1, 2, 3, 4, 5};
    int* p = vector;
    printf("address of vector: %p\n", &vector);
    printf("address of p: %p\n", p);
    printf("size of vector: %ld; size of p: %ld\n",
            sizeof(vector), sizeof(p));  // printf 指针，应该用 %ld
    return 0;
}

/*
sizeof(vector) = 20;
sizeof(p) = 8;
*/
```

> p = p + 1; 
>
> vector = vector + 1; // 语法错误

### 4.2 用 malloc 创建一维数组

```c
int *p = (int*)malloc(sizeof(int) * 5);
for (int i = 0; i < 5; i++)
    p[i] = i + 1; 
// or *(p+i) = i + 1;
// 解引用 * 的优先级比 + 高
```

### 4.3 用 realloc 调整数组长度

C99 支持变长数组，有些情况下可能比 realloc 函数更好。但是**变长数组只能在函数内部声明**，如果数组的声明周期比函数长，只能用 realloc。

> 从标准输入读取字符并放入缓冲区，缓冲区会包含除最后的回车字符之外的所有字符。

```c
char* getLine(void)
{
    const size_t sizeIncrement = 10;
    char* buffer = (char*)malloc(sizeIncrement);
    char* currentPosition = buffer;
    size_t maximumLength = sizeIncrement;
    size_t length = 0;
    int character;
    
    if (currentPosition == NULL)
        return NULL;
    
    while (1)
    {
        character = fgetc(stdin);
        if (character == '\n')
            break;
        if (++length >= maximumLength)
        {
            char* newBuffer = (char*)realloc(buffer, maximumLength += sizeIncrement);
            if (newBuffer == NULL)
            {
                free(buffer);
                return NULL;
            }
            currentPosition = newBuffer + (currentPosition - buffer);
            buffer = newBuffer;
        }
        *currentPosition++ = character;
    }
    *currentPosition = '\0';
    return buffer;
}
```

> realloc 函数减少指针指向的内存

```c
char* trim(char* phrase)
{
    char* old = phrase;
    char* new = phrase;
    
    while (*old == ' ')
        old++;
    while (*old)
        *(new++) = *(old++);
    
    *new = 0;
    return (char*)realloc(phrase, strlen(phrase) + 1);
}

int main()
{
    char* buffer = (char*)malloc(strlen("  cat") + 1);
    strcpy(buffer, "  cat");
    printf("%s\n", trim(buffer));
}
```

### 4.4 传递一维数组

```c
void displayArray(int arr[], int size)
{
    for (int i = 0; i < size; i++)
    {
        printf("%d\n", arr[i]);
    }
}

int vector[5] = {1, 2, 3, 4, 5};
displayArray(vector, 5);
```

```c
void displayArray(int* arr, int size)
{
    for(int i = 0; i < size; i++)
    {
        printf("%d\n", arr[i]);
    }
}
```

### 4.5 使用指针的一维数组

```c
int* arr[5];
for(int i = 0; i<5; i++)
{
    arr[i] = (int*)malloc(sizeof(int));
    *arr[i] = i;
}

/*
*(arr+i) = (int*)malloc(sizeof(int));
**(arr+i) = i;
*/
```

> arr 是指针数组，所以 arr[i] 返回的是一个地址，即 arr[i] 也是一个指针。

### 4.6 指针和多维数组

```c
int main()
{
    int matrix[2][5] = {{1, 2, 3, 4, 5}, {6, 7, 8, 9,0}};
    for (int i = 0; i < 2; i++)
        for (int j = 0; j < 5; j++)
            printf("matrix[%d][%d] address: %p value: %d\n",
                    i, j, &matrix[i][j], matrix[i][j]);
    return 0;
}
```

> int (*pmatrix)[5] = matrix;
>
> 声明了一个指针处理这个数组

> *(matrix[0]+1) 取到的是 2；而 *(matrix+1) 取到的是 6 的地址，\*\*(matrix + 1) 取到的是 6。

### 4.7 传递多维数组

```c
void display(int arr[][5], int rows){}
void display2(int (*arr)[5], int rows){}
```

```c
void display3DArray(int (*arr)[2][4], int rows)
{
	for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < 2; j++)
        {
            for (int k = 0; k < 4; k++)
            {
                printf("%d ", arr[i][j][k]);
            }
        }
    }
}

display3DArray(arr, 2);
```

### 4.8 动态分配二维数组

- 数组元素是否需要连续
- 数组是否规则

```c
int matrix[2][5] = {{1,2,3,4,5},{6,7,8,9,10}};  // 内存是连续的

// 内存可能不连续的二维数组
int rows = 2;
int columns = 5;
int** matrix = (int**)malloc(rows * sizeof(int*));
for (int i = 0; i < rows; i++)
{
    matirx[i] =  (int*)malloc(columns * sizeof(int));
}
```

用 malloc 为二维数组分配连续内存

```c
int rows = 2;
int columns = 5;
int** matrix = (int**)malloc(rows * sizeof(int*));
matrix[0] = (int*)malloc(rows * columns * sizeof(int));
for (int i = 0; i < rows; i++)
{
    matirx[i] = matrix[0] + i * columns;
}
```

```c
int rows = 2;
int columns = 5;
int* matrix = (int*)malloc(rows * columns * sizeof(int));
for (int i = 0; i < rows; i++)
{
    for (int j = 0; j < columns; j++)
    {
        *(matrix + (i*columns) + j) = i*j;
    }
}
```

### 4.10 不规则数组

**复合字面量**

```c
(const int) {100};
(int[3]) {10, 20, 30};
```

```c
int(*(arr1[])) = {
  (int[]) {0, 1, 2}, 
  (int[]) {3, 4, 5},
  (int[]) {6, 7, 8}};
```

不规则数组

```c
int(*(arr2[])) = {
  (int[]) {0, 1, 2, 3}, 
  (int[]) {4, 5},
  (int[]) {6}};
```

| 类型     | 声明                                  | 访问元素                   |
| -------- | ------------------------------------- | -------------------------- |
| 一维数组 | int* array[5]                         | *array[i] or **(array + i) |
| 二维数组 | int (*matrix)[5] or int matrix\[]\[5] | \*(\*(matrix + i) + j)     |

## 5. 指针和字符串

字符串通常以字符指针的形式传递给函数和从函数返回。

#### 5.1 字符串基础

字符串是以 ASCII 字符 NUL 结尾的字符序列，ASCII 字符 NUL 表示为 \0。

字符串通常存储在数组或者从堆上分配的内存中。

字符数组也可以用来表示布尔值等小的整数单元，以节省内存空间。

- 单字节字符串 - 由 char 数据类型组成的序列 - 在 **string.h** 中
- 宽字符串 - 由 wchar_t 数据类型组成的序列 - 在 **wchar.h** 中

> NULL 和 NUL 不同。NULL 用来表示特殊的指针，通常定义为 ((void*)0)，NUL 是一个 char，定义为 \0

**字符常量是单引号引起来的字符序列**。字符常量通常由一个字符组成，也可以包含转义字符，它们的**类型是 int**。

#### 5.1.1 字符串声明

声明字符串的方式有三种：字面量，字符数组和字符指针。

```c
char header[32];
char *header;
char header = "header";
```

#### 5.1.2 字符串字面量池

字符串字面量一般是分配在只读内存中，所以是不可变的。一般可以像下面这样使用。

```c
const char *tabHeader = "Sound";
*tabHeader = 'L';
printf("%s\n", tabHeader);

/*
test.c: In function ‘main’:
test.c:8:16: error: assignment of read-only location ‘*tabHeader’
     *tabHeader = 'L';
                ^
*/
```

#### 5.1.3 字符串初始化

- 初始化操作符初始化 char 数组

    ```c
    char header[] = "Media Player";
    ```

- 初始化 char 指针

    ```c
    char* header;
    char* header = (char*)malloc(strlen("Media player") + 1); // 堆上和常量池中都有
    char* header = "Media player";  // 只有常量池中有
    ```

- 从标准输入初始化字符串

    ```c
    char* command = (char*)malloc(14);
    printf("Enter a Command: ");
    scanf("%s", command);
    ```

- 字符串位置小结

    ```c
    char* golbalHeader = "Chapter";
    char globalArrayHeader[] = "Chapter";
    
    void displayHeader()
    {
        static char* staticHeader = "Chapter";
        static char staticArrayHeader[] = "Chapter";
        char* localHeader = "Chapter";
        char localArrayHeader[] = "Chapter";
        char* heapHeader = (char*)malloc(strlen("Chapter") + 1);
        strcpy(heapHeader, "Chapter");
    }
    ```

    ![image-20220516140853722](https://s2.loli.net/2022/05/16/xwsUnbSAVu6iJrO.png)

    - 分配在全局内存的字符串会一直存在，也可以被多个函数访问
    - 静态字符串也可以一直存在，不过只有定义它们的函数才能访问
    - 堆上的内存在释放之前也能一直存在，可以被多个函数访问

### 5.2 字符串操作

#### 5.2.1 比较字符串 strcmp

函数原型

```c
int strcmp(const char* s1, const char* s2);
```

按照字典序比较 s1 和 s2。返回值为负数，则是 s1 比 s2 小；返回值为 0，相等；返回值为整数，s1 比 s2 大。

#### 5.2.2 复制字符串 strcpy

函数原型

```c
char* strcpy(char* s1, const char* s2);
```

#### 5.2.3 拼接字符串 strcat

函数原型

```c
char* strcat(char* s1, const char* s2);
```

如果没有为拼接后的字符串分配独立的内存，可能会覆写第一个字符串。

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main()
{
    char* error = "Error:";
    char* errorMessage = "No enough memory";

    strcat(error, errorMessage);
    printf("%s\n", error);
    printf("%s\n", errorMessage);
    return 0;
}

/*
ouput:
Segmentation fault (core dumped)
*/

/*
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main()
{
    char* error = "Error:";
    char* errorMessage = "No enough memory";
    char* buffer = (char*)malloc(strlen(error)+strlen(errorMessage)+1);
    
    strcpy(buffer, error);
    strcat(buffer, errorMessage);
    
    printf("%s", error);
    printf("%s\n", errorMessage);
    return 0;
}
*/
```

拼接字符串应该使用的是**字符字面量**而不是字符串字面量。

```c
char* path = "C:";
char* currentPath = (char*) malloc(strlen(path)+2);
currentPath = strcat(currentPath,"\\");  // error, \\ 会被认为是一个整数
```

### 5.3 传递字符串

#### 5.3.4 给应用程序传递参数

C 中的 main 函数用 argc 和 argv 参数支持命令行参数。argc 是一个整数，指定了传递的参数数量；argv 通常被看做字符串指针的一维数组，每个指针引用一个命令行参数。

```c
int main(int argc, char** argv){...}
int main(int argc, char* argv[]){...}
```

### 5.4 返回字符串

函数返回字符串，实际上返回的是字符串的地址。

- 返回字面量的地址

    ```c
    char* returnALiteral(int code) {
    	switch(code) {
    		case 100:
    			return "Boston Processing Center";
    		case 200:
    			return "Denver Processing Center";
    		case 300:
    			return "Atlanta Processing Center";
    		case 400:
    			return "San Jose Processing Center";
    	}
    }
    ```

- 返回动态分配内存的地址

    ```c
    char* blanks(int number)
    {
        char* spaces = (char*)malloc(number+1);
        for (int i = 0; i < number; i++)
        {
            spaces[i] = ' ';
        }
        spaces[number] = '\0';
        return spaces;
    }
    ```

## 6. 指针和结构体

### 6.1 介绍

结构体声明

- ```c
    struct _person{
        char* firstName;
        char* lastName;
        char* title;
        unsigned int age;
    };
    ```

    ```c
    int main()
    {
        struct person person;
        person.age = 23;
        printf("person age is %d\n", person.age);
    }
    ```

- ```c
    typedef struct _person {
        char* firstName;
        char* lastName;
        char* title;
        unsigned int age;   
    } Person;
    ```

    ```c
    Person *ptrPerson;
    ptrPerson = (Person*)malloc(sizeof(Person));
    ptrPerson->firstName = (char*)malloc(strlen("Bob") + 1);
    ptrPerson->age = 23;
    ```

为结构体分配内存

分配的内存至少是各个字段的长度和。实际长度可能会大于这个和，因为**各个字段之间可能会有填充**。比如，短整数通常对齐到能被 2 整除的地址上，整数对齐到能被 4 整除的地址上。

### 6.2 结构体释放问题

为结构体分配内存时，**系统不会自动为结构体内部的指针分配内存**。所以，当结构体消失的时候，系统也不会自动释放结构体内部的指针指向的内存。

### 6.3 避免 malloc/free 开销

重复分配然后释放结构体会产生一些开销，可能导致性能瓶颈。

解决的一种方式是：为分配的结构体单独维护一个池子。

```c
#define LIST_SIZE 10
Person* list[LIST_SIZE];
// 初始化
for(int i = 0; i < LIST_SIZE; i++)
{
    list[i] = NULL;
}
```

### 6.4 用指针支持数据结构

```c
typedef stuct _employee
{
    char name[32];
    unsigned int age;
} Employee;
```

#### 6.4.1 链表

```c
typedef struct _node
{
    void* data;
    struct _node *next;
} Node;

typedef struct _linkedList
{
    Node *head;
    Node *tail;
    Node *current;
} LinkedList;
```

```c
void initList(LinkedList*);
void addHead(LinkedList*, void*);
void addTail(LinkedList*, void*);
void delete(LinkedList*, Node*);
Node* getNode(LinkedList*, COMPARE, void*);
void displayLinkedList(LinkedList*, DISPLAY);
```

```c
void initList(LinkedList* list)
{
    list->head = NULL;
    list->tail = NULL;
    list->current = NULL;
}
```

```c
void addHead(LinkedList* list, void* data)
{
    Node* node = (Node*)malloc(sizeof(Node));
    node->data = data;
    if(list->head == NULL){
        list->tail = node;
        node->next = NULL;
    } else {
        node->next = list->head;
    }
    list->head = node;
}
```

```c
void addTail(LinkedList* list, void* data)
{
    Node* node = (Node*)malloc(sizeof(Node));
    node->data = data;
    node->next = NULL;
    if (list->head == NULL){
        list->head = node;
    } else {
        list->tail->next = node;
    }
    list->tail = node;
}
```

```c
Node* getNode(LinkedList* list, COMPARE compare, void* data)
{
    Node* node = list->head;
    while(node != NULL){
        if(compare(node->data, data) == 0)
        {
            return node;
        }
        node = node->next;
    }
    return NULL;
}
```

```c
void delete(LinkedList* list, Node* node)
{
    if(node == list->head){
        if(list->head->next == NULL){
            list->head = list->tail = NULL;
        } else {
            list->head = list->head->next;
        }
    } else {
        Node* tmp = list->head;
        while(tmp != NULL && tmp->next != node){
            tmp = tmp->next;
        }
        if (tmp != NULL){
            tmp->next = node->next;
        }
    }
    free(node);
}
```

```c
void displayLinkedList(LinkedList* list, DISPLAY display)
{
    Node* current = list->head;
    while(current != NULL)
    {
        display(current->data);
        current = current->next;
    }
}
```

#### 6.4.2 队列

```c
typedef LinkedList Queue;
```

```c
void* dequeue(Queue* queue)
{
    Node* tmp = queue->head;
    void* data;
    if (queue->head == NULL)
    {
        data = NULL;
    } else if (queue->head == queue->tail)
    {
        queue->head = queue->tail = NULL;
        data = tmp->data;
        free(tmp);
    } else {
        while(tmp->next != queue->tail)
            tmp = tmp->next;
        queue->tail = tmp;
        tmp = tmp->next;
        queue->tail->next = NULL;
        data = tmp->data;
        free(tmp);
    }
    return data;
}

/*
if 队列为空
else if 单元素队列
else 多元素队列
*/
```

#### 6.4.3 栈

```c
typedef LinkedList Stack;
```

```c
void* pop(Stack* stack){
    Node* node = stack->head;
    if(node == NULL)
    {
        return NULL;
    } else if(node == stack->tail){
        stack->head = stack->tail = NULL;
        void* data = node->data;
        free(node);
        return data;
    } else {
        stack->head = stack->head->next;
        void* data = node->data;
        free(node);
        return data;
    }
}
```

#### 6.4.4 树

```c
typedef struct _tree{
    void* data;
    struct _tree *left;
    struct _tree *right;
} TreeNode;
```

```c
void insertNode(TreeNode** root, COMPARE compare, void* data)
{
    TreeNode* node = (TreeNode*)malloc(sizeof(TreeNode));
    node->data = data;
    node->left = NULL;
    node->right = NULL;
    if (*root == NULL){
        *root = node;
        return;
    }
    while(1){
        if(compare((*root)->data, data) > 0){
            if((*root)->left != NULL){
                *root = (*root)->left;
            } else {
                (*root)->left = node;
                break;
            }
        } else {
            if((*root)->right != NULL){
                *root = (*root)->right;
            } else {
                (*root)->right = node;
                break;
            }
        }
    }
}

/*
如果根为空，把新节点赋给 root，然后返回。
如果树非空，程序就进入一个无限循环，直到将新节点插入树中结束。
每次循环迭代都会比较新节点和当前节点，根据比较结果，
将局部 root 指针置为左子节点或者右子节点，这个 root 指针总是指向树的当前节点。
如果左子节点或右子节点为空，那么就将新节点添加为当前节点的子节点，循环结束。
*/
```

```c
void preOrder(TreeNode* root, DISPLAY display){
    if(root != NULL){
        display(root->data);
        preOrder(root->left, display);
        preOrder(root->right, display);
    }
}

void inOrder(TreeNode* root, DISPLAY display){
    if(root != NULL){
        inOrder(root->left, display);
        display(root->data);
        inOrder(root->right, display);
    }
}

void postOrder(TreeNode* root, DISPLAY display){
    if(root != NULL){
        postOrder(root->left, display);
        postOrder(root->right, display);
        display(root->data);
    }
}
```

## 7. 安全问题和指针误用

[CERT组织](http://www.cert.org/) 可以了解到 C 和其它语言安全问题全面解决方案的好来源。

操作系统（OS）已经引入了一些安全改进，有些改进反映在内存的使用方式上。尽管这些改进通常超出了开发者的控制范围，但是它们确实会影响程序。理解这些问题有助于解释应用程序的行为。我们会把精力集中在**地址空间布局随机化**和**数据执行保护**上。
地址空间布局随机化 （Address Space Layout Randomization，ASLR）过程会**把应用程序的数据区域随机放置在内存中**，这些数据区域包括代码、栈和堆。随机放置这些区域导致攻击者更难预测内存的位置，从而更难利用它们。有些类型的攻击（比如说 return-to-libc 攻击），会覆写栈的一部分，然后把控制转移到这个区域。这个区域经常是共享 C 库 libc。如果栈和 libc 的位置是未知的，这类攻击的成功率就会降低。
**如果代码位于内存的不可执行区域， 数据执行保护 （Data Execution Prevention，DEP）技术会阻止执行这些代码**。在有些类型的攻击中，恶意代码会覆写内存的某个区域，然后将控制转移到这个区域。如果这个区域（比如栈或是堆）的代码不可执行，那么恶意代码就无法执行了。这种技术可以用硬件实现，也可以用软件实现。

### 7.1 指针的声明和初始化

```c
// 同一行中把两个变量都声明为指针
int *p1, *p2;
// 用类型定义替代宏定义
typedef int* PINT;
PINT ptr1, ptr2;
```

处理未初始化指针的方法

- 总是用 NULL 来初始化指针

    ```c
    int *p = NULL;
    if(p != NULL) {...} else {...}
    ```

- 用 assert 函数

    ```c
    #include <assert.h>
    assert(p != NULL)
    ```

- 第三方工具

### 7.2 指针的使用问题

很多安全问题聚焦的是**缓冲区溢出**的概念。

- 发生在应用程序地址空间以外的内存

    操作系统会发出一段错误然后终止程序。这类攻击不会获取未授权的访问，但会试图搞垮应用程序甚至服务器。

- 发生在应用程序的地址空间内

    会导致对数据的未授权访问或控制转移到其它代码段，可能攻陷系统。

- 发生在栈帧的元素上，可能把栈帧的返回地址部分覆写为对同一时间创建的恶意代码的调用

    函数返回时会将控制转移到恶意函数，该函数可以执行任何操作，只受限于当前用户的特权等级。

可能导致缓冲区溢出的情况

- 访问数组元素时没有检查索引值
- 对数组指针做指针算术运算时不够小心
- 用 gets 这样的函数从标准输入读取字符串
- 误用 strcpy 和 strcat 这样的函数

1. 使用 malloc 这类函数的时候一定要检查返回值，否则可能会导致程序非正常终止

2. 指针的解引用和赋值不一样

3. 迷途指针

4. 越界访问数组内存

5. 错误计算数组长度

6. 错误使用 sizeof 操作符

    ```c
    int buffer[20];
    int *pbuffer = buffer;
    // sizeof(buffer) = 20*4 = 80
    // sizeof(buffer)/sizeof(int) = 20
    ```

7. 匹配指针类型，强制类型转换可能有问题

8. 有界指针

    有界指针是指指针的使用被限制在有效的区域内

9. 字符串安全问题

10. 指针算术运算和结构体

11. 函数指针问题

### 7.3 内存释放问题

- 重复释放

    避免这类漏洞的简单办法是释放指针后总是将其置为 NULL

- 清除敏感数据

    一旦不需要内存中的敏感数据，立马进行覆写

### 7.4 静态分析工具

- GCC -Wall

## 8. 其他

### 8.1 转换指针

转换指针对包括：**访问有特殊目的的地址**；**分配一个地址来表示端口**；**判断机器的字节序**等方面很有帮助。

> 句柄：是系统资源的引用，对资源的访问通过句柄实现。

```c
int num = 0x12345678;
char *pc = (char*)&num;
for (int i = 0; i < 4; i++)
{
    printf("%p: %02x\n", pc, (unsigned char) *pc++);
}
```

### 8.2 别名，强制名和 restrict 关键字

用 restrict 关键字可以在声明指针时告诉编译器这个指针没有别名，这样就允许编译器产生更高效的代码。

restrict关键字隐含了两层含义：
1. 对于编译器来说，这意味着它可以执行某些代码优化；
2. 对于程序员来说，这意味着这些指针不能有别名，否则操作的结果将是**未定义**的。

### 8.3 线程和指针

### 8.4 面向对象

C 中的多态

```c
typedef struct _shape {
    vFunction functions;
    int x;
    int y;
} Shape;
```

```c
typedef void (*fptrSet)(void* int);
typedef int (*fptrGet)(void*);
typedef void (*fptrDisplay)();

typedef struct _functions {
    fptrGet getX;
    fptrGet getY;
    fptrSet setX;
    fptrSet setY;
    fptrDisplay display;
} vFunctions;
```

```c
void shapeDisplay(Shape *shape) { printf("Shape\n");}
void shapeSetX(Shape *shape, int x) {shape->x = x;}
void shapeSetY(Shape *shape, int y) {shape->y = y;}
int shapeGetX(Shape *shape) { return shape->x;}
int shapeGetY(Shape *shape) { return shape->y;}
```

```c
Shape* getShapeInstance() {
	Shape *shape = (Shape*)malloc(sizeof(Shape));
	shape->functions.display = shapeDisplay;
	shape->functions.setX = shapeSetX;
	shape->functions.getX = shapeGetX;
	shape->functions.setY = shapeSetY;
	shape->functions.getY = shapeGetY;
	shape->x = 100;
	shape->y = 100;
	return shape;
}

Shape *sptr = getShapeInstance();
sptr->functions.setX(sptr,35);
sptr->functions.display();
printf("%d\n", sptr->functions.getX(sptr));
```

```c
typedef struct _rectangle {
	Shape base;
	int width;
	int height;
} Rectangle;
```

```c
void rectangleSetX(Rectangle *rectangle, int x) {
	rectangle->base.x = x;
}
void rectangleSetY(Rectangle *rectangle, int y) {
	rectangle->base.y;
}
int rectangleGetX(Rectangle *rectangle) {
	return rectangle->base.x;
}
int rectangleGetY(Rectangle *rectangle) {
	return rectangle->base.y;
}
void rectangleDisplay() {
	printf("Rectangle\n");
}
```

```c
Rectangle* getRectangleInstance() {
	Rectangle *rectangle = (Rectangle*)malloc(sizeof(Rectangle));
	rectangle->base.functions.display = rectangleDisplay;
	rectangle->base.functions.setX = rectangleSetX;
	rectangle->base.functions.getX = rectangleGetX;
	rectangle->base.functions.setY = rectangleSetY;
	rectangle->base.functions.getY = rectangleGetY;
	rectangle->base.x = 200;
	rectangle->base.y = 200;
	rectangle->height = 300;
	rectangle->width = 500;
	return rectangle;
}

Rectangle *rptr = getRectangleInstance();
rptr->base.functions.setX(rptr,35);
rptr->base.functions.display();
printf("%d\n", rptr->base.functions.getX(rptr));
```
