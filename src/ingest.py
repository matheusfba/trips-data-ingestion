import time
import logging
import pandas as pd
from sqlalchemy import create_engine


def read_file(path, columns_sort):
    try: 
        return pd.read_csv(path).sort_values(columns_sort)        
    except IOError as e:
        logging.info(f'Failed to read the file {path}.\n{str(e)}')


def save_dataframe(df, table, mode):
    engine = create_engine('postgresql://postgres:postgres@db:5432/postgres')
    df.to_sql(table, engine, if_exists=mode)


def ingest_file(file_name):
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    #print(f'\n')
    time.sleep(2)
    #logging.info('==========================================================\n')
    logging.info(f'Reading file {file_name}')
    df = read_file(file_name, ['origin_coord', 'destination_coord', 'datetime'])    
    if df is None:
        logging.warn(f'Dataframe for file {file_name} is empty.\nMoving to next file.')
        return
    logging.info('Saving dataframe to trips table in PostreSQL')
    save_dataframe(df, 'trips', 'replace')    
    logging.info(f'Data from file {file_name} saved in trips table with success!')
    logging.info('==========================================================')