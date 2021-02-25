from airflow import DAG
from airflow.operators import BashOperator
from datetime import datetime, timedelta

from airflow.operators.pipeline_plugin import HDXExtractOperator, HDXAdm0TransformOperator, HDXAdm1TransformOperator, \
    HDXRoadsTransformOperator, OSMExtractOperator, RCloneOperator

from config import config
from utils.dag_configuration import get_default_arguments, get_schedule_interval, get_catchup

from hdx_adm_dags import create_hdx_adm_dag
from hdx_roads_dags import create_hdx_road_dag
from osm_roads_dags import create_osm_road_dag


# Following are defaults which can be overridden later on
default_args = get_default_arguments()
schedule_interval = get_schedule_interval()
catchup = get_catchup()

countries = config.get_countries()

hdx_adm0_dag = create_hdx_adm_dag(countries=countries, schedule_interval=schedule_interval, catchup=catchup,
                                  default_args=default_args)
hdx_road_dag = create_hdx_road_dag(countries=countries, schedule_interval=schedule_interval, catchup=catchup,
                                   default_args=default_args)
osm_road_dag = create_osm_road_dag(countries=countries, schedule_interval=schedule_interval, catchup=catchup,
                                   default_args=default_args)

def create_sync_dag(schedule_interval, catchup, default_args):
    dag = DAG(f"sync", schedule_interval=schedule_interval, catchup=catchup, default_args=default_args)

    sync_operator = RCloneOperator(
        task_id=f"all_countries_sync_data",
        dag=dag
    )

    return dag

sync_dag = create_sync_dag(schedule_interval=schedule_interval, catchup=catchup, default_args=default_args)
