from airflow import DAG

from airflow.operators.pipeline_plugin import (
    OSMExtractOperator,
    OSMRiversTransformOperator,
)
from utils.config_parser import config
from utils.dag_configuration import (
    get_catchup,
    get_default_arguments,
    get_schedule_interval,
)

countries = config.get_countries()

# Defaults which can be overridden if needed
default_args = get_default_arguments()
schedule_interval = get_schedule_interval()
catchup = get_catchup()

with DAG(
    "osm_rivers",
    schedule_interval=schedule_interval,
    catchup=catchup,
    default_args=default_args,
) as dag:
    for country in countries:
        osm_rivers_extract = OSMExtractOperator(
            task_id=f"{country}_osm_rivers_extract",
            osm_url=config.get_osm_url(country=country),
            country_iso2=config.get_iso2(country=country),
            overpass_query_schema_filename=config.get_osm_query_schema(
                country=country, dataset_name="rivers"
            ),
            osm_output_filename=config.get_raw_osm_data_path(
                country=country, dataset_name="rivers", format="raw_osm"
            ),
            gpkg_output_filename=config.get_raw_osm_data_path(
                country=country, dataset_name="rivers", format="raw_gpkg"
            ),
            dag=dag,
        )

        source = "osm"
        rivers_transform = OSMRiversTransformOperator(
            task_id=f"{country}_osm_rivers_transform",
            source=source,
            input_filename=config.get_raw_osm_data_path(
                country=country, dataset_name="rivers", format="raw_gpkg"
            ),
            output_filename=config.get_osm_processed_filepath(
                country=country, dataset_name="rivers"
            ),
            crs=config.get_crs(),
            schema_mapping=config.get_schema_mapping(
                source=source, country=country, dataset_name="rivers"
            ),
            dag=dag,
        )

        osm_rivers_extract >> rivers_transform
