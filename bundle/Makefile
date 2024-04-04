.PHONY: install-dependencies validate-bundle deploy-bundle run-train-remote run-inference-remote run-bundle-remote

include .env

BUNDLE_TARGET?=research
SCHEMA_NAME?=${schema}
CATALOG_NAME?=${catalog}
MODEL_NAME?=mgl
EXPERIMENT_NAME?=mgl

install-dependencies:
	curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh

validate-bundle:
	databricks bundle validate -t $(BUNDLE_TARGET) --var="model_name=$(MODEL_NAME),schema_name=$(SCHEMA_NAME),catalog_name=$(CATALOG_NAME),experiment_name=$(EXPERIMENT_NAME)"

deploy-bundle:
	databricks bundle deploy -t $(BUNDLE_TARGET) --var="model_name=$(MODEL_NAME),schema_name=$(SCHEMA_NAME),catalog_name=$(CATALOG_NAME),experiment_name=$(EXPERIMENT_NAME)"

run-bundle-remote:
	databricks bundle run -t $(BUNDLE_TARGET) model_training_job --no-wait --var="model_name=$(MODEL_NAME),schema_name=$(SCHEMA_NAME),catalog_name=$(CATALOG_NAME),experiment_name=$(EXPERIMENT_NAME)"
