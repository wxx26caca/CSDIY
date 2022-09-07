# Kafka

## Kafka 是什么？主要的应用场景

- Kafka 是一个分布式流式处理平台，流平台主要提供下面三个关键的功能
    - 消息队列：发布和订阅消息流，类似于消息队列
    - 容错的持久方式存储记录消息流：Kafka 会把消息持久化到磁盘，避免了消息丢失的风险
    - 流式处理平台：在消息发布的时候进行处理，Kafka 提供了一个完整的流式处理类库
- 应用场景
    - 消息队列
    - 数据处理：构建实时的流数据处理程序来转换和处理数据流

## Kafka 与其他消息队列相比的优势

- 极致的性能：基于 Scala 和 Java，使用了大量批量处理和异步的思想
- 生态系统兼容性好：尤其在大数据和流计算领域

## 队列模型以及 Kafka 消息模型

- 队列模型

    - 使用**队列**作为消息的通信载体，满足**生产者与消费者**模式，一条消息只能被一个消费者使用，未被消费的消息会在队列中保留直到被消费或者超市
    - 可能存在的问题：将生产者产生的消息发送给多个消费者时候，并且每个消费者都能接收到完整的消息

- Kafka 消息模型

    - 发布 - 订阅模型

        使用**主题**（Topic）作为消息的通信载体，发布者发布一条消息，该消息通过主题传递给所有订阅者，在一条消息广播之前用户必须先订阅，否则收不到消息

## Kafka 中几个重要的概念

- Producer（生产者）：产生消息的一方
- Consumer（消费者）：消费消息的一方
- Broker（代理）：一个独立的 Kafka 实例，多个 broker 可组成一个 Kafka cluster
- Topic（主题）：Producer 将消息发送到特定的主题，Consumer 通过订阅特定的 Topic(主题) 来消费消息
- Partition（分区）： Partition 属于 Topic 的一部分。一个 Topic 可以有多个 Partition ，并且同一 Topic 下的 Partition 可以分布在不同的 Broker 上，这也就表明一个 Topic 可以横跨多个 Broker 

## Kafka 的多副本机制

为分区引入多副本（Replica）机制。分区中的多个副本之间会有一个 leader，其他副本称为 follower。我们发送的消息会被发送到 leader 副本，然后 follower 副本才能从 leader 副本中拉取消息进行同步。

当 leader 副本发生故障时，会从 follower 中选出一个 leader，但是 follower 中如果有和 leader 同步程度达不到要求的参加不了 leader 的竞选。

多副本的好处：

- 通过给特定 Topic 指定多个 Partition，而各个 Partition 可以分布在不同 Broker 上，这样能提供比较好的并发和负载均衡能力
- Partition 可以指定对应的 Replica 数，极大地提高了消息存储的安全性，提高了容灾能力，不过需要额外的存储空间

## Zookeeper 在 Kafka 中的作用

## Kafka 如何保证消息的消费顺序

- 分析：

    Kafka 中 Partition 是真正保存消息的地方，分区又存在与 Topic 这个概念中，我们可以给特定的 Topic 指定多个 Partition。

    每次添加消息到 Partition 的时候，采用**尾加法**。Kafka 只能保证 Partition 中的消息有序，不能保证 Topic 中的 Partition 的有序。

    消息被追加到 Partition 的时候都会分配一个特点的偏移量（**offset**），offset 表示 Consumer 当前消费到的 Partition 的所在位置，Kafka 通过偏移量可以保证消息在分区内的顺序性。

    Kafka 中发送一条消息的时候，可以指定 topic，partition，key，data 4 个参数，如果你发送消息的时候指定了 Partition 的话，所有消息都会被发送到一个 Partition。并且同一个 key 的消息可以保证只发送到同一个 Partition，可以采用表/对象的 id 作为 key。

    ![Kafka Topic Partitions Layout](https://camo.githubusercontent.com/39a19abce442bb75245e9e5196290bddef5820e725c6f5e118ad9c9165ad207d/68747470733a2f2f6d792d626c6f672d746f2d7573652e6f73732d636e2d6265696a696e672e616c6979756e63732e636f6d2f323031392d31312f4b61666b61546f70696350617274696f6e734c61796f75742e706e67)

- 方法：

    - 一个 Topic 只对应一个 Partition
    - 发送消息的时候指定 key/Partition
    - 

## Kafka 如何保证消息不丢失

- 生产者丢失消息
    - 通过回调函数来判断 send 方法发送消息之后，是否发送成功了
    - 为 Proceduer 设置合理的 retries 值

- 消费者丢失消息
    - 多副本机制