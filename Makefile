# Makefile for Terraform operations
.PHONY: help init plan apply destroy validate format check clean

# Default target
help:
	@echo "Available targets:"
	@echo "  init      - Initialize Terraform"
	@echo "  validate  - Validate Terraform configuration"
	@echo "  format    - Format Terraform files"
	@echo "  plan      - Create Terraform execution plan"
	@echo "  apply     - Apply Terraform configuration"
	@echo "  destroy   - Destroy Terraform-managed infrastructure"
	@echo "  check     - Run validation and formatting checks"
	@echo "  clean     - Clean Terraform cache and state backup files"

# Initialize Terraform
init:
	terraform init

# Validate configuration
validate:
	terraform validate

# Format Terraform files
format:
	terraform fmt -recursive

# Create execution plan
plan:
	terraform plan

# Apply configuration
apply:
	terraform apply

# Destroy infrastructure (use with caution!)
destroy:
	@echo "WARNING: This will destroy all Terraform-managed resources!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		terraform destroy; \
	else \
		echo "Destroy cancelled."; \
	fi

# Run all checks
check: validate format
	@echo "All checks passed!"

# Clean up temporary files
clean:
	rm -rf .terraform/
	rm -f .terraform.lock.hcl
	rm -f terraform.tfstate.backup
	rm -f *.tfplan

# Development workflow
dev-setup: init validate format plan

# Production deployment workflow
prod-deploy: init validate plan
	@echo "Ready for production deployment. Run 'make apply' to proceed."