read [-options] [variable...]

如果read命令之后没有定义变量名，那么环境变量REPLY会包含所有的输入
#!/bin/bash
# read-single: read multiple values into default variable
echo -n "Enter one or more values > "
read
echo "REPLY = '$REPLY'"

read命令除了读取键盘输入，可以用来读取文件
while read myline
do
  echo "$myline"
done < $filename

-t
-p    指定用户输入的提示信息
-a    把用户的输入赋值给一个数组，从零号位置开始
-n    指定只读取若干个字符作为变量值，而不是整行读取




read命令读取的值，默认是以空格分隔。可以通过自定义环境变量IFS（内部字段分隔符，Internal Field Separator 的缩写），修改分隔标志。

#!/bin/bash
# read-ifs: read fields from a file

FILE=/etc/passwd

read -p "Enter a username > " user_name
file_info="$(grep "^$user_name:" $FILE)"

if [ -n "$file_info" ]; then
  IFS=":" read user pw uid gid name home shell <<< "$file_info"
  echo "User = '$user'"
  echo "UID = '$uid'"
  echo "GID = '$gid'"
  echo "Full Name = '$name'"
  echo "Home Dir. = '$home'"
  echo "Shell = '$shell'"
else
  echo "No such user '$user_name'" >&2
  exit 1
fi

如果IFS设为空字符串，就等同于将整行读入一个变量。
#!/bin/bash
input="/path/to/txt/file"
while IFS= read -r line
  do
  echo "$line"
done < "$input"
