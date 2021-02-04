import os

import pandas as pd
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

from datetime import datetime, timedelta
from airflow.hooks.postgres_hook import PostgresHook


default_args = {
    "owner":"airflow",
    "depend_on_past":False,
    "start_date":datetime.today(),
    "retries":1,
    "retry_delay": timedelta(minutes=1)
}


def vaccinations(**kwargs):
    airflow_home = os.getenv("AIRFLOW_HOME")
    if airflow_home:
        pg_hook = PostgresHook(postgres_conn_id='my_database',schema='business_intelligence').get_sqlalchemy_engine()
        file = f'{airflow_home}/data/country_vaccinations.csv'
        df = pd.read_csv(file, 
                 dtype={"total_vaccinations": "Int64", 
                        "people_vaccinated": "Int64", 
                        "people_fully_vaccinated": "Int64", 
                        "daily_vaccinations": "Int64", 
                        "daily_vaccinations_per_million": "Int64"}, encoding='utf-8')
        with pg_hook.begin() as transaction:
            transaction.execute('DELETE FROM vacinations_per_country')
            df.to_sql('vacinations_per_country', con=transaction, if_exists='append',index=False)


with DAG('vaccinations',
        default_args=default_args,
        schedule_interval='@once',
        catchup=False) as dag:

        op = DummyOperator(task_id='op')
        etl = PythonOperator(task_id="vaccinations_etl",python_callable=vaccinations)
        op >> etl

