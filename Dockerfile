FROM python:latest 
WORKDIR /app
COPY ./app . 
RUN pip install -r requirements.txt 
ENV MYSQL_HOST_TEST=localhost
ENV MYSQL_DATABASE_TEST=tutorial
ENV MYSQL_USER_TEST=root
ENV MYSQL_PASSWORD_TEST=Ningning1231??
RUN apt-get update
RUN apt-get install -y default-mysql-client
EXPOSE 80 
CMD ["tail", "-f", "/dev/null"]