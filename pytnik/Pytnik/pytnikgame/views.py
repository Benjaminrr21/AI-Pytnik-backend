from http.client import HTTPResponse
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import algorithams
from .algorithams import JockePath,AkiPath, MickoPath, UkiPath


@csrf_exempt
def pytnik(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print('Received data:', data)

            # Process the data as needed
            matrix = data['matrica']
            response_data = {"status": "success"}
            print(response_data)
            if data['agent'] == 'Aki' :
                return JsonResponse({"path":AkiPath(matrix)})
            if data['agent'] == 'Micko' :
                return JsonResponse({"path":MickoPath(matrix)})
            if data['agent'] == 'Uki':
                return JsonResponse({"path":UkiPath(matrix)})
            if data['agent'] == 'Jocke':
                return JsonResponse({"path":JockePath(matrix)})
            return HttpResponse("What is the problem??")
        except json.JSONDecodeError as e:
            print('Invalid JSON format:', request.body.decode('utf-8'))
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)

   # return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
        

""" @csrf_exempt  # Use only for testing purposes; CSRF should be enabled in production
def pytnik(request):
    if request.method == 'POST':
        try:
            # Assuming your JSON data is in the request body
            data = json.loads(request.body)
            
            # Access the 'matrica' key from the JSON data
            #path = data.get('matrica', [])
            
            # Process the 'path' as needed
            # ...

            return JsonResponse({"success": "Aaa"})
        except json.JSONDecodeError as e:
            # Handle JSON decoding error
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    else:
        # Handle other HTTP methods if necessary
        return JsonResponse({"error": "Unsupported method"}, status=405) """
