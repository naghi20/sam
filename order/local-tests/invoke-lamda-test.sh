#!/bin/sh

clear

EVENT_FILE="../events/order.json"

# Start local docker container with local DDB
./setup-docker-for-local-testing.sh

echo "Invoking Lambda function locally..."
sam local invoke OrderProcessorFunction \
    --template ../template.yaml  \
    --event "$EVENT_FILE" \
    --env-vars env.json \
    2>&1 | tee test_output.log

echo "Test complete, removing local DDB container"
#Once test ends, kill DDB Container
docker container rm -f ddb-local


echo "done."

