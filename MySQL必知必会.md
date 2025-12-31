DDL ---- Data Definition Language
DML ---- Data Manipulation Language
DCL ---- Data Control Language
DQL ---- Data Query Language

DBMS ---- DataBase Management System
DBS ---- Database System

- 实体 - 关系图 : 实体就是要管理的对象，属性是标识每个实体的属性，关系是对象之间的关系

- SQL 在 Oracle 中的执行过程：

    ```
    # insert pic
    ```

    软解析：在库缓存中查找，如果存在 SQL 语句的执行计划，就直接拿来执行
    硬解析：创建解析树进行解析，生成执行计划，进入优化器

    可以通过绑定变量来减少硬解析，减少 Oracle 的解析工作量，但是会使 SQL 的执行效率不同，优化比较难。

    ```mysql
    select * from player where player_id = 1000;
    select * from player where player_id = :player_id;  //使用了绑定变量
    ```

- SQL 在 MySQL 的执行过程：

    - MySQL 是典型的 C/S 架构，服务器端程序使用 mysqld
    - MySQL 由三层组成：
        连接层 ---- 客户端发送 SQL 到服务器端
        SQL 层 ---- 对 SQL 语句进行查询处理
        存储引擎层 ---- 负责数据的读取和存储

    - MySQL8.0 以下的版本会有查询缓存，因为查询缓存效率不高，8.0 之后就抛弃了这个功能

    - MySQL 的存储引擎采用插件形式，常见的存储引擎：InnoDB, MyISAM, Memory, NDB, Archive

- 在 MySQL 中分析一条 SQL 语句的执行时间
    开启 profiling，它可以让 MySQL 收集在 SQL 执行时所使用的资源情况。

    ```mysql
    mysql> select @@profiling;  // 查看profiling值
    mysql> set profiling=1;     // 开启profiling
    mysql> show profile;        // 获取上一次查询的执行时间
    mysql> show profile for query 2  // 查询指定的Query ID
    mysql> select version();    // 查看MySQL版本
    ```

- DDL 基础语法

    ```mysql
    CREATE
      CREATE TABLE [table_name] (字段名 数据类型 ……)
      
    CREATE TABLE player (
    	player_id int(11) NOT NULL AUTO_INCREMENT,
    	player_name varchar(255) NOT NULL
    );
    
    DROP
    
    ALTER 
    ALTER TABLE player ADD (age int(11));
    ALTER TABLE player RENAME COLUMN age to player_age;
    ALTER TABLE player MODIFY (player_age float(3,1));
    ALTER TABLE player DROP COLUMN player_age;
    ```

- 数据表常见约束
    - 主键约束、外键约束
    - 唯一性约束
    - NOT NULL 约束
    - DEFAULT
    - CHECK 约束

- SQL 查询语法
    起别名：

    ```mysql
    SELECT name AS n, hp_max AS hm, mp_max AS mm, attack_max AS am, defense_max AS dm FROM heros;
    ```

    查询常数：

    ```mysql
    SELECT 'wangzherongyao' as platform, name FROM heros;
    ```

    去重复行：

    ```mysql
    SELECT DISTINCT attack_range FROM heros; 
    ```

    - DISTINCT 需要放到所有列的前面
    - DISTINCT 其实是对后面所有列名的组合进行去重

    排序检索数据：ORDER BY

    ```mysql
    SELECT name,hp_max FROM heros ORDER BY ha_max DESC;
    ```

    - ORDER BY 后面可以有一个或多个列名，如果是多个列名进行排序，会按照后面第一个列先进行排序，当第一列的值相同的时候，再按照第二列进行排序，以此类推。
    - ORDER BY 后面可以注明排序规则，ASC 代表递增排序，DESC 代表递减排序。如果没有注明排序规则，默认情况下是按照 ASC 递增排序。
    - ORDER BY 可以使用非选择列进行排序，所以即使在 SELECT 后面没有这个列名，你同样可以放到 ORDER BY 后面进行排序。
    - ORDER BY 通常位于 SELECT 语句的最后一条子句，否则会报错。

    约束返回结果数量：LIMIT

    ```mysql
    SELECT name,ha_max FROM heros ORDER BY hp_max DESC LIMIT 5;
    ```

