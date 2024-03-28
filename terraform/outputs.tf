output "catalog" {
  value = databricks_catalog.research_test_catalog.name
}

output "schema" {
  value = databricks_schema.research_test_schema.name
}