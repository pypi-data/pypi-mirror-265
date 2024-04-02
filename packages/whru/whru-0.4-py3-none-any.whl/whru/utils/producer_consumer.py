import threading
import time
import queue

# 生产者任务
def producer(queue):
    for i in range(5):
        item = f'产品{i}'
        queue.put((item, item))
        print(f'生产者生产了 {item}')
        time.sleep(1)  # 模拟生产耗时

# 消费者任务
def consumer(queue):
    while True:
        item = queue.get()
        print(type(item))
        if item is None:
            break  # 如果接收到None，表示生产结束，消费者停止消费
        print(f'消费者消费了 {item}')
        consume(*item)
        time.sleep(2)  # 模拟消费耗时

def consume(a, b):
    print("consume", a, b)

# 创建一个共享队列
shared_queue = queue.Queue(maxsize=10)

# 创建生产者和消费者线程
producer_thread = threading.Thread(target=producer, args=(shared_queue,))
consumer_thread = threading.Thread(target=consumer, args=(shared_queue,))

# 启动线程
producer_thread.start()
consumer_thread.start()

# 等待线程完成
producer_thread.join()
shared_queue.put(None)  # 生产完毕，放入None通知消费者结束
consumer_thread.join()

print('生产消费过程结束。')
