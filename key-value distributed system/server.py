# -*- coding: utf-8 -*
import argparse
import rpyc
from rpyc.utils.server import ThreadedServer
from multiprocessing import Process
from sqlitedict import SqliteDict

log=[]

class Server(rpyc.Service):
	"""Server"""
	def on_connect(self, conn):
		self.db = SqliteDict('./database.sqlite', autocommit=True)

	def on_disconnect(self, conn):
		pass

	def exposed_set(self, k, v):
		self.db[k] = v

	def exposed_get(self, k):
		return None if k not in self.db else self.db[k]

	def exposed_rem(self, k):
		if k not in self.db:
			return
		del self.db[k]

	def exposed_getall(self):
		return [(k, self.db[k]) for k in self.db]

	def exposed_delall(self):
		keys = [k for k in self.db]
		for k in keys:
			del self.db[k]
	
	def exposed_writelog(self,msg):
		log.append(msg)

	def exposed_getlog(self):
		return log


def run(id_):
	port_ = id_ + 18862
	server = ThreadedServer(Server, port=port_)
	try:
		server.start()
	except KeyboardInterrupt:
		server.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--p', type=int, default=1)
	args = parser.parse_args()

	if args.p > 10:
		raise Exception('Requested too many servers. Please no more than 10.')

	processes = [Process(target=run,args=(i,)) for i in range(args.p)]
	print('%d servers are running.' % args.p)
	for i in range(args.p):
		processes[i].start()
	for i in range(args.p):
		processes[i].join()

