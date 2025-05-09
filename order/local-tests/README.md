# README
simply execute ./invoke-lamda-test.sh

and this will call thecript setup-docker-for-local-testing.sh
to start the local DynamDB container in order to create the Order table.

Then lambda function willo get invoked and use custom env variables declared in env.json
to interact with local DDB container.

Once test complet, the container is removed.

All output is sent to stdout and test_output.json


Note:  ddb-test-commands.sh is just for aside testing to confirm table is in Docker DDB local container if ever there was a doubt.
