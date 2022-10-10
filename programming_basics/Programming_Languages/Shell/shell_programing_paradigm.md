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

### 参考
[Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)
