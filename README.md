# Brightcore Project

### Requirements

* docker
* docker-compose

### Install Procedure

1. `docker-compose build`
2. `docker-compose up -d`
3. `docker exec -i -t brightcore_project bash`
4. `python init_db.py` -- Feel free to log out of the docker image after
   this
5. Access the site at localhost:32770

