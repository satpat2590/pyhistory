FROM python:latest 
WORKDIR /app
COPY ./app . 
RUN pip install -r requirements.txt 
RUN apt-get update
RUN apt-get install -y default-mysql-client
RUN apt-get install -y neovim 
EXPOSE 80 
CMD ["tail", "-f", "/dev/null"]