- FileSort 和 Index 排序

    - Index 排序中，索引可以保证数据的有序性，不需要再进行排序，效率更高。

    - FileSort 排序则一般在内存中进行排序，占用 CPU 较多。如果待排结果较大，会产生临时文件 I/O 到磁盘进行排序的情况，效率较低。

        ORDER BY 子句时，应该尽量使用 Index 排序，避免使用 FileSort 排序。

        当然你可以使用 explain 来查看执行计划，看下优化器是否采用索引进行排序。

- SELECT 执行顺序
    - 关键字顺序：
        SELECT ... FROM ... WHERE ... GROUP BY ... HAVING ... ORDER BY ...
    - 语句执行顺序：
        FROM > WHERE > GROUP BY > HAVING > SELECT 字段 > DISTINCT > ORDER BY > LIMIT
    - 在 SELECT 语句执行这些步骤的时候，每个步骤都会产生一个虚拟表，然后将这个虚拟表传入下一个步骤中作为输入。

- SELECT 数据过滤条件

    ```mysql
    SELECT name,hp_max FROM heros WHERE hp_max > 600;
    SELECT name,hp_max, mp_max FROM heros WHERE (hp_max+mp_max) > 8000 OR hp_max > 6000 AND mp_max>1700 ORDER BY (hp_max+mp_max) DESC;
    SELECT name FROM heros WHERE name LIKE '%abc%'
    ```


    Note: WHERE 字句中同时存在 AND 和 OR 时，AND 的执行优先级高

- SQL 函数

    - 算术函数
    - 字符串函数
    - 日期函数
    - 转换函数
    - 聚集函数
        - COUNT()  总行数
        - MAX()    最大值
        - MIN()    最小值
        - SUM()    求和
        - AVG()    平均值

    ```mysql
    SELECT COUNT(*) as num, role_main, role_assist FROM heros GROUP BY role_main,role_assist HAVING num>5 ORDER BY num DESC;
    ```

    Note : WHERE是用于数据行，HAVING作用于分组

- 关联子查询和非关联子查询
    EXISTS 子查询
    IN 子查询

    ```mysql
    SELECT * FROM A WHERE cc IN (SELECT cc FROM B);
    SELECT * FROM A WHERE EXIST (SELECT cc FROM B WHERE B.cc=A.cc);
    ```

    > 实际上在查询过程中，在我们对 cc 列建立索引的情况下，我们还需要判断表 A 和表 B的大小。
    > 如果表 A 比表 B 大，那么 IN 子查询的效率要比 EXIST 子查询效率高，因为这时 B 表中如果对 cc 列进行了索引，那么 IN 子查询的效率就会比较高。
    > 如果表 A 比表 B 小，那么使用 EXISTS 子查询效率会更高，因为我们可以使用到 A 表中对 cc 列的索引，而不用从 B 中进行 cc 列的查询。

- 几种连接 SQL 92

    - 笛卡尔积
        假设有两个集合 X 和 Y，那么 X 和 Y 的笛卡尔积就是 X 和 Y 的所有可能组合，也就是第一个对象来自于 X，第二个对象来自于 Y 的所有可能。

    - 等值连接
        两张表的等值连接就是用两张表中都存在的列进行连接。

        ```mysql
        SELECT player_id, player.team_id, player_name, height, team_name FROM player, team WHERE player.team_id = team.team_id;
        SELECT player_id, a.team_id, player_name, height, team_name FROM player AS a, team AS b WHERE a.team_id = b.team_id;
        ```

    - 非等值连接

    - 外连接

        - 左外连接，就是指左边的表是主表，需要显示左边表的全部行，而右侧的表是从表，（+）表示哪个是从表。

            ```mysql
            SELECT * FROM player, team where player.team_id = team.team_id(+);
            ```

        - 右外连接，指的就是右边的表是主表，需要显示右边表的全部行，而左侧的表是从表。

            ```mysql
            SELECT * FROM player, team where player.team_id(+) = team.team_id;
            ```

    - 自连接

