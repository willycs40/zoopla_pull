1. create keys.py for zoopla api key
2. run docker built -t image_zp . 

3. Make the mysql 
docker pull mysql
docker run --name db -p 3306:3306 -e MYSQL_ROOT_PASSWORD=rootpass -e MYSQL_DATABASE=housing -e MYSQL_USER=will -e MYSQL_PASSWORD=housepass -d mysql
docker run -it --rm --name app --link db:mysql image_zp


https://hub.docker.com/_/python/
https://hub.docker.com/_/mysql/
https://scriptingmysql.wordpress.com/2011/09/09/retrieving-data-from-mysql-via-python/
