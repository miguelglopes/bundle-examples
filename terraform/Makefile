.PHONY: lint plan apply


lint:
	terraform validate
	terraform fmt
	tflint

plan: lint
	terraform plan

apply: lint
	terraform apply
	terraform output -json | jq -r 'to_entries[] | "\(.key)=\(.value.value)"' > ../mlops_stacks/.env