- SQL99

    - 交叉连接 CROSS JOIN

        ```mysql
        SELECT * FROM player CROSS JOIN team;
        ```

    - 自然连接 NATURAL JOIN

        ```
        SELECT player_id, team_id, player_name, height, team_name FROM player NATURAL JOIN team;
        ```

    - ON 连接

        ```mysql
        SELECT player_id, player.team_id, player_name, height, team_name FROM player JOIN team ON player.team_id=team.team_id;
        ```

    - USING 连接

        ```mysql
        SELECT player_id, team_id, player_name, height, team_name FROM player JOIN team USING(team_id);
        ```

    - 外连接

        - LEFT JOIN

            ```mysql
            SELECT * FROM player LEFT JOIN team ON player.team_id = team.team_id;
            ```

        - RIGHT JOIN

            ```mysql
            SELECT * FROM player RIGHT JOIN team ON player.team_id = team.team_id;
            ```

        - FULL JOIN

            ```mysql
            SELECT * FROM player FULL JOIN team ON player.team_id = team.team_id;
            ```

    - 自连接

- 视图 （虚表）

    通常视图用于查询，临时表是真实存在的数据表，当关闭连接时，临时表会自动释放

    创建视图

    ```mysql
    CREATE VIEW view_name AS
    SELECT column1, column2
    FROM table
    WHERE condition
    ```

    嵌套视图

    修改视图

    ```mysql
    ALTER VIEW view_name AS
    SELECT column1, column2
    FROM table
    WHERE condition
    ```

    删除视图

    ```mysql
    DROP VIEW view_name
    ```

- 存储过程 （程序化的SQL）
    存储过程实际上由SQL语句和流程控制语句共同组成

    ```mysql
    CREATE PROCEDURE 存储过程名称([参数列表])
    BEGIN
        需要执行的语句
    END    
    ```

    因为默认情况下 SQL 采用（；）作为结束符，这样当存储过程中的每一句 SQL 结束之后，采用（；）作为结束符，就相当于告诉 SQL 可以执行这一句了。
    但是存储过程是一个整体，我们不希望 SQL 逐条执行，而是采用存储过程整段执行的方式，
    因此我们就需要临时定义新的 DELIMITER，新的结束符可以用（//）或者（$$）。

    ```mysql
    DELIMITER //
    CREATE PROCEDURE `add_num`(IN n INT)
    BEGIN
        DECLARE i INT;
        DECLARE sum INT;
        SET i = 1;
      	SET sum = 0;
        WHILE i <= n DO
            SET sum = sum + i;
            SET i = i +1;
        END WHILE;
        SELECT sum;
    END //
    DELIMITER ;
    ```

