.PHONY: install-dependencies validate-bundle deploy-bundle run-train-remote run-inference-remote run-bundle-remote

BUNDLE_TARGET?=research
SCHEMA_NAME?=$(shell sh -c "terraform -chdir=../terraform output -raw schema")
CATALOG_NAME?=$(shell sh -c "terraform -chdir=../terraform output -raw catalog")
MODEL_NAME?=mgl
EXPERIMENT_NAME?=/Users/42c5f20a-2787-46aa-9e62-0e80e69865cd/mgl

install-dependencies:
	curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh

validate-bundle:
	databricks bundle validate -t $(BUNDLE_TARGET) --var="model_name=$(MODEL_NAME),schema_name=$(SCHEMA_NAME),catalog_name=$(CATALOG_NAME),experiment_name=$(EXPERIMENT_NAME)"

deploy-bundle:
	databricks bundle deploy -t $(BUNDLE_TARGET) --var="model_name=$(MODEL_NAME),schema_name=$(SCHEMA_NAME),catalog_name=$(CATALOG_NAME),experiment_name=$(EXPERIMENT_NAME)"

run-train-remote:
	if [ $(BUNDLE_TARGET) = "research" ]; then \
		databricks bundle run -t $(BUNDLE_TARGET) model_training_job --no-wait --var="model_name=$(MODEL_NAME),schema_name=$(SCHEMA_NAME),catalog_name=$(CATALOG_NAME),experiment_name=$(EXPERIMENT_NAME)"; \
	fi

run-inference-remote:
	databricks bundle run -t $(BUNDLE_TARGET) batch_inference_job --no-wait --var="model_name=$(MODEL_NAME),schema_name=$(SCHEMA_NAME),catalog_name=$(CATALOG_NAME),experiment_name=$(EXPERIMENT_NAME)"

run-bundle-remote: run-train-remote run-inference-remote
	
