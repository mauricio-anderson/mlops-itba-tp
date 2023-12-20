
hello:
	echo "Hello, World"

add-kernel:
	poetry run python -m ipykernel install --user --name=mlops-itba-tp

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
