from pipeline_plugin.transform.general_transformers.cod_transform import transform_cod
from pipeline_plugin.transform.general_transformers.osm_transform import transform_osm
from pipeline_plugin.transform.general_transformers.transform_to_crs import (
    transform_to_crs,
)
from pipeline_plugin.utils.files import load_file, save_shapefiles


def transform(
    source: str, input_filename: str, output_filename: str, crs, schema_mapping
):
    """
    :param source: "osm" or "cod" are the options
    """
    input_filename = load_file(input_filename)

    if source == "osm":
        df = transform_osm(input_filename=input_filename, schema_mapping=schema_mapping)
        df = transform_to_crs(df=df, crs=crs)

    elif source == "cod":
        df = transform_cod(input_filename=input_filename, schema_mapping=schema_mapping)
        df = transform_to_crs(df=df, crs=crs)

    save_shapefiles(df, output_filename, encoding="utf8")
