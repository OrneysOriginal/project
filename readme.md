## Проект запускается на версиях питона 3.10, 3.11, 3.12
[![pipeline status](https://gitlab.crja72.ru/django/2024/spring/course/students/199562-sav1ngeorgiy-course-1112/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2024/spring/course/students/199562-sav1ngeorgiy-course-1112/-/commits/main)

### Для Windows:
* Создать виртуальную среду
```bash
python -m venv venv
```
* Активировать её
```bash
venv/Script/activate
```
* Скачать все продовые зависимости командой
```bash
pip install -r requirements/prod.txt
```
* Перейти в lyceum и прописать в терминале:
```bash
python manage.py runserever
```

## Для Linux(запускаемся из папки проекта):
* Установка виртуально среды
```bash
$ pip3 install virtualenv
```
* Активация виртуальной среды
```bash
$ source env/bin/activate
```
* Установка всех продовых зависимостей
(python3 или python, смотря какой у вас питон установлен)
```bash
$ python3 -m pip install -r requirements/prod.txt
```
* Меняем директорию
(project - это имя вашего проекта)
```bash
cd project
```
* Запускаем проект
(python3 или python, смотря какой у вас питон установлен)
```bash
$ python3 manage.py runserver - запускаем проект
```

### Веб сервер джанго запущен :)
