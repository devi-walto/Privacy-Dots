###########################################
# File was programmed by Diego and Carson #
###########################################

from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.urls import path
from datetime import datetime
import time
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Device

# Create your views here.
def home(request):
    return render(request, "home.html")


# function that checks for POST requests from the Pi 
@csrf_exempt  # Disable CSRF protection 
def motion_detected(request):

    if request.method == 'POST':
        try:
            # Get the motion data from the request body
            motion_data = json.loads(request.body)

            # gets the information from the connected nodes (name, location)
            node_id = motion_data.get('node_id')
            location = motion_data.get('location', 'Unknown') 
            motion_detected = motion_data.get('motion_detected', False)
            print("Received motion data:", motion_data)

            # Store or update the Node information in the database
            node, created = Device.objects.get_or_create(node_id=node_id, defaults={'location': location})

            # Notify if motion is detected
            if motion_detected:
                send_push_notification(
                    title="Motion Detected",
                    body=f"Motion detected at {location} (Node ID: {node_id})"
                )

            return JsonResponse({'status': 'success', 'data': motion_data}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=405)

# send a push notification to the Webapp using  Expo Push Notification
def send_push_notification(title, body):
    url = "https://exp.host/--/api/v2/push/send"
    headers = {
        "Content-Type": "application/json",
        "Accept": 'application/json',
    }

    # Since we are only using one Dots we could hardcode the tokens 
    # Hardcoded the Expo push token for the webapp
    push_token = "ExponentPushToken[wkpAV-AHN5ifQ-X48fi3Nr]" 

    data = {
        "to": push_token,
        "sound": "default",
        "title": title,
        "body": body,
    }


    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            print("Notification sent successfully")
        else:
            print(f"Failed to send notification: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending notification: {e}")
