#!/bin/sh

#Once local docker container is running, can test Order table is in DDB container
aws dynamodb list-tables --endpoint-url http://localhost:8000
