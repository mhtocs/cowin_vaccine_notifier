import datetime
import requests
import time

from beepy import beep


REFRESH_DELAY = 60 #every 1 minute
PINCODE =  ["560063"] 
SOUND = 'coin'  #available sounds ->  coin, robot_error, error, ping, ready, sucess, wilhelm

# Update the above parameters 



MOCK_HEADER = {
        'Accept': 'application/json', 
        'Accept-Language': 'hi_IN', 
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
        }

URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"


def check_availibilty(date):
    try:
        for pin in PINCODE:
            print(f"\nPINCODE: {pin}\n")
           
            payload = {"pincode": pin, "date": date}
            resp = requests.get(URL, params=payload,headers=MOCK_HEADER)       
            resp.raise_for_status()
            resp = resp.json()
            centers = resp['centers']
            if centers:
                max_center_string_len = max([len(center['name']) for center in centers])
            for center in centers:
                center_name = center['name']

                sessions = center['sessions']
                for session in sessions:
                    available = session['available_capacity']
                    vaccine_type = session['vaccine']
                    session_date = session['date']
                    age = session['min_age_limit']
                    slots = session['slots']
                    print(f"{center_name:>{max_center_string_len}} => available:: {available:03}, date:: {session_date}, type:: {vaccine_type}, timing :: {slots}\n")       
                    
                    # beep as many times as many vaccines are available
                    # why? to piss off people
                    for c in range(0,available):
                        beep(sound=SOUND)
            
            print("=======================================\n")
    except requests.exceptions.RequestException as e:
        print(f"Error while checking availibilty {e}")
        raise SystemExit(e)

if __name__ == '__main__':
    while True:
        print("\n\n")
        today = datetime.datetime.now()
        today = today.strftime("%d-%m-%Y")

        check_availibilty(date=today)
        local_delay=REFRESH_DELAY
        
        print('')
        while local_delay > 0:
            print("", end=f"\rTrying again in {local_delay} seconds")
            time.sleep(1)
            local_delay-=1
        
