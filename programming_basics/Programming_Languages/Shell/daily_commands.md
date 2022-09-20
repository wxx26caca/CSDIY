# Deep understand linux commands

## uptime

> man uptime

`uptime` shows *the current time*, *how long the system has been running*, *how many users are currently logged on*, *system load averages for the past 1, 5, and 15 minutes*.

System load averages is the **average number of processes** that are either in a **runnable** or **uninterruptable** state.

A process in runnable state (R state shows from `ps`) is either using the CPU or waiting to use the CPU. A process in uninterruptable state (D state shows from `ps`) is waiting for some I/O access, eg waiting for disk.

Load averages are not normalized for the number of CPUs in a system, so a load average of 1 means a single CPU system is loaded all the time while on a 4 CPU system it means it was idle 75% of the time.

```
查看 cpu 的数量
$ top
or
$ cat /proc/cupinfo
```

当平均负载比 CPU 个数还大的时候，系统就出现了过载。 三个不同时间间隔的平均值，其实提供了，分析系统负载趋势的数据来源，可以更全面、更立体地理解目前的负载状况。

CPU 使用率，是单位时间内 CPU 繁忙情况的统计，跟平均负载并不一定完全对应。比如：

- CPU 密集型进程，使用大量 CPU 会导致平均负载升高，此时这两者是一致的；
- I/O 密集型进程，等待 I/O 也会导致平均负载升高，但 CPU 使用率不一定很高；
- 大量等待 CPU 的进程调度也会导致平均负载升高，此时的 CPU 使用率也会比较高。