- 事务 （transaction）
    是进行一次处理的基本单元，要么完全执行，要么都不执行

    - 事务的特性：ACID
        - 原子性（Atomicity）。原子的概念就是不可分割，你可以把它理解为组成物质的基本单位，也是我们进行数据处理操作的基本单位。
        - 一致性（Consistency）。一致性指的就是数据库在进行事务操作后，会由原来的一致状态，变成另一种一致的状态。也就是说当事务提交后，或者当事务发生回滚后，数据库的完整性约束不能被破坏。
        - 隔离性（Isolation）。它指的是每个事务都是彼此独立的，不会受到其他事务的执行影响。也就是说一个事务在提交之前，对其他事务都是不可见的。 
        - 持久性（Durability）。事务提交之后对数据的修改是持久性的，即使在系统出故障的情况下，比如系统崩溃或者存储介质发生故障，数据的修改依然是有效的。因为当事务完成，数据库的日志就会被更新，这时可以通过日志，让系统恢复到最后一次成功的更新状态。

    ```mysql
    show engines;  // 查看mysql支持的存储引擎有哪些
    ```

    - START TRANSACTION 或者 BEGIN，作用是显式开启一个事务。
        COMMIT：提交事务。当提交事务后，对数据库的修改是永久性的。
        ROLLBACK 或者 ROLLBACK TO [SAVEPOINT]，意为回滚事务。意思是撤销正在进行的所有没有提交的修改，或者将事务回滚到某个保存点。
        SAVEPOINT：在事务中创建保存点，方便后续针对保存点进行回滚。一个事务中可以存在多个保存点。
        RELEASE SAVEPOINT：删除某个保存点。
        SET TRANSACTION，设置事务的隔离级别。
    - 使用事务有两种方式，分别为隐式事务和显式事务。
        隐式事务实际上就是自动提交，Oracle 默认不自动提交，需要手写 COMMIT 命令，而 MySQL 默认自动提交

    ```mysql
    mysql> set autocommit=0; //关闭自动提交
    
    CREATE TABLE test(name varchar(255), PRIMARY KEY (name)) ENGINE=InnoDB;
    BEGIN;
    INSERT INTO test SELECT '关羽';
    COMMIT;
    BEGIN;
    INSERT INTO test SELECT '张飞';
    INSERT INTO test SELECT '张飞';
    ROLLBACK;
    SELECT * FROM test;
    ```

    - MySQL 中 completion_type 参数的作用，实际上这个参数有 3 种可能：
        completion=0，这是默认情况。也就是说当我们执行 COMMIT 的时候会提交事务，在执行下一个事务时，还需要我们使用 START TRANSACTION 或者 BEGIN 来开启。
        completion=1，这种情况下，当我们提交事务后，相当于执行了 COMMIT AND CHAIN，也就是开启一个链式事务，即当我们提交事务之后会开启一个相同隔离级别的事务（隔离级别会在下一节中进行介绍）。
        completion=2，这种情况下 COMMIT=COMMIT AND RELEASE，也就是当我们提交后，会自动与服务器断开连接。

    ```mysql
    SET @@completion_type = 1;
    ```

- 事务隔离
    事务并发处理时会存在的异常情况
    
    - 脏读(Dirty Read) -- 读到了其他事务还没有提交的数据
    - 不可重复读(Nnrepeatable Read) -- 对某数据进行读取，发现两次读取的结果不同。这是因为有其他事务对这个数据同时进行了修改或删除
    - 幻读(Phantom Read) -- 事务 A 根据条件查询得到了 N 条数据，但此时事务 B 更改或者增加了 M 条符合事务 A 查询条件的数据，这样当事务 A 再次进行查询的时候发现会有 N+M 条数据，产生了幻读。
    
    4种隔离级别从低到高：读未提交、读已提交、可重复读、可串行化

|          | 脏读 | 不可重复读 | 幻读 |
| -------- | ---- | ---------- | ---- |
| 读未提交 | 允许 | 允许       | 允许 |
| 读已提交 | 禁止 | 允许       | 允许 |
| 可重复读 | 禁止 | 禁止       | 允许 |
| 可串行化 | 禁止 | 禁止       | 禁止 |

- 游标
    可以从数据结果集合中每次取一条数据记录进行操作
    游标是一种临时的数据库对象，可以指向存储在数据库表中的数据行指针

    使用游标的步骤

    - 第一步，定义游标。 DECLARE cursor_name CURSOR FOR select_statement
        要使用 SELECT 语句来获取数据结果集，而此时还没有开始遍历数据，这里 select_statement 代表的是 SELECT 语句。
        DECLARE cur_hero CURSOR FOR SELECT hp_max FROM heros;
    - 第二步，打开游标。 OPEN cursor_name 当我们定义好游标之后，如果想要使用游标，必须先打开游标。
    - 第三步，从游标中取得数据。 FETCH cursor_name INTO var_name ...这句的作用是使用 cursor_name 这个游标来读取当前行，并且将数据保存到 var_name 
    - 第四步，关闭游标。 CLOSE cursor_name。
    - 最后一步，释放游标。 DEALLOCATE cursor_namec 

- 用 Python 操作 MySQL

    python DB api 规范
    数据库连接对象 connection
    数据库交互对象 cursor
    数据库异常类   exceptions

    mysql-connector是mysql官方提供的驱动器

