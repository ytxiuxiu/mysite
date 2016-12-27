import base64, json, boto3, time

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth import authenticate
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return HttpResponse("Hello, world. You're at the travel index.")

@require_http_methods(['POST'])
@csrf_exempt
def location(request):
    basic_auth = request.META['HTTP_AUTHORIZATION'].split()
    username, password = base64.b64decode(basic_auth[1]).split(':')
    user = authenticate(username = username, password = password)
    if user is not None and user.is_active:
        data = json.loads(request.body)
        if data['_type'] == 'location':
            client = boto3.client('dynamodb')
            result = client.put_item(
                TableName = 'locations',
                Item = {
                    'user_id': { 'N': str(user.id) },
                    'accuracy': { 'N': str(data['acc']) },
                    'visited_at': { 'N': str(int(time.time())) },
                }
            )
            print result


    response = HttpResponse()
    response.status_code = 401
    return response