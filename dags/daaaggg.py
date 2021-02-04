import os

import pandas as pd
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from airflow.hooks.postgres_hook import PostgresHook


def vaccinations(**kwargs):
    airflow_home = os.getenv("AIRFLOW_HOME")
    if airflow_home:
        pg_hook = PostgresHook(mysql_conn_id='my_database',schema='business_intelligence').get_sqlalchemy_engine()
        file = f'{airflow_home}/data/country_vaccinations.csv'
        df = pd.read_csv(file, 
                 dtype={"total_vaccinations": "Int64", 
                        "people_vaccinated": "Int64", 
                        "people_fully_vaccinated": "Int64", 
                        "daily_vaccinations": "Int64", 
                        "daily_vaccinations_per_million": "Int64"}, encoding='utf-8')
        with pg_hook.begin() as transaction:
            transaction.execute('DELETE FROM test.vacinations_per_country')
            df.to_sql('vacinations_per_country', con=transaction, schema='business_intelligence', index=False)


dag = DAG('vaccinations', description='vaccinations etl',
          schedule_interval='0 12 * * *',
          start_date=datetime(2017, 3, 20), catchup=False)


etl = PythonOperator(task_id="vaccinations_etl",
                     python_callable=vaccinations,
                     dag=dag
                     )