- 使用Python ORM 框架操作 MySQL
    ORM == Object Relation Mapping（对象关系映射）

    Django

    SQLALchemy

    peewee

- 数据库调优

    选择合适的DBMS
    表设计优化：三范式、反范式优化、表字段数据类型选择
    逻辑查询优化：对查询进行重写
    物理查询优化：创建索引、确定访问
    加缓存：Redis、mMmcached
    库级优化：主从复制、mysql自带的分区表、垂直切分、水平切分

- Redis vs Memcached

    它们都可以将数据存放到内存中

    - 从可靠性来说，Redis 支持持久化，可以让我们的数据保存在硬盘上，不过这样一来性能消耗也会比较大；Memcached 仅仅是内存存储，不支持持久化
    - 从支持的数据类型来说，Redis 比 Memcached 要多，它不仅支持 key-value 类型的数据，还支持 List，Set，Hash 等数据结构，当我们有持久化需求或者是更高级的数据处理需求的时候，就可以使用 Redis；如果是简单的 key-value 存储，则可以使用 Memcached

- 数据表的范式（NF）
    1NF、2NF、3NF、BCNF(巴斯-科德范式)、4NF、5NF

    1NF 需要保证表中每个属性都保持原子性
    2NF 需要保证表中的非主属性与候选键完全依赖  --  一张表只表达一个意思
    3NF 需要保证表中的非主属性与候选键不存在传递依赖。
    BCNF，也叫做巴斯 - 科德范式，它在 3NF 的基础上消除了主属性对候选键的部分依赖或者传递依赖关系。

    数据表中常用的键：
    超键  --  能唯一标识元组的属性集
    候选键  --  不包含多余属性的超键
    主键  --  候选键中的一个
    外键  --  不是表1主键但是是表2主键的表1属性集
    主属性  --  包含在任一候选键中的属性
    非主属性  --  不包含在任何一个候选键中的属性

- 乐观锁和悲观锁并不是锁，而是锁的设计思想
    乐观锁（Optimistic Locking）认为对同一数据的并发操作不会总发生，属于小概率事件，不用每次都对数据上锁，也就是不采用数据库自身的锁机制，而是通过程序来实现。在程序上，我们可以采用**版本号机制或者时间戳机制**实现。
    乐观锁**适合读操作多的场景，相对来说写的操作比较少**。它的优点在于程序实现，不存在死锁问题，不过适用场景也会相对乐观，因为它阻止不了除了程序以外的数据库操作。
    悲观锁（Pessimistic Locking）也是一种思想，对数据被其他事务的修改持保守态度，会通过数据库自身的锁机制来实现，从而保证数据操作的排它性
    悲观锁**适合写操作多的场景，因为写的操作具有排它性**。采用悲观锁的方式，可以在数据库层面阻止其他事务对该数据的操作权限，**防止读 - 写和写 - 写的冲**突。 

    在客户端 1 获取某数据行共享锁的同时，另一个客户端 2 也获取了该数据行的共享锁，
    这时任何一个客户端都没法对这个数据进行更新，因为共享锁会阻止其他事务对数据的更新，
    当某个客户端想要对锁定的数据进行更新的时候，就出现了死锁的情况。
    当死锁发生的时候，就需要一个事务进行回滚，另一个事务获取锁完成事务，然后将锁释放掉.

