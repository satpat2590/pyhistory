# Configuring Docker Containers for MySQL 

docker run --name basic-mysql --rm -v /tmp/mysql-data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=genericpassword -e MYSQL_DATABASE=testing -p 3307:3306 -it mysql:latest