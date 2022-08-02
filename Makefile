run:
	cd ./api && uvicorn main:app --reload

req:
	pip freeze > requirements.txt

test:
	pytest