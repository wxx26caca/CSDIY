# Shell 编程范例

## 数值运算

Shell 本身可以做整数运算，也可以借助外部命令 `expr`, `bc`, `awk` 等实现复杂运算。

### 整数运算

```bash
# 范例 1：对某个数加 1
i=0;
((i++))
let i++
expr $i + 1
echo $i 1 | awk '{printf $1+$2 "\n"}'
```

> 使用 `type` 命令可以查看各个命令的类型。`type type` `type let` `type expr` `type awk`。已经用过的命令，会加载在内存的 hash 表中。

> 使用 `help` 命令可以查看内置命令的说明，使用 `man` 可以查看外部命令的说明。

```bash
#!/bin/bash
# 范例 2：从 1 加到某个数
i=0;
while [ $i -lt 100 ]
do
  ((i++))
done
echo $i
```

执行脚本的方式：

- `bash` + 脚本文件。

- 通过 `bash` 的内置命令 `.` 或 `source` 执行。`. ./test.sh` or `source ./test.sh`。

- 修改文件为可执行。

`time` 命令可以用来统计命令执行时间，这部分时间包括总的运行时间，用户空间执行时间，内核空间执行时间，它通过 `ptrace` 系统调用实现。

`let`, `expr`, `bc` 都可以用 `%` 运算符来求模，`let` 可以用 `**` 运算符求幂，而 `bc` 使用 `^` 运算符求幂。

```bash
# 范例 3：求模
expr 5%2
let i=5%2
echo 5%2 | bc
((i=5%2))
```

```bash
# 范例 4：求幂
let i=5**2
((i=5**2))
echo "5^2" | bc
```

```bash
# 范例 5：进制转换
# 将八进制的 11 转换成十进制
echo "obase=10;ibase=8;11" | bc
echo $((8#11))
```

### 浮点运算

`let` 和 `expr` 都不能进行浮点运算，但是  `bc` 和 `awk` 可以。

```bash
# 范例 6：求 1 除以 13，保留 3 位有效数字
echo "scale=3; 1/13" | bc
echo "1 13" | awk '{printf("%0.3f\n", $1/$2)}'
```

```bash
# 范例 7：余弦值转角度
export cos=0.996293; echo "scale=100; a(sqrt(1-$cos^2)/$cos)*180/(a(1)*4)" | bc -l
echo 0.996293 | awk '{ printf("%s\n", atan2(sqrt(1-$1^2),$1)*180/3.1415926535);}'
```

```bash
#!/bin/bash
# 范例 8：income.txt 文件中有一组数据，求人均月平均收入最高的家庭
# income.txt
# 1 3 4490
# 2 5 3896
# 3 4 3112
# 4 4 4716
# 5 4 4578
# 6 6 5399
# 7 3 5089
# 8 6 3029
# 9 4 6195
# 10 5 5145

[ $# -lt 1 ] && echo "please input the income file" && exit -1
[ ! -f $1 ] && echo "$1 is not a file" && exit -1

income=$1
awk '{ printf("%d %0.2f\n", $1, $3/$2); }' $income | sort -k 2 -n -r
```

> `$#` 是 Shell 中传入参数的个数；`sort` 命令 `-k 2` 以第 2 列进行排序， `-n` 按照数字排序， `-r` 逆序

### 随机数

环境变量 `RANDOM` 产生从 0 到 32767 的随机数，`awk` 的 `rand()` 函数可以产生 0 到 1 之间的随机数。

```bash
# 范例 9：获取一个随机数
echo $RANDOM
echo "" | awk '{srand(); printf("%f", rand());}'
```

> `srand()` 在无参数时，采用当前时间作为 `rand()` 随机数产生器的一个 seed。

```bash
# 范例 10：随机产生一个从 0 到 255 之间的数字
expr $RANDOM / 128
echo "" | awk '{srand(); printf("%d\n", rand() * 255);}'
```

```bash
#!/bin/bash
# 范例 11：自动获取一个可用的 IP 地址

# set your own network, default gateway, and the time out of ping command
net="10.10.10"
default_gateway="10.10.10.1"
over_time=2

# check the current ipaddress
ping -c 1 $default_gateway -W $over_time
[ $? -eq 0 ] && echo "the current ipaddress is okay" && exit -1

while :; do
  # clear the current config
  ifconfig eth0 down
  ifconfig eth0 $net.$(($RANDOM / 130 + 2)) up
  route add default gw $default_gateway
  ping -c 1 $default_gateway -W $over_time
  [ #? -eq 0 ] && break
done
```

### 其他运算

`seq` 可以产生一系列数，指定数的递增间隔，也可以指定相邻两个数之间的分割符。

