import boto3
from boto3.dynamodb.conditions import Key

dy = boto3.resource('dynamodb')


def replace_in_dynamo(table_name, item):
	table = dy.Table(table_name)
	table.put_item(Item=item)


def get_from_dynamo(table_name, key, proj_expr):
	table = dy.Table(table_name)
	res = table.get_item(Key=key, ProjectionExpression=proj_expr)
	
	return res.get('Item')


def update_in_dynamo(table_name, key, update_expr, expr_attr_vals):
	table = dy.Table(table_name)
	table.update_item(Key=key, UpdateExpression=update_expr, ExpressionAttributeValues=expr_attr_vals)


def delete_from_dynamo(table_name, key):
	table = dy.Table(table_name)
	table.delete_item(Key=key)


def query_dynamo(table_name, key, proj_expr, expr_attr_names=None):
	table = dy.Table(table_name)
	res = table.query(KeyConditionExpression=key, ProjectionExpression=proj_expr, ExpressionAttributeNames=expr_attr_names)
	
	return res.get('Items')


# print(query_dynamo('prod_watchlist', Key('user_id').eq('123'), 'list_id, #items', {'#items': 'items'}))
