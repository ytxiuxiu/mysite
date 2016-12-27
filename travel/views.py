import base64, json, boto3, time, os

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
            if 'DYNAMODB_REGION' in os.environ:
                client = boto3.client('dynamodb', region_name = os.environ['DYNAMODB_REGION'])
            else:
                client = boto3.client('dynamodb');
            result = client.put_item(
                TableName = 'locations',
                Item = {
                    'user_id': { 'N': str(user.id) },
                    'accuracy': { 'N': str(data['acc']) },
                    'altitude': { 'N': str(data['alt']) },
                    'battery': { 'N': str(data['batt']) },
                    'heading': { 'N': str(data['cog']) },
                    'waypoint': { 'S': str(data['desc']) },
                    'event': { 'S': str(data['event']) },
                    'latitude': { 'N': str(data['lat']) },
                    'longitude': { 'N': str(data['lon']) },
                    'radius': { 'N': str(data['rad']) },
                    'altitude_accurancy': { 'N': str(data['acc']) },
                    'velocity': { 'N': str(data['vel']) },
                    'barometric_pressure': { 'N': str(data['p']) },
                    'network': { 'S': str(data['conn']) },
                    'visited_at': { 'N': str(data['tst']) },
                }
            )
            return HttpResponse(str(result))


    response = HttpResponse()
    response.status_code = 401
    return response