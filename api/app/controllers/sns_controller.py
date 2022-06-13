from io import StringIO
import csv
from models import SnsModel
from helpers.utils import transformation_fields_associated
from datetime import datetime, date, timedelta
# import cv2
from random import randint, uniform
import random
import os
import http.client
import json
from pg import DB
from twilio.rest import Client

class SnsController(object):
    def __init__(self):
        self.sns_model = SnsModel()
        # self.db = DB(dbname='DBDLLO', host='jerdevrds01.cwf68ralqtsp.us-east-1.rds.amazonaws.com', port=5432, user='administrator', passwd='123456789')
        self.db = DB(dbname='DBDLLO', host='logiiblue-db-cluster.cluster-czj90e0hs7ck.us-east-1.rds.amazonaws.com', port=5432, user='core_application', passwd='c0r3_4ppl1c4t10n')

    # @authos: Luis Hernandez
    # @description: Metodo que se encarga de guardar y enviar el codigo de validacion
    def send_code_register(self, phone):
        account_sid = 'AC45411c1382f30aa3681f3537e5622191'
        auth_token = 'f00e636a91f70f409a130a00704e0d0a'
        client = Client(account_sid, auth_token)
        # auth_token = '[AuthToken]' 
        code = random.randint(1000, 9999) # random number generator
        mess = 'Tu código de validación para el registro en logii es '+str(code)
        # validate yes insert code in database
        if int(self.db.query("INSERT INTO sms_codigo VALUES ("+str(code)+", "+str(phone['phone'])+", "+str(False)+", "+str(self.get_timestamp())+")")):
            message = client.messages \
                .create(
                    body=mess,
                    from_='+19122078959',
                    to='+'+phone['code']+phone['phone']
                )
            return 1
        else:
            raise Exception("Problems savings the code")


    # @authos: Luis Hernandez
    # @description: Metodo que devuelve la fecha y hora en formato int
    def get_timestamp(self):
        now = datetime.now()
        return int(datetime.timestamp(now))


    # @authos: Luis Hernandez
    # @description: Metodo que se encarga de buscar y validar el codigo
    def valid_code(self, code):
        # return "here testing valid code"
        if len(self.db.query("SELECT codigo, validacion FROM sms_codigo WHERE codigo = '"+str(code)+"' ")) == 1:
            self.db.query("UPDATE sms_codigo SET validacion = '"+str(True)+"' WHERE codigo = '"+str(code)+"'")
            return 1
        else:
            return 0
        
        

        




   
