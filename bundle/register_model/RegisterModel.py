# Databricks notebook source
##################################################################################
# Log model in mlflow
#
# This notebook has the following parameters:
#
#  * model_uri (required)  - URI of the model to deploy. Must be in the format "models:/<name>/<version-id>", as described in
#                            https://www.mlflow.org/docs/latest/model-registry.html#fetching-an-mlflow-model-from-the-model-registry
#                            This parameter is read as a task value
#                            (https://learn.microsoft.com/azure/databricks/dev-tools/databricks-utils#get-command-dbutilsjobstaskvaluesget),
#                            rather than as a notebook widget. That is, we assume a preceding task (the Train.py
#                            notebook) has set a task value with key "model_uri".
##################################################################################

# COMMAND ----------

import os
notebook_path =  '/Workspace/' + os.path.dirname(dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get())
%cd $notebook_path

# COMMAND ----------

# MAGIC %pip install -r requirements.txt

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------
# DBTITLE 1, Helper function
from mlflow.tracking import MlflowClient


def deploy(model_uri):
    """Deploys an already-registered model in Unity catalog by assigning it the appropriate alias for model deployment.

    :param model_uri: URI of the model to deploy. Must be in the format "models:/<name>/<version-id>", as described in
                      https://www.mlflow.org/docs/latest/model-registry.html#fetching-an-mlflow-model-from-the-model-registry
    :return:
    """
    print(f"Deployment")
    _, model_name, version = model_uri.split("/")
    client = MlflowClient(registry_uri="databricks-uc")
    mv = client.get_model_version(model_name, version)
    target_alias = "Champion"
    if target_alias not in mv.aliases:
        client.set_registered_model_alias(
            name=model_name,
            alias=target_alias, 
            version=version)
        print(f"Assigned alias '{target_alias}' to model version {model_uri}.")
        
        # remove "Challenger" alias if assigning "Champion" alias
        if target_alias == "Champion" and "Challenger" in mv.aliases:
            print(f"Removing 'Challenger' alias from model version {model_uri}.")
            client.delete_registered_model_alias(
                name=model_name,
                alias="Challenger")

# COMMAND ----------

model_uri = dbutils.jobs.taskValues.get("Train", "model_uri", debugValue="")
assert model_uri != "", "model_uri notebook parameter must be specified"
deploy(model_uri)

# COMMAND ----------
print(
    f"Successfully completed model deployment for {model_uri}"
)