```bash
# 范例 12：`seq` 用法
# -f, --format=FORMAT    use printf style floating-point FORMAT
# -s, --separator=STRING use STRING to separate numbers (default: \n)
# -w, --equal-width      equalize width by padding with leading zeroes
seq 1 2 5
seq -s: 1 2 5
seq -w 1 2 14
seq -f "0x%g" 1 5
```

> `Bash` 版本 3 以上，`for` 循环中可以通过 `{1..5}` 产生 1 到 5 的数字。

```bash
# 范例 13：统计字符串中各单词出现次数
wget -c http://tinylab.org
cat index.html | sed -e "s/[^a-zA-Z]/\n/g" | grep -v ^$ | sort | uniq -c
# 统计出现频率最高的前 10 单词
cat index.html | sed -e "s/[^a-zA-Z]/\n/g" | grep -v ^$ | sort | uniq -c | sort -n -r -k 1 | head -10
```

> `sed -e "s/[^a-zA-Z]/\n/g"`: 把非字母字符替换成空格，只保留字母字符；`grep -v ^$`：去掉空行

```bash
#!/bin/bash
# 范例 14：统计指定单词出现次数方法一，只统计那些需要统计的单词

if [ $# -lt 1 ]; then
  echo "Usage: basename $0 FILE WORDS ..."
  exit -1
fi

FILE=$1
((WORDS_NUM=$#-1))

for n in $(seq $WORDS_NUM)
do
  shift
  cat $FILE | sed -e "s/[^a-zA-Z]/\n/g" | grep -v ^$ | sort | grep ^$1$ | uniq -c
done
```

```bash
#!/bin/bash
# 范例 14：统计指定单词出现次数方法二，把所有单词的个数都统计出来，然后再返回那些需要统计的单词给用户

if [ $# -lt 1 ]; then
  echo "Usage: basename $0 FILE WORDS ..."
  exit -1
fi

FILE=$1
((WORDS_NUM=$#-1))

for n in $(seq $WORDS_NUM)
do
  shift
  cat $FILE | sed -e "s/[^a-zA-Z]/\n/g" | grep -v ^$ | sort | uniq -c | grep " $1$"
done
```

## 文件操作

### 文件的各种属性

```c
struct stat {
    dev_t st_dev;    /* 设备 */
    ino_t st_ino;    /* 节点 */
    mode_t st_mode;   /* 模式 */
    nlink_t st_nlink; /* 硬连接 */
    uid_t st_uid;  /* 用户ID */
    gid_t st_gid;  /* 组ID */
    dev_t st_rdev; /* 设备类型 */
    off_t st_off;  /* 文件字节数 */
    unsigned long  st_blksize; /* 块大小 */
    unsigned long st_blocks;  /* 块数 */
    time_t st_atime; /* 最后一次访问时间 */
    time_t st_mtime; /* 最后一次修改时间 */
    time_t st_ctime; /* 最后一次改变时间(指属性) */
};
```

与文件系统相关的常用命令：

- `stat`： 按照上面 stat 结构体的格式，显示文件或文件系统的信息。

- `ls`： 跟上 `-l` 参数可以显示文件的更多信息。

- `od`：以八进制或者其他格式“导出”文件内容。

- `strings`：读出文件中的字符（可打印的字符）。

- `file`：查看各类文件的属性。

- `readelf`: ELF 文件分析命令。

- `gcc`, `gdb`：编译和调试命令。

- `objdump`：反汇编命令。

常见的文件类型（`stat` 中的 `st_mode`)：

- 常规文件，`ls` 命令显示为 `d` 的是目录，`-` 为普通文件。

- 硬链接，`ls` 命令显示为 `-` 可能为硬链接文件。

- 软链接，`ls` 命令显示 `l`。

- 管道文件，`ls` 命令显示 `p`。

- 符号设备，`ls` 命令显示 `c`。

- 块设备，`ls` 命令显示 `b`。

- socket 文件，`ls` 命令显示 `s`。

> 硬链接和软链接的主要区别有：1. 删除原文件的时候，硬链接相当于是原文件，所以还可以读取内容，而软链接只是有一个 `inode`，并没有实际存储空间，所以无法读取内容；2. 可以用 `stat` 查看它们的区别，包括 `Blocks`，`inode` 值等，也可以用 `diff` 查看它们的大小；3. 硬链接不可以跨文件系统，软链接可以；4. 不允许给目录创建硬链接。

> `file` 命令相比 `stat` 命令来说，可以显示更详细的信息，在操作系统的支持下会得到不同的解释，执行不同的动作。Linux 是按照**文件头**来识别各类文件的，这样在解释相应的文件时就更不容易出错。

