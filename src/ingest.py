import time
import logging
import pandas as pd
from sqlalchemy import create_engine

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)    


def read_file(file_name):    
    return pd.read_csv(f'/app/files_to_ingest/{file_name}', parse_dates=['datetime']).sort_values(['origin_coord', 'destination_coord', 'datetime'])            


def save_dataframe(df, table, mode):
    engine = create_engine('postgresql://postgres:postgres@db:5432/postgres')
    df.to_sql(table, engine, if_exists=mode)


def ingest_file(file_name):    
    time.sleep(1)
    logging.info(f'Reading file {file_name}')
    try:
        df = read_file(file_name)
    except Exception as e:        
        logging.error(f'Failed to read the file {file_name}.')
        logging.error(str(e))

    if df is None:
        time.sleep(1)
        logging.warn(f'Dataframe for file {file_name} is empty.')
        logging.warn('Moving to next file.')
        return
    time.sleep(1)

    logging.info('Saving dataframe to trips table in PostreSQL')
    save_dataframe(df, 'trips', 'append')    
    time.sleep(1)
    logging.info(f'Data from file {file_name} saved in trips table with success!')
    logging.info('==========================================================')