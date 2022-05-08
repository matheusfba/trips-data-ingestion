import os
import sys
import time
import logging
import subprocess
from redis import Redis
from rq import Retry, Queue
from rq.job import Job
from ingest import ingest_file
from multiprocessing import Process

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def start_rq_server(max_files_to_process):
    """
        Start the rq worker. Not used in this PoC because I choose to use synchronized process of ingestion
    """
    subprocess.run(["rq", "worker", "--max-jobs", max_files_to_process, "-q"])


def main(args):   
    if len(args) == 1:
        logging.error('No files informed to be processed!')
        sys.exit('FINISHED!')
        
    files = args[1].split(",")
    time.sleep(1)
    logging.info(f'Files to ingest: {files}')
    time.sleep(1)
    logging.info('Creating RQ queue') 
    time.sleep(1)
    logging.info('==========================================================')
    queue = Queue(connection=Redis(os.environ['REDIS_HOST'], 6379),is_async=False)

    for file_name in files:
        time.sleep(1)
        logging.info(f'Putting {file_name} into queue to ingestion.')
        queue.enqueue(ingest_file, file_name, retry=Retry(max=3))

    time.sleep(1)
    logging.info('FINISHED!')


if __name__ == "__main__":    
    main(sys.argv)    