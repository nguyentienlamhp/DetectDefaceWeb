#!/bin/bash

exec service cron start &
exec echo "MONGODB_USERNAME=${MONGODB_USERNAME}" >> /etc/environment &
exec echo "MONGODB_PASSWORD=${MONGODB_PASSWORD}" >> /etc/environment &
exec echo "MONGODB_HOSTNAME=${MONGODB_HOSTNAME}" >> /etc/environment & 
exec echo "API_URL=${API_URL}" >> /etc/environment & 
exec /usr/bin/python3 /opt/In0ri/FlaskApp/app.py &
exec /usr/bin/python3 /opt/In0ri/api.py