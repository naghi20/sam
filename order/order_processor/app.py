import json
import os
import boto3
import socket
from botocore.exceptions import ClientError
# DynamoDB requires that numerical types with decimals be represented with the Decimal class, which maintains precision
from decimal import Decimal

# When you invoke your Lambda locally using sam local invoke, the SAM CLI sets the environment variable AWS_SAM_LOCAL to true by default.
# os.environ.get looks for environment variables that are available defined for the Lambda execution context when using SAM local.
IS_LOCAL = os.environ.get("AWS_SAM_LOCAL", False)

# Get EC2 private IP if running on EC2
# If you are running DynamoDB in a Docker container on your EC2 instance, you should use the private IP of the EC2 instance.
# FYI: localhost (or 127.0.0.1) inside your Lambda running on EC2 refers to the EC2 instance itself, not the Docker container running DynamoDB.
ec2_private_ip = os.environ.get("EC2_PRIVATE_IP", "localhost")

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=f"http://{ec2_private_ip}:8000" if IS_LOCAL else None
)

# Initialize DynamoDB resource
order_table_name = os.environ.get("ORDER_TABLE_NAME")
table = dynamodb.Table(order_table_name)

def lambda_handler(event, context):
    #print("Environment Variables:", os.environ)

    print (f"IS_LOCAL: {IS_LOCAL} for dynamodb at EC2_PRIVATE_IP: {ec2_private_ip} ");

    # Log the event received from SNS
    print("Received event: " + json.dumps(event, indent=2))
    
    # Extract the SNS message from the event
    sns_message = event['Records'][0]['Sns']['Message']
    message = json.loads(sns_message)  # Parse the message into a Python dictionary
    
    try:
        # Parse the JSON message
        order = json.loads(sns_message)
        
        # Get order details
        order_id = order.get('order_id')
        item_id = order.get('item_id')
        item_count = order.get('item_count')
        item_price  = Decimal(str(message['item_price']))   # Convert float to Decimal
        total_price = Decimal(str(message['total_price']))  # Convert float to Decimal 

        # Log the order details
        print(f"Order details - Order ID: {order_id}, Item ID: {item_id}, Item Count: {item_count}, Item Price: {item_price}, Total Price: {total_price}")
        print(f"order_table_name: {order_table_name}")
        
        # Save the order to DynamoDB
        response = table.put_item(
            Item={
                'order_id': order_id,
                'total_price': total_price,
                'item_id': item_id,
                'item_count': item_count,
                'item_price': item_price
            }
        )
        
        # Log DynamoDB response
        print("DynamoDB Response: " + json.dumps(response, indent=2))
        
        # Return a success message
        return {
            'statusCode': 200,
            'body': json.dumps('Order successfully processed and saved to DynamoDB')
        }
        
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid JSON in SNS message')
        }
    except KeyError as e:
        print(f"KeyError: Missing key in JSON message - {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps(f'Missing key in SNS message: {str(e)}')
        }
    except ClientError as e:
        print(f"ClientError: Unable to save order to DynamoDB - {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to save order to DynamoDB')
        }
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }

