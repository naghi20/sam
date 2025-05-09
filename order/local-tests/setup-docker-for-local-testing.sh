#!/bin/sh

# Create local docker testing container for sam local invoke commands
docker run --name ddb-local -d -p 8000:8000 amazon/dynamodb-local

# Wait for container and port to be ready
echo "Waiting for DynamoDB Local to be ready..."

# Wait loop (max 10 seconds)
for i in {1..10}; do
  if curl -s http://localhost:8000 > /dev/null; then
    echo "DynamoDB Local is up!"
    break
  else
    echo "Still waiting... ($i)"
    sleep 1
  fi
done

# Check if container started successfully
if ! docker ps | grep -q ddb-local; then
  echo "DynamoDB Local container failed to start"
  exit 1
fi


TABLE_NAME="Order"
EVENT_FILE="events/order.json"

echo "Creating local DynamoDB table: $TABLE_NAME"
aws dynamodb create-table \
    --table-name "$TABLE_NAME" \
    --attribute-definitions AttributeName=order_id,AttributeType=S AttributeName=total_price,AttributeType=N \
    --key-schema AttributeName=order_id,KeyType=HASH AttributeName=total_price,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST \
    --endpoint-url http://localhost:8000 > /dev/null

echo "Waiting for table to exist..."
aws dynamodb wait table-exists \
    --table-name "$TABLE_NAME" \
    --endpoint-url http://localhost:8000


# Check status
if [ $? -eq 0 ]; then
  echo "DynamoDB table '$TABLE_NAME' is ready."
else
  echo "Failed to confirm DynamoDB table '$TABLE_NAME' exists." >&2
  exit 1
fi

#echo "Table exists. Describing..."
#aws dynamodb describe-table \
#    --table-name "$TABLE_NAME" \
#    --endpoint-url http://localhost:8000
