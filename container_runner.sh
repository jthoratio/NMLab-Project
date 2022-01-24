#!/bin/bash
for i in {1..25}
do
  docker run -t -d --name test${i} -e MYSQL_ROOT_PASSWORD=1234 -p 3306:3306 mysql:latest 
  quo=$((i/5))
  rem=$((i%5))
  sleep 30
  
  if [ $quo -eq 0 ];
  then
    docker exec -it test${i} mysqlslap -u root -p1234 --concurrency=20 --number-of-queries=20 --auto-generate-sql
  elif [ $quo -eq 1 ];
  then
    docker exec -it test${i} mysqlslap -u root -p1234 --concurrency=5 --iterations=3 --number-int-cols=2 --number-char-cols=3 --auto-generate-sql
  elif [ $quo -eq 2 ];
  then
    docker exec -it test${i} mysqlslap -u root -p1234 --concurrency=5 --iterations=5 --query=query.sql --create=create.sql --delimiter=";"
  elif [ $quo -eq 3 ];
  then
    docker exec -it test${i} mysqlslap -u root -p1234 --concurrency=5 --number-of-queries=10 --auto-generate-sql
  elif [ $quo -eq 4 ];
  then
    docker exec -it test${i} mysqlslap -u root -p1234 --concurrency=5 --iterations=3 --number-int-cols=10 --number-char-cols=10 --auto-generate-sql
  fi
  

  sqlmap -u 0.0.0.0:3306?id=1 -a --batch --risk=3


   if [ $rem -eq 0 ];
  then
    docker exec -it test${i} mysqlslap -u root -p1234 --concurrency=20 --number-of-queries=20 --auto-generate-sql
  elif [ $rem -eq 1 ];
  then
    docker exec -it test${i} mysqlslap -u root -p1234 --concurrency=5 --iterations=3 --number-int-cols=2 --number-char-cols=3 --auto-generate-sql
  elif [ $rem -eq 2 ];
  then
    docker exec -it test${i} mysqlslap -u root -p1234 --concurrency=5 --iterations=5 --query=query.sql --create=create.sql --delimiter=";"
  elif [ $rem -eq 3 ];
  then
    docker exec -it test${i} mysqlslap -u root -p1234 --concurrency=5 --number-of-queries=10 --auto-generate-sql
  elif [ $rem -eq 4 ];
  then
    docker exec -it test${i} mysqlslap -u root -p1234 --concurrency=5 --iterations=3 --number-int-cols=10 --number-char-cols=10 --auto-generate-sql
  fi



  docker stop test${i}
  docker rm test${i}
  docker volume prune -f
  sleep 5
done
