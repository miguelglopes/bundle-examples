# Databricks notebook source
##################################################################################
# Batch Inference Notebook
#
# This notebook is an example of applying a model for batch inference against an input delta table,
# It is configured and can be executed as the batch_inference_job in the batch_inference_job workflow defined under
# ``mlops_stacks/resources/batch-inference-workflow-resource.yml``
#
# Parameters:
#
#  * input_table_name (required)  - Delta table name containing your input data.
#  * model_name (required) - The name of the model to be used in batch inference.
##################################################################################

# COMMAND ----------

import os
notebook_path =  '/Workspace/' + os.path.dirname(dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get())
%cd $notebook_path

# COMMAND ----------

# MAGIC %pip install -r requirements.txt

# COMMAND ----------

dbutils.library.restartPython()

# List of input args needed to run the notebook as sparka job.
# Provide them via DB widgets or notebook arguments.
#
# A Hive-registered Delta table containing the input features.
dbutils.widgets.text("input_table_name", "", label="Input Table Name")
# Unity Catalog registered model name to use for the trained mode.
dbutils.widgets.text(
    "model_name", "", label="Full (Three-Level) Model Name"
)

# COMMAND ----------

# DBTITLE 1,Define input and output variables

input_table_name = dbutils.widgets.get("input_table_name")
model_name = dbutils.widgets.get("model_name")
assert input_table_name != "", "input_table_name notebook parameter must be specified"
assert model_name != "", "model_name notebook parameter must be specified"
alias = "Champion"
model_uri = f"models:/{model_name}@{alias}"

# COMMAND ----------
# DBTITLE 1, Helper function
import mlflow
from pyspark.sql.functions import struct, lit, to_timestamp


def predict_batch(
    spark_session, model_uri, input_table_name, model_version, ts
):
    """
    Apply the model at the specified URI for batch inference on the table with name input_table_name
    """
    mlflow.set_registry_uri("databricks-uc")
    table = spark_session.table(input_table_name)
    
    predict = mlflow.pyfunc.spark_udf(
        spark_session, model_uri, result_type="string", env_manager="virtualenv"
    )
    output_df = (
        table.withColumn("prediction", predict(struct(*table.columns)))
        .withColumn("model_version", lit(model_version))
        .withColumn("inference_timestamp", to_timestamp(lit(ts)))
    )
    
    return output_df

# COMMAND ----------

from mlflow import MlflowClient

# Get model version from alias
client = MlflowClient(registry_uri="databricks-uc")
model_version = client.get_model_version_by_alias(model_name, alias).version

# COMMAND ----------

# Get datetime
from datetime import datetime

ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# COMMAND ----------
# DBTITLE 1, run inference

output_df = predict_batch(spark, model_uri, input_table_name, model_version, ts)
output_df.display()