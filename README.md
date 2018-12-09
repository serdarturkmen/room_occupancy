* Use Django and Django Rest Framework to implement back-end part
* Use Angular 2+ to implement front end part
* Use Mysql as database
* Use web sockets for communication between the frontend and backend part

###Start Project

####start mysql with docker:
docker-compose -f docker/mysql.yml up
python3 manage.py makemigrations rooms
python3 manage.py migrate

#### start redis
docker run -p 6379:6379 -d redis:2.8

##### sample data insert with shell
python3 manage.py shell
from rooms.models import Room
room = Room(name="first", count=1)
room.save()