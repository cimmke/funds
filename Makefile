build: Dockerfile ## create the prod build
	docker build -t cimmke/funds:latest .

build-dev: Dockerfile ## create the dev build
	docker build --build-arg DEVEL=yes -t cimmke/funds:dev .	

clean: ## remove prod and dev images
	docker rmi -f cimmke/funds:latest cimmke/funds:dev

outdated: ## Show outdated python packages
	docker run --rm cimmke/funds:latest pip list --outdated

db-destroy: ## Delete the database volumes
	docker volume rm funds_db_data

update: ## Get latest images
	docker pull python:3.9
	docker pull postgres:13