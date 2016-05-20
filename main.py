import threading
from queue import Queue
from spidermo import Spider
from domain import *
from general import *

PROJECT_NAME = 'thenewboston'
HOMEPAGE = 'https://thenewboston.com/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWED_FILE = PROJECT_NAME + '/crawed.txt'
NUMBER_OF_THREADS = 8
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE , DOMAIN_NAME)

# create worker theads (will die when main exists)
def create_workers():
	for _ in range(NUMBER_OF_THREADS):
		t = threading.Thread(target = work)
		t.daemon = True
		t.start()

# do the next job in the queue 
def work():
	while True:
		url = queue.get()
		Spider.crawl_page(threading.current_thread().name, url)
		queue.task_done()

def create_jobs():
	for links in file_to_set(QUEUE_FILE):
		queue.put(links)
	queue.join()
	crawl()

# check if there are items in the queue,if so crewl then
def crawl():
	queued_links = file_to_set(QUEUE_FILE)
	if len(queued_links) > 0 :
		print(str(len(queued_links)) + ' links in the queue')
		create_jobs()

create_workers()
crawl()
