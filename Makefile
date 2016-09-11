VERSION=$(shell cat VERSION)

all:
	@make build
	@make run

VERSION=$(shell cat VERSION)
#building docker images for each service
build-db:
	@docker-compose build db
build-data:
	@docker-compose build data
build-web:
	@docker-compose build web
build-base:
	@docker build -t zenofcoder/base -f ./base/Dockerfile-base ./base
build-nginx:
	@docker-compose build nginx
build: build-data build-db build-nginx build-base build-web


#run docker images
run-db:
	@docker-compose up data db
run-web:
	@docker-compose up web
run-nginx:
	@docker-compose up nginx
run:
	@docker-compose up -d
# the only right way to run it on production
run-prod:
	@docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

#containers and images ids
CONTS-DB=$(shell docker ps -a -q -f "name=zenofcoder-db")
IMGS-DB=$(shell docker images -q -f "label=application=zenofcoder-db")

CONTS-DATA=$(shell docker ps -a -q -f "name=zenofcoder-data")
IMGS-DATA=$(shell docker images -q -f "label=application=zenofcoder-data")

CONTS-WEB=$(shell docker ps -a -q -f "name=zenofcoder-web")
IMGS-WEB=$(shell docker images -q -f "label=application=zenofcoder-web")

CONTS-NGINX=$(shell docker ps -a -q -f "name=zenofcoder-nginx")
IMGS-NGINX=$(shell docker images -q -f "label=application=zenofcoder-nginx")

IMGS-BASE=$(shell docker images -q -f "label=application=zenofcoder-base")

#stop docker containers
stop-db:
	-@docker stop $(CONTS-DB)
stop-data:
	-@docker stop $(CONTS-DATA)
stop-web:
	-@docker stop --time=1 $(CONTS-WEB)
stop-nginx:
	-@docker stop $(CONTS-NGINX)
stop:
	@docker-compose down

#start docker containers
start-db:
	@docker start zenofcoder-data
	@docker start zenofcoder-db
start-web:
	@docker start zenofcoder-web
start-nginx:
	@docker start zenofcoder-nginx
start: start-db start-web start-nginx

#remove docker containers
rm-data:
	-@docker rm $(CONTS-DATA)
rm-db:
	-@docker rm $(CONTS-DB)
rm-web:
	-@docker rm $(CONTS-WEB)
rm-nginx:
	-@docker rm $(CONTS-NGINX)
rm: rm-db rm-web rm-nginx


#remove docker images
rmi-data:
	-@docker rmi -f $(IMGS-DATA)
rmi-db:
	-@docker rmi -f $(IMGS-DB)
rmi-web:
	-@docker rmi -f $(IMGS-WEB)
rmi-nginx:
	-@docker rmi -f $(IMGS-NGINX)
rmi-base:
	-@docker rmi -f $(IMGS-BASE)
rmi: rmi-db rmi-web rmi-nginx


# stop containters, rmove containers, remove images
clean-db: stop-db rm-db rmi-db
clean-web: stop-web rm-web rmi-web
clean-nginx: stop-nginx rm-nginx rmi-nginx
clean-apps: clean-db clean-web clean-nginx
clean-base: rmi-base
clean-data: stop-data rm-data rmi-data
clean-compose:
	@docker-compose rm -f
clean-all: clean-db clean-web clean-nginx clean-data clean-base clean-compose

reload-nginx:
	@make clean-nginx
	@make build-nginx
	@make run-nginx


#rebuild images
rebuild: clean-all build

# open shell in container
shell-web:
	@docker exec -it zenofcoder-web bash
shell-db:
	@docker exec -it zenofcoder-db bash

logs:
	@docker-compose logs

# Reload static files in web container
reload_static:
	@docker exec zenfocoder-web python manage.py collectstatic --no-input

# Reload static files automatically after every change.
dev_static:
	@when-changed -1 -v -r `find ./zenofcoder-web/* -name 'static'` -c make reload_static
