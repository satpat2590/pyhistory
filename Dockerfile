FROM python:latest 
WORKDIR /app
COPY . . 
RUN cat app/requirements.txt 
RUN ls 
EXPOSE 80 