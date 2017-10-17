#!/usr/bin/env sh

docker run \
	-p 27017:27017 \
	-v /opt/mongodb/db:/data/db \
	--name my-mongo-dev \
	-d \
	mongo mongod --auth
