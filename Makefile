
hello:
	echo "Hello, World"

add-kernel:
	poetry run python -m ipykernel install --user --name=mlops-itba-tp

build-image:
	docker build -t mlops-itba .

start-env:
	docker-compose --env-file .env up

start-airbyte:
	./airbyte/run-ab-platform.sh

start-dagster:
	poetry run dagster dev

run-black:
	poetry run black mlops_itba_tp/*

run-isort:
	poetry run isort mlops_itba_tp/*

run-pylint:
	poetry run pylint mlops_itba_tp/*
