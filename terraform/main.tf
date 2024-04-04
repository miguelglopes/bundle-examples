terraform {
  required_version = ">= 1.0"
  required_providers {
    databricks = {
      source  = "databricks/databricks"
      version = "1.38.0"
    }
  }
}

# this wil lbe set here for now, they'll be variables in the future
locals {
  inference_metastore_id = "aws:us-east-1:c7df54a7-a8aa-49d9-b3fb-5af6ecd5bfb9"
  research_metastore_id  = "aws:eu-west-1:c4224c23-ed75-4fff-a21e-3e65cb93e35a"
  iteration              = 4
  pipeline_user          = "42c5f20a-2787-46aa-9e62-0e80e69865cd"
  ai_platform_group      = "SGIA_TEAM_RD_AI_Platform"
}
################# RESEARCH #################

# this assumes ~/.databrickscfg has a profile named RESEARCH configured
provider "databricks" {
  alias   = "research"
  profile = "RESEARCH"
}

resource "databricks_catalog" "research_test_catalog" {
  provider = databricks.research
  name     = "test${local.iteration}"
  comment  = "this catalog is managed by terraform"
}

resource "databricks_grants" "research_test_catalog_grants" {
  provider = databricks.research
  catalog  = databricks_catalog.research_test_catalog.name
  grant {
    principal  = local.ai_platform_group
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = local.pipeline_user
    privileges = ["ALL_PRIVILEGES"]
  }
}

resource "databricks_schema" "research_test_schema" {
  provider     = databricks.research
  catalog_name = databricks_catalog.research_test_catalog.id
  name         = "test${local.iteration}"
}

resource "databricks_grants" "research_test_schema_grants" {
  provider = databricks.research
  schema   = databricks_schema.research_test_schema.id
  grant {
    principal  = local.ai_platform_group
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = local.pipeline_user
    privileges = ["ALL_PRIVILEGES"]
  }
}

resource "databricks_recipient" "research_test_recipient" {
  provider                           = databricks.research
  name                               = "test${local.iteration}"
  authentication_type                = "DATABRICKS"
  data_recipient_global_metastore_id = local.inference_metastore_id
}

resource "databricks_share" "research_test_share" {
  provider = databricks.research
  name     = "test${local.iteration}"
  object {
    name                        = "test${local.iteration}.test${local.iteration}"
    data_object_type            = "SCHEMA"
    history_data_sharing_status = "ENABLED"
  }
}

resource "databricks_grants" "research_test_share_grants" {
  provider = databricks.research
  share    = databricks_share.research_test_share.name
  grant {
    principal  = databricks_recipient.research_test_recipient.name
    privileges = ["SELECT"]
  }
}
################# INFERENCE #################

# # this assumes ~/.databrickscfg has a profile named INFERENCE configured
provider "databricks" {
  alias   = "inference"
  profile = "INFERENCE"
}

resource "databricks_catalog" "inference_test_catalog" {
  provider      = databricks.inference
  name          = "test${local.iteration}"
  share_name    = databricks_share.research_test_share.name
  provider_name = local.research_metastore_id
}

resource "databricks_grants" "inference_test_catalog_grants" {
  provider = databricks.inference
  catalog  = databricks_catalog.inference_test_catalog.name
  grant {
    principal  = local.ai_platform_group
    privileges = ["BROWSE", "APPLY_TAG", "USE_CATALOG", "EXECUTE", "MODIFY", "SELECT", "READ_VOLUME", "USE_SCHEMA"]
  }
  grant {
    principal  = local.pipeline_user
    privileges = ["BROWSE", "APPLY_TAG", "USE_CATALOG", "EXECUTE", "MODIFY", "SELECT", "READ_VOLUME", "USE_SCHEMA"]
  }
}