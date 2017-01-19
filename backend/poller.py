#!/usr/bin/python

# poller.py -- a python interface for polling Nest Thermostat data
# into a database.
# by Guillaume Chenuet, guillaume@chenuet.fr, http://yauuu.me/
#
# Usage:
#    'poller.py' will fill a new row in the database
#
# Licensing:
#    This is distributed unider the Creative Commons 3.0 Non-commecrial,
#    Attribution, Share-Alike license. You can use the code for noncommercial
#    purposes. You may NOT sell it. If you do use it, then you must make an
#    attribution to me (i.e. Include my name and thank me for the hours I spent
#    on this)

import pyowm
import datetime
from nest import Nest
import mysql.connector

# Override variables with your informations
OWM = ""
OWM_CITY = ""

NEST_ID = ""
NEST_PWD = ""
NEST_SN = ""

DB_USER = ""
DB_PWD = ""
DB_HOST = ""
DB_NAME = ""


def polling(n, w, d):
    nstat = n.show_status()
    query = "INSERT INTO status(date, city_curr_temp, city_curr_hum, cur_weather_icon, \
    		 cur_weather_code, cur_weather_status_detail, cur_weather_status, \
    		 cur_pressure, cur_windspeed,	\
             nest_curr_temp,nest_targ_temp,nest_curr_hum,nest_targ_hum, \
             nest_heat_state, current_schedule_mode, leaf,auto_away, \
             time_to_target, away_temperature_low) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
args = (datetime.datetime.now(),
            w.get_temperature('celsius')['temp'],
            w.get_humidity(),
            w.get_weather_icon_name(),
            w.get_weather_code(),
            w.get_detailed_status(),
            w.get_status(),
            w.get_pressure()['press'],
            w.get_wind()['speed'],            
            nstat['current_temperature'],
            nstat['target_temperature'],
            nstat['current_humidity'],
            nstat['target_humidity'],
            int(nstat['hvac_heater_state']),
            nstat['current_schedule_mode'],
            int(nstat['leaf']),
            int(nstat['auto_away']),
            nstat['time_to_target'],
            nstat['away_temperature_low']);
    d.execute(query, args)

def main():
    #Setup Nest account
    n = Nest(NEST_ID, NEST_PWD, NEST_SN, 0, "C")
    n.login()
    n.get_status()
    # Setup OpenWeatherMap account
    owm = pyowm.OWM(OWM)
    observation = owm.weather_at_place(OWM_CITY)
    w = observation.get_weather()
    # Connect to DB
    cnx = mysql.connector.connect(user=DB_USER, password=DB_PWD,
                                  host=DB_HOST, database=DB_NAME)
    d = cnx.cursor()
    polling(n, w, d)
    cnx.commit()
    d.close()

if __name__ == "__main__":
    main()
