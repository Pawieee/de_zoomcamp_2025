#!/usr/bin/env python
# coding: utf-8

import os

from time import time

import pandas as pd
from sqlalchemy import create_engine


def main():
    user = "postgres"
    password = "postgres"
    host = "db"
    port = "5432"
    db = "ny_taxi"
    taxi_table_name ="green_tripdata"
    taxi_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz"
    zone_table_name = "taxi_zone_lookup"
    zone_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"
    
    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    taxi_csv = fetch_data(taxi_url, "taxi")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    df_iter = pd.read_csv(taxi_csv, iterator=True, chunksize=100000)

    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=taxi_table_name, con=engine, if_exists='replace')
    df.to_sql(name=taxi_table_name, con=engine, if_exists='append')


    while True: 
        try:
            t_start = time()
            df = next(df_iter)
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            df.to_sql(name=taxi_table_name, con=engine, if_exists='append')
            t_end = time()

            print('inserted another chunk, took %.3f second' % (t_end - t_start))

        except StopIteration:
            print("Finished ingesting taxi data into the postgres database")
            break
    
    # Insert taxi zones
    zone_csv = fetch_data(zone_url, "zones")
    zone_df = pd.read_csv(zone_csv)
    zone_df.tosql(name=zone_table_name, con=engine, if_exists='replace')
    print("Finished ingesting zone data into the postgres database")
    
    engine.dispose()


def fetch_data(url, name):
    if url.endswith('.csv.gz'):
        csv_name = 'output_' + name + '.csv.gz' 
    else:
        csv_name = 'output_' + name + '.csv'

    os.system(f"wget {url} -O {csv_name}")
    return csv_name


if __name__ == '__main__':
    main()
