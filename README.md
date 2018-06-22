# vocabulary_trainer
A simple Django vocabulary trainer

## Setup
Go to  directory vocabulary_trainer-master/vocabulary
```
pip install django
python manage.py makemigrations trainer
python manage.py migrate
python manage.py createsuperuser
```
Open http://localhost:8000/ in Browser

## Usage
First create vocabluary pairs in Django admin. Then add the pairs to a lesson.
