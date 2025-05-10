#!/bin/sh -xe

API_GW_URL=https://xs2hbyrem6.execute-api.eu-west-2.amazonaws.com/prod/checkout


curl -X POST $API_GW_URL \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": "12345",
    "item_id": "A1B2C3",
    "item_count": 2,
    "item_price": 19.99,
    "total_price": 39.98
  }'