管理文件属主的常用命令：

- 创建用户和组：`useradd` `groupadd`。

- 删除用户和组：`userdel` `groupdel`。

- 修改用户密码：`passwd`。

- 修改文件属主：`chown`，`chown <user>:<group> filename`。

- 查看文件属主：`ls -l | -n`。`ls -l` 命令是通过读取配置文件中的用户 ID 和组 ID 实现的，可以用 `strace` 跟踪。 

- 配置文件：`/etc/passwd` `/etc/group` `/etc/shadow`。

`chmod` 命令可以修改文件的权限。`ls -l` 命令输出的文件权限部分，分为文件所属用户，所属组，其他组对文件的权限三部分。

除了常规的读，写，可执行权限外，还有与安全相关的权限，即 `setuid/setgid` 和只读控制等。如果设置了文件（程序或者命令）的 `setuid/setgid` 权限，那么用户将可用 root 身份去执行该文件，因此，这将可能带来安全隐患；如果设置了文件的只读权限，那么用户将仅仅对该文件将有可读权限，这为避免诸如 `rm -rf` 的“可恶”操作带来一定的庇佑。

> `setuid` 和 `setgid` 位是让普通用户可以以 root 用户的角色运行只有 root 帐号才能运行的程序或命令。

> `chattr` 可以设置文件的特殊权限。

文件大小对于普通文件而言就是文件内容的大小；对于目录而言，它存放的内容是以**目录结构体** （`struct dirent`）组织的各类文件信息，所以**目录的大小一般都是固定的**，它存放的文件个数的上限，即它的大小除以文件名的长度；设备文件的“文件大小”则对应设备的主、次设备号；管道文件因为特殊的读写性质，所以大小常是 0 ；硬链接实质上是原文件的一个完整的拷贝，它的大小就是原文件的大小，而软链接只是一个 `inode`，存放了一个指向原文件的指针，因此它的大小仅仅是原文件名的字节数。

> 文件名并没有存放在文件结构体内，而是存放在它所在的目录结构体中。所以，在目录的同一级别中，文件名必须是唯一的。

文件操作相关的常用命令：

- 创建文件：创建一个文件实际上是在文件系统中添加了一个节点（inode)，该节点信息将保存到文件系统的节点表中。可以用 `tree` 或 `ls` 等命令呈现出来。

  ```
  $ touch regular_file       # 创建普通文件
  $ mkdir directory_file     # 创建目录文件，目录文件里可以包含更多文件
  $ ln regular_file regular_file_hard_link     # 硬链接，是原文件的一个完整拷比
  $ ln -s regular_file regular_file_soft_link  # 类似一个文件指针，指向原文件
  $ mkfifo fifo_pipe   # 或者通过 "mknod fifo_pipe p" 来创建，FIFO满足先进先出的特点
  $ mknod hda1_block_dev_file b 3 1  # 块设备
  $ mknod null_char_dev_file c 1 3   # 字符设备
  ```

- 删除文件：文件删除之后，并不是立即消失了，而是仅仅做了删除标记，因此，如果删除之后，没有相关的磁盘写操作把相应的磁盘空间“覆盖”，那么原理上是可以恢复的。`rm`。

- 复制文件：有 `link` 和 `copy` 两种复制方式。一般所指的复制是指 `copy`。`link` 和 `copy` 不同之处是：`link` 为同步更新，`copy` 则不然，复制之后两者不再相关。`cp` `ln`。

- 编辑文件：文件编辑工具 `vim`, `emacs`, `gedit` 等。也可以利用重定向来实现。

- 压缩文件：`tar`，`bzip2`，`bunzip2`，`gzip`，`gunzip` 等。

- 搜索文件：`find` 命令提供了一种“及时的”搜索办法，它在指定的目录层次中遍历所有文件直到找到需要的文件为止。而 `updatedb+locate` 提供了一种“快速的”的搜索策略，`updatedb` 更新并产生一个本地文件数据库，而 `locate` 通过文件名检索这个数据库以便快速找到相应的文件。`grep` `sed` 可以搜索具体的文件内容。

  ```
  $ find ./ -name "*.c" -o -name "*.h"  # 找出所有的C语言文件，-o 是或者的意思
  $ find ./ \( -name "*.c" -o -name "*.h" \) -exec mv '{}' ./c_files/ \;  # 把找到的文件移到c_files下
  $ find ./ -name "*.c" -o -name "*.h" | xargs -i mv '{}' ./c_files/
  $ 
  ```

## 参考资料
[Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)

[China Unix Shell 讨论区](http://bbs.chinaunix.net/forum-24-1.html)

[Everything Is Byte](http://www.reteam.org/papers/e56.pdf)
