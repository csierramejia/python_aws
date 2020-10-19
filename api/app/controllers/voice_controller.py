from io import StringIO
import csv
from models import SnsModel
from helpers.utils import transformation_fields_associated
from datetime import datetime, date, timedelta
import boto3
from PIL import Image
from random import randint, uniform
from random import randint
import random
from bson.objectid import ObjectId
import requests
import os
import http.client
import json
from pg import DB
import psycopg2
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Say

class VoiceController(object):
    def __init__(self):
        self.sns_model = SnsModel()
        # self.db = DB(dbname='DBDLLO', host='jerdevrds01.cwf68ralqtsp.us-east-1.rds.amazonaws.com', port=5432, user='administrator', passwd='123456789')
        self.db = DB(dbname='DBDLLO', host='jerdevrds01.cwf68ralqtsp.us-east-1.rds.amazonaws.com', port=5432, user='core_application', passwd='c0r3_4ppl1c4t10n')

    # @authos: Luis Hernandez
    # @description: Metodo que se encarga de guardar y enviar el codigo de validacion via telefonicamente
    def send_code_register(self, phone):
        account_sid = 'AC587ffa7d668e9bf3e37a554eb47015e3'
        auth_token = 'f974b33308d809f9d72077f31490fb61'
        client = Client(account_sid, auth_token)
        code = random.randint(1000, 9999)
        message = 'Tu código de validación para el registro en logii es '+str(code)

        if int(self.db.query("INSERT INTO sms_codigo VALUES ("+str(code)+", "+str(phone['phone'])+", "+str(False)+", "+str(self.get_timestamp())+")")):
            call = client.calls.create(
                                twiml='<Response><Say voice="woman" language="es">'+message+'</Say></Response>',
                                to='+'+phone['code']+phone['phone'],
                                from_='+12016544164'
                            )
            return 1
        else:
            raise Exception("Problems savings the code")

    
    # @authos: Luis Hernandez
    # @description: Metodo que devuelve la fecha y hora en formato int
    def get_timestamp(self):
        now = datetime.now()
        return int(datetime.timestamp(now))


        
        

        




   
