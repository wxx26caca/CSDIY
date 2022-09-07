[toc]

# TCP

## 状态转换图

![](https://i.loli.net/2021/01/23/VwIjkZ3qARKvtmC.png)

## 三次握手

- `第一次握手`

    client 发送，server 接收。====> server 能得出结论：client 的发送能力和 server 的接收能力正常

    ```
    SYN=1, seq=x
    ```

- `第二次握手`

    server 发送，client 接收。====> client 能得出结论：server 的收发能力正常，client 的收发能力正常

    ```
    SYN=1, seq=y
    ACK=1, ack=x+1
    ```

- `第三次握手`

    client 发送，server 接收。====> server 能得出结论：client 的收发能力正常，server 的收发能力正常

    ```
    ACK=1, ack=y+1, seq=x+1
    ```

## 四次挥手

TCP连接是**双向传输**的对等模式，即双方都可以同时向对方发送或者接收数据。

- `第一次挥手`

    一方要关闭连接时，会发送 `FIN` 指令告诉对方，我要关闭连接了。

    ```
    FIN=1, seq=u
    ```

- `第二次挥手`

    对方会回一个 `ACK` ，此时**一个方向的连接关闭，但是另一个方向仍然可以继续传输数据**。

    ```
    ACK=1, seq=v, ack=u+1
    ```

- `第三次挥手`

    等所有数据都传完了之后，对方发送一个 `FIN` ，关闭此方向上的连接。

    ```
    FIN=1, ACK=1, seq=w, ack=u+1
    ```

- `第四次挥手`

    接收方发送一个 `ACK` 确认关闭连接。

    ```
    ACK=1, seq=u+1, ack=w+1
    ```

## 基本问题Q&A

### 为什么需要三次握手？

> 防止已经失效的连接请求报文突然又传到了服务器，导致错误。

> 发送双方确认自己和对方的接收和发送能力是正常的。

### 为什么建立连接是三次握手，关闭连接却是四次挥手

> 因为服务端在 LISTEN 状态下，收到建立连接请求的 SYN 报文后，把 ACK 和 SYN 放在一个报文里发送给客户端。
>
> 关闭连接时，当收到对方的 FIN 报文时，仅仅表示对方不再发送数据了但是还能接收数据，己方是否现在关闭发送数据通道，需要上层应用来决定，因此，己方 ACK 和 FIN 一般都会分开发送。

### 为什么客户端最后还要等2MSL

> MSL(Maximum Segment Lifetime)
>
> 一：**保证客户端发送的最后一个 ACK 报文能够到达服务器**。因为这个 ACK 报文可能丢失，站在服务器的角度看来，我已经发送了 FIN+ACK 报文请求断开了，客户端还没有给我回应，应该是我发送的请求断开报文它没有收到，于是服务器又会重新发送一次，而客户端就能在这个 2MSL 时间段内收到这个重传的报文，接着给出回应报文，并且会重启 2MSL 计时器。
>
> 二：**防止类似与“三次握手”中提到了的“已经失效的连接请求报文段”出现在本连接中**。客户端发送完最后一个确认报文后，在这个 2MSL 时间中，就可以使本连接持续的时间内所产生的所有报文段都从网络中消失。这样新的连接中不会出现旧连接的请求报文。

## 进阶知识

### 三次握手可能出现的问题

- 假如 server 给 client 回复 SYN+ACK 之后，client 掉线了，怎么办？

    server 在一定时间内没有到会重新发 SYN+ACK，默认重试次数是 5 次，1+2+4+8+16+32=63s，（5次加等待第五次超时），63s内都没有回复，则会断掉这个连接

- 假如有恶意攻击者发送大量 SYN 后就下线了，会造成什么后果？（SYN Flood 攻击）

    攻击者可能会把服务器的 SYN 连接的队列耗尽，让正常的连接请求无法处理 

    -> 当 SYN 队列满了之后， TCP 会通过 source_port, dest_port 和时间戳来打造出一个特别的 Sequence Number （cookie） 发回去，如果是攻击者则不会响应，如果是正常连接，会把这个 SYN cookie 发回来，服务端可以通过 cookie 建立连接。通过 **tcp_syncookies** 参数对应这种情况

    -> 一般的解决方式：减小 **tcp_synack_retries** 来减少重试次数；增大 **tcp_max_syn_backlog** 参数来增加 SYN 连接数；**tcp_abort_on_overflow** 处理不过来就直接拒绝连接

- ISN 的初始化

    ISN 不可以 hard code，RFC793 中说，ISN 会和一个假的时钟绑在一起，这个时钟会在每 4 微妙对 ISN 做加一操作，知道超过 2^32，又从 0 开始。这样，一个 ISN 的存活周期大约是 4.55 小时

    只要Segment 存活时间不超过 MSL（Maximum Segment Lifetime），就不会重用到 ISN

### 四次挥手可能出现的问题

- 为什么 TIME_WAIT 状态到 CLOSED 状态之间要设置 2*MSL ？

    - 确保有足够的时间让对端收到了 ACK，如果被动关闭的那端没收到 ACK，就会触发被动端重发 FIN，以来一去正好 2 个 MSL
    - 确保有足够的时间让这个连接不会跟后面的连接混到一起（可能有些路由器会缓存 IP 数据包，如果连接被重用了，那些延迟收到的包就可能和新连接混到一起）

- TIME_WAIT 数量太多了怎么办？

    在大并发的短链接下，TIME_WAIT 就会太多，消耗很多系统资源

    解决方式涉及两个参数 **tcp_tw_reuse** + tcp_timestamps=1，**tcp_tw_recycle**，打开这两个参数要很谨慎

    tcp_max_tw_buckets 是控制并发的 TIME_WAIT 的数量的，如果超过限制，系统会把多的给 destroy 掉

### 数据传输中的 Sequence Number

seqNum 的增加是和传输的字节数相关的

### TCP 重传机制

SeqNum 和 ACK 是以字节数为单位，所以 ACK 的时候，不能跳着确认，只能确认最大的连续收到的包

- 超时重传机制

    可能出现的问题：仅重传 timeout 的包；重传 timeout 后所有的包

- 快速重传机制

    - TCP 的 Fast Retransmit 的算法，不以时间驱动，以数据驱动重传，**解决了 timeout 的问题**。它的做法是，如果包没有连续到达，就 ACK 最后那个可能被丢的包，如果发送方连续 3 次收到相同的 ACK，就重传。

        可能出现的问题：到底是只重传没有到达的包还是它之后的包都重传

    - SACK（Selective Acknowledgment）

        ACK 还是 Fast Retransmit 的 ACK，SACK 则是汇报收到的数据碎版。RFC-2018

        通过 **tcp_sack** 参数打开这个功能

        可能出现的问题：如果攻击者给数据发送方发一堆 SACK 的选项，这会导致发送方开始要重传甚至遍历已经发出的数据，会消耗很多发送端的资源

    - Duplicate SACK

        主要使用了 SACK 来告诉发送方**有哪些数据被重复接收了**。RFC-2883

        通过 **tcp_dsack** 参数打开这个功能

        如果 SACK 的第一个段的范围被 ACK 所覆盖，那么就是 D-SACK

        如果 SACK 的第一个段的范围被 SACK 的第二个段所覆盖，那么就是 D-SACK

        引入 D-SACK 的好处：

        - 可以让发送方知道，是发出去的包丢了，还是回来的ACK包丢了。
        - 是不是自己的timeout太小了，导致重传。
        - 网络上出现了先发的包后到的情况（又称reordering）。
        - 网络上是不是把我的数据包给复制了。

### TCP 的 RTT 算法

**RTT (Round Trip Time)** 即一个数据包从发出到回来的时间，这样就可以设置 Timeout - **RTO（Retransmisson TimeOut）**

- 经典算法

    > 1）首先采样 RTT，记下最近好几次的 RTT 值
    >
    > 2）做平滑计算 SRTT = (α \* SRTT) + ((1-α) \* RTT)
    >
    > 3）计算 RTO = min[UBOUND, max[LBOUND, (β \* SRTT)]]

    UBOUND 为 timeout 上限值，LBOUND 为 timeout 下限值，α 取 0.8~0.9，β 取 1.3~2.0

- Karn/Partridge 算法

    忽略重传，不把重传的 RTT 做采样

- Jacobson/Karels 算法

    RFC-6289

    > SRTT = SRTT + α(RTT– SRTT)  —— 计算平滑RTT
    >
    > DevRTT = (1-β)\*DevRTT + β\*(|RTT-SRTT|) ——计算平滑RTT和真实的差距（加权移动平均）
    >
    > RTO= µ \* SRTT + ∂ \*DevRTT —— 神一样的公式
    >
    > 在Linux下，α = 0.125，β = 0.25， μ = 1，∂ = 4 ——这就是算法中的“调得一手好参数”，nobody knows why, it just works…

### TCP 滑动窗口

**TCP必需要解决的可靠传输以及包乱序（reordering）的问题**

**TCP头里有一个字段叫Window，又叫Advertised-Window，这个字段是接收端告诉发送端自己还有多少缓冲区可以接收数据**。**于是发送端就可以根据这个接收端的处理能力来发送数据，而不会导致接收端处理不过来**。 

![TCP Transmission Stream Categories and Send Window Terminology](http://www.tcpipguide.com/free/diagrams/tcpswwindows.png)

> #1 已收到 ack 确认的数据
>
> #2 发出了但还没收到 ack 的
>
> #3 在窗口中还没有发出的（接收方还有空间）
>
> #4 窗口以外的数据（接收方没有空间）

可能出现的问题：处理缓慢的 server 端把 client 端的滑动窗口将为 0 了怎么办？是不是此时发送端就不发送数据了？如果发送端不发送数据了，接收方一会儿 window size 可用了，怎么通知发送端？

- **Zero Window Probe**

    发送端窗口变为 0 后，会发 ZWP 包给接收方，让接收方来 ack 它的 window size，如果几次之后，如果还是 0 的话，有的 TCP 会发 RST 把链接断掉。

    可能出现的问题：如果攻击者在 HTTP 建好链接发完 GET 请求后，把 window size 设置为 0 ，然后服务端就只能等 ZWP ，于是攻击者会并发大量的这样的请求，把服务端资源耗尽。

- **Silly Window Syndrome**

    糊涂窗口综合症

    对于以太网来说，MTU是1500字节，除去TCP+IP头的40个字节，真正的数据传输可以有1460，这就是所谓的MSS（Max Segment Size）。

    **如果你的网络包可以塞满MTU，那么你可以用满整个带宽，如果不能，那么你就会浪费带宽**。

    **Silly Windows Syndrome这个现像就像是你本来可以坐200人的飞机里只做了一两个人**。应对方式是**直到足够大的 window size 再响应**。

    - 如果这个问题是由Receiver端引起的，那么就会使用 **David D Clark’s** 方案。

        在receiver端，如果收到的数据导致window size小于某个值，可以直接ack(0)回sender，这样就把window给关闭了，也阻止了sender再发数据过来，等到receiver端处理了一些数据后windows size 大于等于了MSS，或者，receiver buffer有一半为空，就可以把window打开让send 发送数据过来。

    - 如果这个问题是由Sender端引起的，那么就会使用著名的 **Nagle’s algorithm**。Nagle算法默认是打开的

        这个算法的思路也是延时处理，它有两个主要的条件：

        1）要等到 Window Size>=MSS 或是 Data Size >=MSS，

        2）收到之前发送数据的ack回包，他才会发数据，否则就是在攒数据。

        **比如像telnet或ssh这样的交互性比较强的程序，你需要关闭这个算法**。你可以在Socket设置**TCP_NODELAY** 选项来关闭这个算法

        ```c
        setsockopt(sock_fd, IPPROTO_TCP, TCP_NODELAY, (char *)&value,sizeof(int));
        ```

        **TCP_CORK其实是更新激进的Nagle算法，完全禁止小包发送，而Nagle算法没有禁止小包发送，只是禁止了大量的小包发送**。

### TCP 的拥塞处理 - Congestion Handling

拥塞控制主要是四个算法：**1）慢启动**，**2）拥塞避免**，**3）拥塞发生**，**4）快速恢复**。

- 慢启动
- 拥塞避免
- 拥塞发生
- 快速恢复

## 参考文章

[“三次握手，四次挥手”你真的懂吗？](https://zhuanlan.zhihu.com/p/53374516)

[TCP协议 笔试面试知识整理](https://hit-alibaba.github.io/interview/basic/network/TCP.html)

[两张动图-彻底明白TCP的三次握手与四次挥手](https://blog.csdn.net/qzcsu/article/details/72861891)

[TCP的那些事儿（上）](https://coolshell.cn/articles/11564.html)

[TCP的那些事儿（下）](https://coolshell.cn/articles/11609.html)

