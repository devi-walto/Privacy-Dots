import requests

 #put your ip in here from whatever wifi you're connected to 
django_url = "http://{server_ip}:8000/pucks/collect/"

data = { # this is the data dictionary and how everything is transported
    "node_id":"node_testing", #this is how node id's can be assigned
    "sensor_data": "insert data here", #I don't actually know how the sensor prints data so heres that
    "time_stamp" : "I want this to work it currently shows null" # this gives a time stamp 
}

try:  
    #this is the actual post being requested with the url and data 
    response = requests.post(django_url, json=data)

    # this is for troubleshooting and notifications of saving
    if response.status_code == 201:
        print("data_saved")
    else:
        print("bad data", response.status_code, response.text)
except requests.exceptions.RequestException as e:
    print("Error:", e)