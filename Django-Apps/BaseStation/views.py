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

def home(request):
    return render(request, "home.html")


@csrf_exempt  # Disable CSRF protection for this view (not recommended for production)
# function that receives the post request ftom the rasberry pi
def motion_detected(request):
    now = datetime.now()
    formatted_time = now.strftime("%H:%M")

    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            motion_data = json.loads(request.body)

            print("Received motion data:", motion_data)

            send_push_notification(title="Motion Detected", body=f"Location: Office ")

            return JsonResponse({'status': 'success', 'data': motion_data}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=405)


# when it recieves the post request, it sends a push notifiaction to the react native app, using Expo push notification.
def send_push_notification(title, body):
    url = "https://exp.host/--/api/v2/push/send"
    headers = {
        "Content-Type": "application/json",
        "Accept": 'application/json',
    }

    # Hardcoded Expo push token 
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
