import requests
import json
import csv
import pandas as pd
import datetime as dt
import os

#{'access_token': 'ya29.a0ARrdaM8_wZjCTqGXf8rS8PHx53ejhKGWljVkVYAK71hsvU7Lq8bi0LfN4n3ZTmJB4GTpGSF2Hcx4DcpUIcS0M1-ZAbeZUNhnsbcSeND69W2GaJf1JbM1OKnXH6a8PAuKBUAh5IUPA1W_TIK6oOxH9exUhjy4', 'expires_in': 3599, 'refresh_token': '1//0g0X2MjDVJaaVCgYIARAAGBASNgF-L9IrQBf0rNvn7VFFvviDtgSf1cTUlDVv47RPvSYsoQ42wwWFpR-6tgR257Jdo3Fb_hF8VQ', 'scope': 'https://www.googleapis.com/auth/fitness.body_temperature.write https://www.googleapis.com/auth/fitness.sleep.write https://www.googleapis.com/auth/fitness.oxygen_saturation.read https://www.googleapis.com/auth/fitness.nutrition.write https://www.googleapis.com/auth/fitness.body.read https://www.googleapis.com/auth/fitness.oxygen_saturation.write https://www.googleapis.com/auth/fitness.body.write https://www.googleapis.com/auth/fitness.heart_rate.write https://www.googleapis.com/auth/fitness.blood_glucose.read https://www.googleapis.com/auth/fitness.location.read https://www.googleapis.com/auth/fitness.sleep.read https://www.googleapis.com/auth/fitness.blood_glucose.write https://www.googleapis.com/auth/fitness.location.write https://www.googleapis.com/auth/fitness.blood_pressure.read https://www.googleapis.com/auth/fitness.activity.read https://www.googleapis.com/auth/fitness.reproductive_health.read https://www.googleapis.com/auth/fitness.heart_rate.read https://www.googleapis.com/auth/fitness.blood_pressure.write https://www.googleapis.com/auth/fitness.activity.write https://www.googleapis.com/auth/fitness.reproductive_health.write https://www.googleapis.com/auth/fitness.body_temperature.read https://www.googleapis.com/auth/fitness.nutrition.read', 'token_type': 'Bearer'}

#'refresh_token' : "1//0gjW3T1sH4yeZCgYIARAAGBASNwF-L9Irzpp-bZSsXr-IbzBGzb5_39wLTE-gTNUX4oyyn8YDnLbwVOMFX4MASehgEaqYhPrd5Sg",
#Aditya

#'refresh_token': '1//0g0X2MjDVJaaVCgYIARAAGBASNgF-L9IrQBf0rNvn7VFFvviDtgSf1cTUlDVv47RPvSYsoQ42wwWFpR-6tgR257Jdo3Fb_hF8VQ',
#Shuddhank


payload = {
        'refresh_token' : "1//0ghLzy-tmjfoWCgYIARAAGBASNwF-L9IrAI21mwJn3_wtJNO8elATGKY5sMxCfoCXQVdtv0Qqr6dgtfadE14ORryolOjLJecB2f0",
        'client_id' : '491655752747-gcl0gml5htbqhkmjq1lohjmk5k8qfjn1.apps.googleusercontent.com',
        "client_secret" : "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",
        'grant_type' : 'refresh_token',
        }

r_token = requests.post('https://oauth2.googleapis.com/token',data=payload).json()

print(r_token)

gfit_access_token = r_token["access_token"] 

print(gfit_access_token)
for i in range(120, 151):
    start = dt.datetime.combine(dt.date.today(), dt.datetime.min.time()) - dt.timedelta(days=i)
    start_millis = int(start.timestamp() * 1000)

    end = dt.datetime.combine(dt.date.today(), dt.datetime.min.time()) - dt.timedelta(days=i - 1)
    end_millis = int(end.timestamp() * 1000)

    date = str(dt.date.today() - dt.timedelta(days=i))
    print(start_millis)
    print(end_millis)

    # Rest of your code goes here...


