import json
import pandas as pd
import csv
import os
import logging

def model(dbt, session):
    dbt.config(materialized="table")
    logger = logging.getLogger(__name__)
    project_root = dbt.config.get("project_root")
    logger.info(f"Project root: {project_root}")
    seed_file_path = os.path.join("seeds", "territorial_authority_2025.csv")
    csv.field_size_limit(1000000)
    try:
        territorial_auths_df = pd.read_csv(seed_file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: { seed_file_path}")
    return territorial_auths_df


# This part is user provided model code
# you will need to copy the next section to run the code
# COMMAND ----------
# this part is dbt logic for get ref work, do not modify

def ref(*args, **kwargs):
    refs = {}
    key = '.'.join(args)
    version = kwargs.get("v") or kwargs.get("version")
    if version:
        key += f".v{version}"
    dbt_load_df_function = kwargs.get("dbt_load_df_function")
    return dbt_load_df_function(refs[key])


def source(*args, dbt_load_df_function):
    sources = {}
    key = '.'.join(args)
    return dbt_load_df_function(sources[key])


config_dict = {'project_root': None}


class config:
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def get(key, default=None):
        return config_dict.get(key, default)

class this:
    """dbt.this() or dbt.this.identifier"""
    database = "qut-data-analytics-capstone"
    schema = "goodnature"
    identifier = "stg_territorial_authorities"
    
    def __repr__(self):
        return 'qut-data-analytics-capstone.goodnature.stg_territorial_authorities'


class dbtObj:
    def __init__(self, load_df_function) -> None:
        self.source = lambda *args: source(*args, dbt_load_df_function=load_df_function)
        self.ref = lambda *args, **kwargs: ref(*args, **kwargs, dbt_load_df_function=load_df_function)
        self.config = config
        self.this = this()
        self.is_incremental = False

# COMMAND ----------


