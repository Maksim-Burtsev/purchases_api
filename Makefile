run:
	uvicorn main:app --reload

req:
	pip freeze > requirements.txt