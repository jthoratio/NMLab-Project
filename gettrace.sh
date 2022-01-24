#!/bin/bash

LOGNAME="log.txt"
if [ -f $LOGNAME ];
then
  rm $LOGNAME
fi
touch $LOGNAME

if [ -d trace_data ];
then
  rm trace_data/*  
  rm -d trace_data
  mkdir trace_data
fi

docker events -f event=create >> $LOGNAME &
while inotifywait -qq -e modify $LOGNAME;
do
  sleep 30
  LAST=$(tail -1 $LOGNAME)
  CNAME=$(echo $LAST)
  NAME=$(echo $CNAME | awk '{split($0, a, "=")}{print substr(a[3], 0, length(a[3])-1)}')
  timeout 3 sysdig -p"%evt.type" container.name=$NAME >> trace_data/$NAME 
done
    
