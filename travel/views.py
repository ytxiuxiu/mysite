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

            print data

            location = {
                'user_id': { 'N': str(user.id) },
                'battery': { 'N': str(data['batt']) },
                'waypoint': { 'S': str(data['desc']) },
                'event': { 'S': str(data['event']) },
                'latitude': { 'N': str(data['lat']) },
                'longitude': { 'N': str(data['lon']) },
                'radius': { 'N': str(data['rad']) },
                'network': { 'S': str(data['conn']) },
                'visited_at': { 'N': str(data['tst']) },
                'trigger': { 'S': str(data['t']) },
                'tracker_id': { 'S': str(data['tid']) },
            }
            if 'acc' in data:
                location['accuracy'] = { 'N': str(data['acc']) }
            if 'alt' in data:
                location['alt'] = { 'N': str(data['alt']) }
            if 'cog' in data:
                location['heading'] = { 'N': str(data['cog']) }
            if 'vac' in data:
                location['altitude_accurancy'] = { 'N': str(data['vac']) }
            if 'vel' in data:
                location['velocity'] = { 'N': str(data['vel']) }
            if 'p' in data:
                location['barometric_pressure'] = { 'N': str(data['p']) }


            result = client.put_item(
                TableName = 'locations',
                Item = location
            )
            return HttpResponse(str(result))


    response = HttpResponse()
    response.status_code = 401
    return response