for i in range(120,151):

      start = dt.datetime.combine(dt.date.today(), dt.datetime.min.time()) - dt.timedelta(days = i)
      start_millis = int(start.timestamp() * 1000)
    
    end = dt.datetime.combine(dt.date.today(), dt.datetime.min.time()) - dt.timedelta(days = i-1) 
    end_millis = int(end.timestamp() * 1000)

    date = str(dt.date.today() - dt.timedelta(days = i))
    print(start_millis)
    print(end_millis)

    firstname = "Pavan"
    lastname = "Kumar"
    phone = "NA"
    email = "NA"
    
    header = {'Content-type': 'application/json',
            'Authorization': 'Bearer ' + gfit_access_token
            }
    
    
    #DATA FETCH --------------------------------------------------------------------------------------

    
    
    #STEPS -------------------------------------------------------------------------------------------

    

    payload = {
            "aggregateBy": [{
                "dataTypeName": "com.google.step_count.delta",
            }],
            "bucketByTime": { "durationMillis": 86400000},
            "startTimeMillis": start_millis,
            "endTimeMillis":  end_millis
            }

    r_token = requests.post('https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate', headers = header, data=json.dumps(payload)).json()
    
    
    checkval = 0
    
    for item in r_token["bucket"]:
        print(item)
        try:
            checkval = int(item["dataset"][0]["point"][0]["value"][0]["intVal"])
        except:
         None
    
    if checkval != 0:
        payload = {
                "aggregateBy": [{
                    "dataTypeName": "com.google.step_count.delta",
                }],
                "bucketByTime": { "durationMillis": 60000},
                "startTimeMillis": start_millis,
                "endTimeMillis":  end_millis
                }

        r_token = requests.post('https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate', headers = header, data=json.dumps(payload)).json()


        # print(r_token)
        gfit_steps = []
        gfit_dates = []

        for item in r_token["bucket"]:
            gfit_dates.append(str(dt.datetime.fromtimestamp(int(item["startTimeMillis"])/1000.0))[10:])
            if len(item["dataset"][0]["point"]) == 0:
                gfit_steps.append(0)
            else:
                gfit_steps.append(item["dataset"][0]["point"][0]["value"][0]["intVal"])
                
        os.makedirs(os.path.dirname("gfit_data/"+firstname+lastname+"_intraday_steps_"+date+".csv"), exist_ok=True)
        with open("gfit_data/"+firstname+lastname+"_intraday_steps_"+date+".csv", 'w') as csvfile:
            writer = csv.writer(csvfile, lineterminator = '\n')
            writer.writerow(["Firstame", firstname])
            writer.writerow(["Lastame", lastname])
            writer.writerow(["Phone", phone])
            writer.writerow(["Email", email])
            writer.writerow(["Token", gfit_access_token])
            writer.writerow(["Date", date])
            writer.writerow(["Datatype", "Intraday Steps"])
            writer.writerow(["", ""])
            writer.writerow(["Time", "Steps"])
            for i in range(len(gfit_dates)):
                writer.writerow([gfit_dates[i], gfit_steps[i]])
            
    #CALORIES -----------------------------------------------------------------------------------------


    header = {'Content-type': 'application/json',
            'Authorization': 'Bearer ' + gfit_access_token
            }

    payload = {
            "aggregateBy": [{
                "dataTypeName": "com.google.calories.expended",
            }],
            "bucketByTime": { "durationMillis": 86400000},
            "startTimeMillis": start_millis,
            "endTimeMillis":  end_millis
            }

    r_token = requests.post('https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate', headers = header, data=json.dumps(payload)).json()
    
    
    checkval = 0
    
    for item in r_token["bucket"]:
        print(item)
        try:
            checkval = int(item["dataset"][0]["point"][0]["value"][0]["fpVal"])
        except:
         None
    
    if checkval != 0:
        payload = {
                "aggregateBy": [{
                    "dataTypeName": "com.google.calories.expended",
                }],
                "bucketByTime": { "durationMillis": 60000},
                "startTimeMillis": start_millis,
                "endTimeMillis":  end_millis
                }

        r_token = requests.post('https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate', headers = header, data=json.dumps(payload)).json()


        # print(r_token)
        gfit_steps = []
        gfit_dates = []

        for item in r_token["bucket"]:
            gfit_dates.append(str(dt.datetime.fromtimestamp(int(item["startTimeMillis"])/1000.0))[10:])
            if len(item["dataset"][0]["point"]) == 0:
                gfit_steps.append(0)
            else:
                gfit_steps.append(item["dataset"][0]["point"][0]["value"][0]["fpVal"])
                
        os.makedirs(os.path.dirname("gfit_data/"+firstname+lastname+"_intraday_calories_"+date+".csv"), exist_ok=True)
        with open("gfit_data/"+firstname+lastname+"_intraday_calories_"+date+".csv", 'w') as csvfile:
            writer = csv.writer(csvfile, lineterminator = '\n')
            writer.writerow(["Firstame", firstname])
            writer.writerow(["Lastame", lastname])
            writer.writerow(["Phone", phone])
            writer.writerow(["Email", email])
            writer.writerow(["Token", gfit_access_token])
            writer.writerow(["Date", date])
            writer.writerow(["Datatype", "Intraday calories"])
            writer.writerow(["", ""])
            writer.writerow(["Time", "Calories"])
            for i in range(len(gfit_dates)):
                writer.writerow([gfit_dates[i], gfit_steps[i]])

    # #ACTIVE MINUTES ------------------------------------------------------------------------------------------

    # payload = {
            # "aggregateBy": [{
                # "dataTypeName": "com.google.active_minutes",
            # }],
            # "bucketByTime": { "durationMillis": 86400000},
            # "startTimeMillis": start_millis,
            # "endTimeMillis":  end_millis
            # }

    # r_token = requests.post('https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate', headers = header, data=json.dumps(payload)).json()

    # gfit_active_mins = []

    # for item in r_token["bucket"]:
        
        # if len(item["dataset"][0]["point"]) == 0:
            # gfit_active_mins.append(0)
        # else:
            # gfit_active_mins.append(item["dataset"][0]["point"][0]["value"][0]["intVal"])


    # #HEARTRATE --------------------------------------------------------------------------------------------------

    checkval = 0
    
    payload = {
            "aggregateBy": [{
                "dataTypeName": "com.google.heart_rate.bpm",
            }],
            "bucketByTime": { "durationMillis": 86400000},
            "startTimeMillis": start_millis,
            "endTimeMillis":  end_millis
            }

    r_token = requests.post('https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate', headers = header, data=json.dumps(payload)).json()

    for item in r_token["bucket"]:
        print(item)
        try:
            checkval = int(item["dataset"][0]["point"][0]["value"][0]["fpVal"])
        except:
         None
            
    if checkval != 0:        
        payload = {
                "aggregateBy": [{
                    "dataTypeName": "com.google.heart_rate.bpm",
                }],
                "bucketByTime": { "durationMillis": 60000},
                "startTimeMillis": start_millis,
                "endTimeMillis":  end_millis
                }

        r_token = requests.post('https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate', headers = header, data=json.dumps(payload)).json()


        gfit_dates = []
        gfit_hr = []
        for item in r_token["bucket"]:
            gfit_dates.append(str(dt.datetime.fromtimestamp(int(item["startTimeMillis"])/1000.0))[10:])
            if len(item["dataset"][0]["point"]) == 0:
                gfit_hr.append(0)
            else:
                gfit_hr.append(int(item["dataset"][0]["point"][0]["value"][0]["fpVal"]))
                
        # print(gfit_dates)
        # print(gfit_hr)
        
        os.makedirs(os.path.dirname("gfit_data/"+firstname+lastname+"_intraday_heartrate_"+date+".csv"), exist_ok=True)
        with open("gfit_data/"+firstname+lastname+"_intraday_heartrate_"+date+".csv", 'w') as csvfile:
            writer = csv.writer(csvfile, lineterminator = '\n')
            writer.writerow(["Firstame", firstname])
            writer.writerow(["Lastame", lastname])
            writer.writerow(["Phone", phone])
            writer.writerow(["Email", email])
            writer.writerow(["Token", gfit_access_token])
            writer.writerow(["Date", date])
            writer.writerow(["Datatype", "Intraday Heartrate"])
            writer.writerow(["", ""])
            writer.writerow(["Time", "HeartRate"])
            for i in range(len(gfit_dates)):
                if gfit_hr[i] != 0:
                    writer.writerow([gfit_dates[i], gfit_hr[i]])
  