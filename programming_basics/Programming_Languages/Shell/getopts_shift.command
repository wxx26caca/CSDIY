getopts命令用在脚本内部，可以解析复杂的脚本命令行参数，通常与while循环一起使用，取出脚本所有的带有前置连词线（-）的参数。

getopts optstring name
它带有两个参数。
第一个参数optstring是字符串，给出脚本所有的连词线参数。比如，某个脚本可以有三个配置项参数-l、-h、-a，其中只有-a可以带有参数值，而-l和-h是开关参数，那么getopts的第一个参数写成lha:，顺序不重要。注意，a后面有一个冒号，表示该参数带有参数值，getopts规定带有参数值的配置项参数，后面必须带有一个冒号（:）。
getopts的第二个参数name是一个变量名，用来保存当前取到的配置项参数，即l、h或a。

while getopts 'lha:' OPTION; do
  case "$OPTION" in
    l)
      echo "linuxconfig"
      ;;

    h)
      echo "h stands for h"
      ;;

    a)
      avalue="$OPTARG"
      echo "The value provided is $OPTARG"
      ;;
    ?)
      echo "script usage: $(basename $0) [-l] [-h] [-a somevalue]" >&2
      exit 1
      ;;
  esac
done
shift "$(($OPTIND - 1))"


shift命令可以改变脚本参数，每次执行都会移除脚本当前的第一个参数（$1），使得后面的参数向前一位，即$2变成$1、$3变成$2、$4变成$3，以此类推。
