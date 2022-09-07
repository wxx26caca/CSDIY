# Python 进阶

## 装饰器

### Python 中一切皆对象

Python 中所有的对象都有属性和方法，也就是可以用过 `.` 去获取它的属性或调用它的方法

### 闭包

Python 中允许在一个方法中嵌套另一个方法，这种特殊的机制就叫做闭包，这个内部方法可以保留外部方法的作用域，尽管外部方法不是全局的，内部方法也可以访问到外部方法的参数和变量

```python
import time

def timeit(func):
    def inner():
        start = time.time()
        func()
        stop = time.time()
        print('duration time %ds', int(stop-start))
    return inner

def hello():
    time.sleep(1)
    print('hello')

hello = timeit(hello)
hello()
```

### 装饰器

```python
@timeit
def hello():
    time.sleep(1)
    print("hello")

hello() # 相当于 hello = timeit(hello)
```

### functools.wraps

```python
import time
from functools import wraps

def timeit(func):
    @wraps(func)
    def inner():
        start = time.time()
        func()
        stop = time.time()
        print('duration time %ds', int(stop-start))
    return inner

@timeit
def hello():
    time.sleep(1)
    print("hello")

print(hello.__name__)
```

### 装饰带参数的方法

```python
import time
from functools import wraps

def timeit(func):
    @wraps(func)
    def inner(*args, **kwargs):  # 使用 *args, **kwargs 适应所有参数
        start = time.time()
        func(*args, **kwargs)    # 传递参数给真实调用的方法
        end = time.time()
        print 'duration time: %ds' % int(end - start)
    return inner

```

### 带参数的装饰器

```python
import time
from functools import wraps

def timeit(prefix):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            func(*args, **kwargs)
        return inner
    return decorator
```

### 类实现装饰器

```python
import time
from functools import wraps

class TimeIt(object):
    def __init__(self, prefix):
        self.prefix = prefix
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
        return wrapper

@TimeIt('prefix')
def hello():
    time.sleep(1)
    print("hello")
```

### 装饰器的应用

使用装饰器的好处是，可以把我们的业务逻辑和控制逻辑分离开，业务开发人员可以更好地关注业务逻辑，装饰器可以方便地实现对控制逻辑的统一定义，这种方式也遵循了设计模式中的单一职责。

- 记录调用日志

    ```python
    import logging
    from functools import wraps
    
    def logging(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 记录调用日志
            logging.info('call method: %s %s %s', func.func_name, args, kwargs)
            return func(*args, **kwargs)
        return wrapper
    ```

- 记录方法执行耗时

    ```python
    from functools import wraps
    
    def timeit(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            duration = int(time.time() - start) # 统计耗时
            print 'method: %s, time: %s' % (func.func_name, duration)
            return result
        return wrapper
    ```

- 记录方法执行次数

    ```python
    from functools import wraps
    
    def counter(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            wrapper.count = wrapper.count + 1   # 累计执行次数
            print 'method: %s, count: %s' % (func.func_name, wrapper.count)
            return func(*args, **kwargs)
        wrapper.count = 0
        return wrapper
    ```

- 本地缓存

    ```python
    from functools import wraps
    
    def localcache(func):
        cached = {}
        miss = object() 
        @wraps(func)
        def wrapper(*args):
            result = cached.get(args, miss)
            if result is miss:
                result = func(*args)
                cached[args] = result
            return result
        return wrapper
    ```

- 路由映射

    ```python
    class Router(object):
    
        def __init__(self):
            self.url_map = {}
    
        def register(self, url):
            def wrapper(func):
                self.url_map[url] = func
            return wrapper
    
        def call(self, url):
            func = self.url_map.get(url)
            if not func:
                raise ValueError('No url function: %s', url)
            return func()
    
    router = Router()
    
    @router.register('/page1')
    def page1():
        return 'this is page1'
    
    @router.register('/page2')
    def page2():
        return 'this is page2'
    
    print(router.call('/page1'))
    print(router.call('/page2'))
    ```

- 权限校验

- 上下文管理

## Python 中的魔法方法

