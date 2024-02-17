# Django project

## By Sakhbiev Damir

[![pipeline status](https://gitlab.crja72.ru/django/2024/spring/course/students/199049-sahbievdg-course-1112/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2024/spring/course/students/199049-sahbievdg-course-1112/-/commits/main)

### Prerequisites

1. Install Python:3.10
    * download link

    ```url
    https://www.python.org/downloads/release/python-3100/
    ```

2. Create virtual environment
    * python

    ```bash
    python -m venv venv
    ```

3. Activate virtual environment
    * windows

    ```bash
    .\venv\Scripts\activate
    ```

    * linux

    ```bash
    source venv/bin/activate
    ```

4. Upgrade pip
    * python

    ```bash
    python -m pip install --upgrade pip
    ```

### Installation

1. Clone the repo

   ```bash
   git clone git@gitlab.crja72.ru:django/2024/spring/course/students/199049-sahbievdg-course-1112.git
   ```

2. Install requirements
    * production

    ```bash
    pip install requirements/prod.txt
    ```

    * test

    ```bash
    pip install requirements/test.txt
    ```

    * devolopment

    ```bash
    pip install requirements/dev.txt
    ```

3. Use your configuration in .env.example
    * windows

    ```bash
    copy .env.example .env
    ```

    * linux

    ```bash
    cp .env.example .env
    ```

### Start

```bash
сd lyceum
python manage.py runserver
```
