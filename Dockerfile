FROM python
WORKDIR /app
COPY /app .
RUN pip install -r requirements/test.txt