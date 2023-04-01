# Makefile

##@ Documentation
docs-build: ## build documentation locally
   @mkdocs build
docs-deploy: ## build & deploy documentation to "gh-pages" branch
   @mkdocs gh-deploy -m "docs: update documentation" -v --force
clean-docs: ## remove output files from mkdocs
   @rm -rf site