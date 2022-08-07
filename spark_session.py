import pandas
import numpy
from pyspark.sql import SparkSession, SQLContext

SPARK_APP_NAME = "parquet_manager"


class SparkSessionManager:
    spark_session = SparkSession
    spark_context = None
    sql_context = SQLContext

    parquet_files_cluster = dict()

    def __init__(self):
        self.__create_new_session()
        self.parquet_files_cluster = list()

    def upload_new_dataframe(self, file_path: str):
        self.parquet_files_cluster[self.__get_name(file_path)] = self.sql_context.read.parquet(file_path)

    def get_dataframe(self, name: str):
        try:
            return self.parquet_files_cluster[name]
        except KeyError:
            return None

    def __create_new_session(self):
        self.spark_session = SparkSession.builder.master("local[*]") \
            .appName(SPARK_APP_NAME) \
            .getOrCreate()
        self.spark_context = self.spark_session.sparkContext
        self.sql_context = SQLContext(self.spark_context)

    @staticmethod
    def __get_name(file_path) -> str:
        import os
        return os.path.basename(file_path)
