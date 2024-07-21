import time,random
import queue,threading
q = queue.Queue()
 
 
def producer(name):
  count = 0
 
  while count < 20:
    time.sleep(random.randrange(3))
    q.put(count)  # 在队列里放包子
    print('Producer %s has produced %s baozi..' % (name, count))
    count += 1
 
 
def consumer(name):
  count = 0
  while count < 20:
    time.sleep(random.randrange(4))
    if not q.empty():  # 如果还有包子
        data = q.get()  # 就继续获取保证
        print(data)
        print('\033[32;1mConsumer %s has eat %s baozi...\033[0m' % (name, data))
    else:
        print("-----no baozi anymore----")
    count += 1
 
p1 = threading.Thread(target=producer, args=('A',))
c1 = threading.Thread(target=consumer, args=('B',))
p1.start()
c1.start()