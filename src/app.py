import sys
import time
import logging
import subprocess
from redis import Redis
from rq import Retry, Queue
from ingest import ingest_file
from multiprocessing import Process


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def start_rq_server():
    subprocess.run(["rq", "worker"])


def main(args):
    logging.info('Getting files list')
    files = args[1].split(",")
    logging.info(f'Files to ingest: {files}')

    logging.info('Creating RQ queue')
    queue = Queue(connection=Redis('172.31.0.2', 6379))

    for file_name in files:
        logging.info(f'Putting {file_name} into queue to ingestion')
        queue.enqueue(ingest_file, file_name, retry=Retry(max=3))        
        time.sleep(1)


if __name__ == "__main__":
    p1 = Process(target=start_rq_server)
    p1.start()
    time.sleep(2)
    p2 = Process(target=main(sys.argv))
    p2.start()
    p1.join()
    p2.join()