- Redis
    Redis 采用 ANSI C 语言编写，它和 SQLite 一样。采用 C 语言进行编写的好处是底层代码执行效率高，依赖性低，因为使用 C 语言开发的库没有太多运行时（Runtime）依赖，而且系统的兼容性好，稳定性高。
    Redis 是**基于内存的数据库**，这样可以避免磁盘 I/O，因此 Redis 也被称为缓存工具。
    Redis 数据结构结构简单，Redis 采用 **Key-Value 方式进行存储**，也就是使用 Hash 结构进行操作，数据的操作复杂度为 O(1)。
    Redis 采用**单进程单线程模型**，这样做的好处就是避免了上下文切换和不必要的线程之间引起的资源竞争。
    Redis 还采用了**多路 I/O 复用技术**。这里的多路指的是多个 socket 网络连接，复用指的是复用同一个线程。采用多路 I/O 复用技术的好处是可以在**同一个线程中处理多个 I/O 请求，尽量减少网络 I/O 的消耗，提升使用效率**。

    用法：
    设置某个键的值，使用方法为 set key value
    设置某个键的哈希值，可以使用 hset key field value
    同时将多个 field-value 设置给某个键 key 的时候，可以使用 hmset key field value [field value...]

    取某个键的某个 field 字段值，可以使用 hget key field
    一次获取某个键的多个 field 字段值，可以使用 hmget key field[field...]

    字符串列表（list）的底层是一个**双向链表结构**，所以我们可以向列表的两端添加元素，时间复杂度都为 O(1)，同时我们也可以获取列表中的某个片段。
    向列表左侧增加元素可以使用：LPUSH key value [...]
    向列表右侧添加元素 RPUSH key value [...]
    获取列表中某一片段的内容，使用LRANGE key start stop

    字符串集合（set）是字符串类型的无序集合，与列表（list）的区别在于集合中的元素是无序的，同时元素不能重复。
    在集合中添加元素，可以使用 SADD key member [...]
    在集合中删除某元素，可以使用 SREM key member [...]
    获取集合中所有的元素，可以使用 SMEMBERS key
    判断集合中是否存在某个元素，可以使用 SISMEMBER key member

    pip install redis
    在 Python 中提供了两种连接 Redis 的方式，
    第一种是直接连接，
    r = redis.Redis(host='localhost', port= 6379)
    第二种是连接池方式。 （连接池机制可以避免频繁创建和释放连接，提升整体的性能）
    pool = redis.ConnectionPool(host='localhost', port=6379)
    r = redis.Redis(connection_pool=pool)

- 原理分析:
    Redis 可能会遇到下面两种错误的情况：
    
    - 首先是**语法错误**，也就是在 Redis 命令入队时发生的语法错误。**Redis 在事务执行前不允许有语法错误，如果出现，则会导致事务执行失败**。
        如官方文档所说，通常这种情况在生产环境中很少出现，一般会发生在开发环境中，如果遇到了这种语法错误，就需要开发人员自行纠错。
    - 第二个是**执行时错误**，也就是在事务执行时发生的错误，比如处理了错误类型的键等，这种错误并非语法错误，Redis 只有在实际执行中才能判断出来。
        不过 **Redis 不提供回滚机制**，因此当发生这类错误时 Redis 会继续执行下去，保证其他命令的正常执行。
        在事务处理中，我们需要通过锁的机制来解决共享资源并发访问的情况。**在 Redis 中提供了 WATCH+MULTI 的乐观锁方式**。
        我们之前了解过乐观锁是一种思想，它是通过程序实现的锁机制，在数据更新的时候进行判断，成功就执行，不成功就失败，不需要等待其他事务来释放锁。
    
- Redis 的事务处理都包括哪些命令。
    **MULTI**：开启一个事务；
    **EXEC**：事务执行，将一次性执行事务内的所有命令；
    **DISCARD**：取消事务；
    **WATCH**：监视一个或多个键，如果事务执行前某个键发生了改动，那么事务也会被打断；
    **UNWATCH**：取消 WATCH 命令对所有键的监视。
- Redis 实现事务是**基于 COMMAND 队列**，如果 Redis 没有开启事务，那么任何的 COMMAND 都会立即执行并返回结果；如果 Redis 开启了事务，COMMAND 命令会放到队列中，并且返回排队的状态 QUEUED，只有调用 EXEC，才会执行 COMMAND 队列中的命令。
    MULTI 后不能再执行 WATCH 命令，否则会返回 WATCH inside MULTI is not allowed 错误（因为 WATCH 代表的就是在执行事务前观察变量是否发生了改变，如果变量改变了就将事务打断，所以在事务执行之前，也就是 MULTI 之前，使用 WATCH）。同时，如果在执行命令过程中有语法错误，Redis 也会报错，整个事务也不会被执行，Redis 会忽略运行时发生的错误，不会影响到后面的执行。
