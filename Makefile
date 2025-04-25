up:
	docker-compose up -d --build

down:
	docker-compose down

test:
	poetry run pytest -s -vv

lint:
	poetry run pre-commit run --all-files

shell:
	docker-compose exec web bash

logs:
	docker-compose logs -f web

migrate:
	docker-compose exec web alembic revision --autogenerate -m "$(m)"

upgrade:
	docker-compose exec web alembic upgrade head

migrate-internal:
	alembic -c src/alembic.ini revision --autogenerate -m "$(m)"

upgrade-internal:
	alembic -c src/alembic.ini upgrade head
