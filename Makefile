build-docker:
	docker build -t habitus_statistics_ms .

run-docker:
	docker run --env-file .env -d -p 8000:8000 --name habitus_statistics_ms habitus_statistics_ms

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload