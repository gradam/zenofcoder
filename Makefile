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
build-server:
	@docker-compose build server
build-client:
    @docker-compose build client
build-base:
	@docker build -t zenofcoder/base -f ./base/Dockerfile-base ./base
build-nginx:
	@docker-compose build nginx
build: build-data build-db build-nginx build-base build-server build-client


#run docker images
run-db:
	@docker-compose up data db
run-server:
	@docker-compose up server
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

CONTS-SERVER=$(shell docker ps -a -q -f "name=zenofcoder-web-server")
IMGS-SERVER=$(shell docker images -q -f "label=application=zenofcoder-web-server")

CONTS-CLIENT=$(shell docker ps -a -q -f "name=zenofcoder-web-client")
IMGS-CLIENT=$(shell docker images -a -q -f "name=zenofcoder-web-client")

CONTS-NGINX=$(shell docker ps -a -q -f "name=zenofcoder-nginx")
IMGS-NGINX=$(shell docker images -q -f "label=application=zenofcoder-nginx")

IMGS-BASE=$(shell docker images -q -f "label=application=zenofcoder-base")

#stop docker containers
stop-db:
	-@docker stop $(CONTS-DB)
stop-data:
	-@docker stop $(CONTS-DATA)
stop-server:
	-@docker stop --time=1 $(CONTS-SERVER)
stop-client:
    -@docker stop $(CONTS-CLIENT)
stop-nginx:
	-@docker stop $(CONTS-NGINX)
stop:
	@docker-compose down

#start docker containers
start-db:
	@docker start zenofcoder-data
	@docker start zenofcoder-db
start-server:
	@docker start zenofcoder-web-server
start-client:
    @docker start zenofcoder-web-client
start-nginx:
	@docker start zenofcoder-nginx
start: start-db start-server start-client start-nginx

#remove docker containers
rm-data:
	-@docker rm $(CONTS-DATA)
rm-db:
	-@docker rm $(CONTS-DB)
rm-server:
	-@docker rm $(CONTS-SERVER)
rm-client:
    -@docker rm $(CONTS-CLIENT)
rm-nginx:
	-@docker rm $(CONTS-NGINX)
rm: rm-db rm-server rm-client rm-nginx


#remove docker images
rmi-data:
	-@docker rmi -f $(IMGS-DATA)
rmi-db:
	-@docker rmi -f $(IMGS-DB)
rmi-server:
	-@docker rmi -f $(IMGS-SERVER)
rmi-client:
    -@docker rmi -f $(IMGS-CLIENT)
rmi-nginx:
	-@docker rmi -f $(IMGS-NGINX)
rmi-base:
	-@docker rmi -f $(IMGS-BASE)
rmi: rmi-db rmi-server rmi-client rmi-nginx


# stop containters, remove containers, remove images
clean-db: stop-db rm-db rmi-db
clean-server: stop-server rm-server rmi-server
clean-client: stop-client rm-client rmi-client
clean-nginx: stop-nginx rm-nginx rmi-nginx
clean-apps: clean-db clean-web clean-nginx
clean-base: rmi-base
clean-data: stop-data rm-data rmi-data
clean-compose:
	@docker-compose rm -f
clean-all: clean-db clean-server clean-client clean-nginx clean-data clean-base clean-compose

reload-nginx:
	@make clean-nginx
	@make build-nginx
	@make run-nginx


#rebuild images
rebuild: clean-all build

# open shell in container
shell-server:
	@docker exec -it zenofcoder-web-server bash
shell-client:
    @docker exec -it zenofcoder-web-client bash
shell-db:
	@docker exec -it zenofcoder-db bash

logs-server:
	@docker-compose logs -f | grep zenofcoder-web-server
logs-client:
    @docker-compose logs -f | grep zenofcoder-web-client
logs-db:
	@docker-compose logs -f | grep zenofcoder-db
logs-https:
	@docker-compose logs -f | grep zenofcoder-https
logs-testing:
	@docker-compose logs -f | grep zenofcoder-testing
logs:
	@docker-compose logs -f

# Reload static files in web container
reload_static:
	@docker exec zenfocoder-web python manage.py collectstatic --no-input

# Reload static files automatically after every change.
dev_static:
	@when-changed -1 -v -r `find ./zenofcoder-web/server/* -name 'static'` -c make reload_static