- 构造与初始化

    - `__init__`

        ```python
        class Person(object):
        
            def __init__(self, name, age):
                self.name = name
                self.age = age
        ```

    - `__new__`

        ```python
        class Person(object):
        
            def __new__(cls, *args, **kwargs):
                print "call __new__"
                return object.__new__(cls, *args, **kwargs)
        
            def __init__(self, name, age):
                print "call __init__"
                self.name = name
                self.age = age
        ```

    - `__del__`

        ```python
        class Person(object):
            def __del__(self):
                print '__del__'
        ```

    - `__init__` 与 `__new__` 的区别

        - `__new__` 的第一个参数是 `cls`，`__init__` 的第一个参数是 `self`
        - `__new__` 返回值是一个实例对象，而 `__init__` 没有任何返回值，只做初始化操作
        - `__new__` 由于返回的是一个实例对象，所以它可以给所有实例进行**统一**的初始化操作
        - `__new__` 优先于 `__init__` 调用

    - `__new__` 的应用场景

        - 实现一个单例类

            ```python
            class Singleton(object):
                _instance = None
                def __new__(cls, *args, **kwargs):
                    if not cls._instance:
                        cls._instance=super(Singleton,cls).__new__(cls,*args,**kwargs)
                    return cls._instance
            class Person(Singleton):
                pass
            a = Person()
            b = Person()
            print(assert a is b) # True
            ```

        - 继承内置类，比如 `int` `str` `tuple` 等

            ```python
            class g(float):
                def __new__(cls, kg):
                    return float.__new__(cls, kg*2)
            ```

        - 配合元类使用

    - `__del__` 

        `__del__` 这个方法就是我们经常说的「析构方法」，也就是在**对象被垃圾回收时被调用**。

        但是请注意，当我们执行 `del obj` 时，这个方法不一定会执行。

        由于 Python 是通过**引用计数**来进行垃圾回收的，如果这个实例在执行 `del` 时，还被其他对象引用，那么就不会触发执行 `__del__` 方法。

        通常来说，`__del__` 这个方法我们很少会使用到，除非需要在显示执行 `del` 执行特殊清理逻辑的场景中才会使用到。

        当我们在对文件、Socket 进行操作时，如果要想安全地关闭和销毁这些对象，最好是在 `try` 异常块后的 `finally` 中进行关闭和释放操作，从而避免资源的泄露。

- 类的表示

    - `__str__` / `__repr__`
    - `__unicode__`
    - `__hash__` / `__eq__`
    - `__nozero__`
    
- `__slots__`

    ```python
    class Parent:
        __slots__ = 'parent', 'parent1'
    
    class Children(Parent):
        __slots__ = 'children', 'children1'
    
    class Children2(Children):
        __slots__ = 'children2'
    
    
    child = Children()
    child.parent = 'p'
    child.children2 = 'c2' 
    # AttributeError: 'Children' object has no attribute 'children2'
    # 只可以给继承的父类 __slots__ 里的属性赋值，不能给子类里的赋值
    print(child.children2)
    ```

    

### Purpose of return self python

https://stackoverflow.com/questions/43380042/purpose-of-return-self-python/43380360

```python
class Counter(object):
    def __init__(self, start=1):
        self.val = start
    def increament(self):
        self.val += 1
        return self
    def decreament(self):
        self.val -= 1
        return self
c = Counter()
c.increament().increament().increament()
```

### super

python3: you can just say `super().__init__()` instead of `super(ChildB, self).__init__()` which IMO is quite a bit nicer.

`super(childB, self).__init__()` 首先找到 childB 的父类，然后把类 childB 的对象转换成 parent 的对象

## 多线程

### threading join 方法

1. 当一个进程启动之后，会默认产生一个主线程，因为线程是程序执行流的最小单元，当设置多线程时，主线程会创建多个子线程，在python中，默认情况下（其实就是setDaemon(False)），主线程执行完自己的任务以后，就退出了，此时子线程会继续执行自己的任务，直到自己的任务结束

2. 当我们使用setDaemon(True)方法，设置子线程为守护线程时，主线程一旦执行结束，则全部线程全部被终止执行，可能出现的情况就是，子线程的任务还没有完全执行结束，就被迫停止

3. join所完成的工作就是线程同步，即主线程任务结束之后，进入阻塞状态，一直等待其他的子线程执行结束之后，主线程再终止

```python
import threading
import time

def run():
    time.sleep(2)
    print('当前线程的名字是： ', threading.current_thread().name)
    time.sleep(2)


if __name__ == '__main__':
    start_time = time.time()
    print('这是主线程：', threading.current_thread().name)
    
    thread_list = []
    for i in range(5):
        t = threading.Thread(target=run)
        thread_list.append(t)

    for t in thread_list:
        t.setDaemon(True)
        t.start()

    for t in thread_list:
        t.join()

    print('主线程结束了！' , threading.current_thread().name)
    print('一共用时：', time.time()-start_time)
```

