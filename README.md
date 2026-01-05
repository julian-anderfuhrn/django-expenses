# Expenses Tracker

Web app developed with Django to manage personal expenses for users

## Objective

This project was created for educaional purposes to practice:
- Django(models, views, forms, auth)
- Relations between models
- CRUD
- Basic good practices(env vars, git, refactor)

## Functionalities

- User authentication
- CRUD of expenses
- CRUD of categories
- Monthly dashboard
- Route protection

## Technologies

- Python 3
- Django
- SQLite
- HTML / CSS

## Installation
1 Clone the repository

``` bash
git clone https://github.com/julian-anderfuhrn/django-expenses
cd django-expenses

2 Create the virtual environment
python -m venv venv
venv\Scripts\activate

3 install dependencies
pip install -r requirements.txt

4 create the .env file
SECRET_KEY=your_secret_key
DEBUG=True

5 Execute migrations and server
python manage.py migrate
python manage.py runserver