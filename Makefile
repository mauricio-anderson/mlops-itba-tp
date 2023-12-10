
hello:
	echo "Hello, World"

add-kernel:
	poetry run python -m ipykernel install --user --name=mlops-itba-tp

start-env:
	docker-compose --env-file .env up

start-airbyte:
	./airbyte/run-ab-platform.sh
