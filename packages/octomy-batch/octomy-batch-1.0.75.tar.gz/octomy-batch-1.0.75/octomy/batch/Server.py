import octomy.batch
import octomy.db 
import multiprocessing
import os
import signal

import logging

logger = logging.getLogger(__name__)


class Server:
	def __init__(self, config):
		self.config = config
		self.dbc = octomy.db.get_database(config)
		self.term_received = False

		def handler(signum, frame):
			logger.info(f"{signum} signal received, terminating gracefully")
			self.term_received = True

		signal.signal(signal.SIGABRT, handler)

	def verify(self):
		bp = octomy.batch.Processor(config=self.config)
		return bp.verify()

	def wrapper(self, num):
		logger.info(f"Batch worker {num} started with id:{os.getpid()}, parent:{os.getppid()}")
		bp = octomy.batch.Processor(config = self.config, dbc = self.dbc)
		while not self.term_received:
			# Do some work
			bp.process()
		logger.info(f"Worker {num} stopped")

	def start(self, num):
		logger.info(f"Batch worker {num} starting...")
		worker = multiprocessing.Process(target = self.wrapper, args = (num,))
		self.workers.append(worker)
		worker.start()
		return worker

	# Start server and serve forever
	def run(self):
		self.workers = []
		workers_count = self.config.get("batch-workers", 1)
		logger.info(f"Starting {workers_count} workers")
		num = 0
		for _ in range(workers_count):
			self.start(num)
			num += 1
		# Restart workes that terminate for whatever reason (they will self terminate on errors)
		while not self.term_received:
			multiprocessing.connection.wait(worker.sentinel for worker in self.workers)
			for worker in self.workers:
				logger.info(f"Batch worker terminating...")
				worker.join()
				self.workers.remove(worker)
				logger.info(f"Batch worker terminated")
				self.start(num)
				num += 1
		logger.info(f"Server stopping:")
		for worker in self.workers:
			logger.info(f"Batch worker terminating...")
			worker.join()
			self.workers.remove(worker)
		logger.info(f"Server stopped")
