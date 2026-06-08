#!/bin/bash
#

if [ -z "$1" ]
then
    echo 'What env do you want to build?  (dev, prod)'
    exit 0
else
    echo "building $1"
fi

# build env
export ENV=$1

REGISTRY=docker-registry.oppenheimer.us:5000
WEBAPP=yip-webapp-$ENV
NGINX=yip-nginx-$ENV
POSTGRESQL=yip-postgresql

# compile angular code
if [ "$1" == 'prod' ]
then
    echo "Compiling angular code with prod environment set"
    cd webapp/yip-frontend
    /usr/bin/ng build --prod --output-path ../yip/static/angular --aot --output-hashing=none
    cd -

elif [ "$1" == 'dev' ]
then
    echo "Compiling angular code with dev environment set"
    cd webapp/yip-frontend
    /usr/bin/ng build --output-path ../yip/static/angular --aot --output-hashing=none
    cd -
fi

# deploy staticfiles to s3
aws s3 cp --recursive webapp/yip/static/angular s3://yoga-injury-prevention/static/angular --acl public-read --profile yip

# build tag and push webapp
docker build -t $WEBAPP ./webapp
docker tag $WEBAPP $REGISTRY/$WEBAPP:latest
docker push $REGISTRY/$WEBAPP:latest

# build tag and push nginx
docker build --build-arg ENV=${ENV} -t $NGINX ./nginx
docker tag $NGINX $REGISTRY/$NGINX:latest
docker push $REGISTRY/$NGINX:latest

# build tag and push postgresql
docker build -t $POSTGRESQL ./postgresql
docker tag $POSTGRESQL $REGISTRY/$POSTGRESQL:latest
docker push $REGISTRY/$POSTGRESQL:latest

# build tag and push rabbitmq
docker build -t rabbitmq ./rabbitmq
docker tag rabbitmq $REGISTRY/rabbitmq:latest
docker push $REGISTRY/rabbitmq:latest
