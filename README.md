# True Safeguard

Basic Django project setup for the True Safeguard website.

## Quick start (testing locally on your device)

1) Create and activate the virtual environment:

- Linux/macOS:
	- `python3 -m venv .venv`
	- `source .venv/bin/activate`

2) Install dependencies:

- `pip install django`

3) Run migrations and start the server:

- `python manage.py migrate`
- `python manage.py runserver`

Open http://127.0.0.1:8000/ to see the home page.

## 🐳 Docker Development Environment
We have switched to a Dockerized setup to ensure environment consistency.

## First-Time Setup

1) Pull the latest changes:

	- `git checkout main`
	- `git pull origin main`

2) Create your .env file:
Create a file named .env in the root directory and add:

- `DEBUG=True`
- `SECRET_KEY=local-dev-key-123`
- `DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0`

3) Build the image:

	- `docker build -t django-app .`

## Running the App

1) Start the container with the following command:

	- `docker run -p 8000:8000 --env-file .env django-app`

Migrations: Database migrations run automatically on startup.

2) URL: Visit http://localhost:8000 to see the site.

## Management Commands
To run commands inside the running container (e.g., creating a user):

- `docker exec -it $(docker ps -q --filter ancestor=django-app) python manage.py createsuperuser`