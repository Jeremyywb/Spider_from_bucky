from urllib.request import urlopen
from link_finder import LinkFinder
from general import *


class Spider:
	"""class variables shared among all instances"""
	project_name = ''
	base_url = ''
	domain_name = ''
	queue_file = ''
	crawed_file = ''
	queue = set()
	crawed = set()


	def __init__(self, project_name, base_url, domain_name):
		Spider.project_name = project_name
		Spider.base_url = base_url
		Spider.domain_name = domain_name
		Spider.queue_file = Spider.project_name + '/queue.txt'
		Spider.crawed_file = Spider.project_name + '/crawed.txt'
		self.boot()
		self.crawl_page('First spider', Spider.base_url)
	@staticmethod
	def boot():
		create_project_dir(Spider.project_name)
		create_data_files(Spider.project_name, Spider.base_url)
		Spider.queue = file_to_set(Spider.queue_file)
		Spider.crawed = file_to_set(Spider.crawed_file)
	
	@staticmethod
	def crawl_page(thread_name, page_url):
		if page_url not in Spider.crawed:
			print(thread_name, ' now crawling ' + page_url)
			print(' Queue ' + str(len(Spider.queue)) + ' | crawed ' + str(len(Spider.crawed)))
			Spider.add_links_to_queue(Spider.gather_links(page_url))
			Spider.queue.remove(page_url)
			Spider.crawed.add(page_url)
			Spider.update_files()
	
	@staticmethod
	def gather_links(page_url):
		html_string = ''
		try:
			response = urlopen(page_url)
			if response.getheader('Content-Type') == 'text/html':
				html_bytes = response.read()
				html_string = html_bytes.decode('utf-8')
			finder = LinkFinder(Spider.base_url, page_url)
			finder.feed(html_string)
		except Exception as e:
			print(str(e))
			print('Error: can not craw page')
			return set()
		return finder.page_links()

	@staticmethod
	def add_links_to_queue(links):
		for url in links:
			if url in Spider.queue:
				continue
			if url in Spider.crawed:
				continue
			if Spider.domain_name not in url:
				continue
			Spider.queue.add(url)

	@staticmethod
	def update_files():
		set_to_file(Spider.queue, Spider.queue_file)
		set_to_file(Spider.crawed, Spider.crawed_file)
