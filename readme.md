[![pipeline status](https://gitlab.crja72.ru/django/2024/spring/course/students/199562-sav1ngeorgiy-course-1112/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2024/spring/course/students/199562-sav1ngeorgiy-course-1112/-/commits/main)
[![flake8](https://img.shields.io/badge/flake8-passed-green?labelColor=gray&style=flat)](https://gitlab.crja72.ru/django/2024/spring/course/students/199562-sav1ngeorgiy-course-1112/-/commits/main)
[![black](https://img.shields.io/badge/black-passed-green?labelColor=gray&style=flat)](https://gitlab.crja72.ru/django/2024/spring/course/students/199562-sav1ngeorgiy-course-1112/-/commits/main)
[![adrestest](https://img.shields.io/badge/adrestest-passed-green?labelColor=gray&style=flat)](https://gitlab.crja72.ru/django/2024/spring/course/students/199562-sav1ngeorgiy-course-1112/-/commits/main)


Проект запускается на версиях питона 3.10, 3.11, 3.12

Чтобы запустить проект на Windows нужно:
В корне проекта прописать команду:
python -m venv venv - Чтобы установить виртуальное окружение
Далее:
venv/Script/activate - чтобы активировать виртуальное окружение
После скачать все продовые зависимости командой:
pip install -r requirements/prod.txt
Потом перейти в lyceum и прописать в терминале:
python manage.py runserever
Веб сервер джанго запущен :)

Для Linux(запускаемся из папки проекта):
$ pip3 install virtualenv - устанавливаем виртуальную среду
$ source env/bin/activate - запускаем виртуальную среду
(projects - это имя вашего проекта)
$ python3 -m pip install -r requirements/prod.txt
(python3 или python, смотря какой у вас питон установлен)
$ python3 manage.py runserver - запускаем проект
(python3 или python, смотря какой у вас питон установлен)
Веб сервер джанго запущен :)
