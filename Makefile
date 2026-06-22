# Makefile
run-backend:
	cd backend && uvicorn main:app --reload

run-frontend:
	cd frontend && ng serve