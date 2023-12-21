
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
	poetry run black mlops_itba_tp/*

run-pylint:
	poetry run black mlops_itba_tp/*

run-flake8:
	poetry run flake8 mlops_itba_tp/*

run-mypy:
	poetry run mypy mlops_itba_tp/*
