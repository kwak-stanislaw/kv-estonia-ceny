import random
import time
from concurrent.futures import ThreadPoolExecutor

def generate_proxy():
    ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
    port = random.randint(1000, 9999)
    return f"{ip}:{port}"

def worker(n):
    proxy = generate_proxy()
    print(f"Worker {n} starting with proxy {proxy}")
    time.sleep(2)
    print(f"my_url.com/page_{n} using {proxy}")
    print(f"Worker {n} done")
    return f"my_url.com/page_{n}"

urls = [i for i in range(10)]

with ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(worker, urls)

for r in results:
    print(r)
##################   1   ########################################

# def worker(n):
#     print(f"Worker {n} starting")
#     time.sleep(2)  # simulates an I/O wait
#     print(f"my_url.com/page_{n}")
#     print(f"Worker {n} done")
#
# threads = [threading.Thread(target=worker, args=(i,)) for i in range(500)]
#
# for t in threads:
#     t.start() # start all threads
# for t in threads:
#     t.join() # wait until all threads are finished



#################   2   ########################################

# def worker(n):
#     print(f"Worker {n} starting")
#     time.sleep(2)  # simulates an I/O wait
#     print(f"my_url.com/page_{n}")
#     print(f"Worker {n} done")
#     return f"my_url.com/page_{n}"
#
# urls = [i for i in range(50)]
#
# with ThreadPoolExecutor(max_workers=30) as executor:
#     results = executor.map(worker, urls)
#
# for r in results:
#     print(r)



# Try to add function that will randomly generate proxy like number and will print it in worker function


# Use threading for intensive I/O operation, specially if that depends on external services (like, api or webscraping)
# Additionally - there is also multiprocessing library that is good for CPU intensive tasks.
# For really heavy-duty tasks (like high-traffic web server with tens of thousands concurrent I/O operations) use asynci


