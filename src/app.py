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
    subprocess.run(["rq", "worker", "--max-jobs", "1", "-q"])


def main(args):   
    files = sys.argv[1].split(",")
    logging.info(f'Files to ingest: {files}')
    logging.info('Creating RQ queue') 
    logging.info('==========================================================')
    queue = Queue(connection=Redis(os.environ['REDIS_HOST'], 6379),is_async=False)

    for file_name in files:
        logging.info(f'Putting {file_name} into queue to ingestion.')
        queue.enqueue(ingest_file, file_name, retry=Retry(max=3))
        #time.sleep(2)
    #print(f'\n')    
    logging.info('ALL FINISHED!')

if __name__ == "__main__":
    
    #p1 = Process(target=start_rq_server, args=str(len(files)))
    #p1.start()        
    time.sleep(2)
    p2 = Process(target=main(files))
    p2.start()    
    #p1.join()
    p2.join()