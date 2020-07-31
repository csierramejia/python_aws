from io import StringIO
import csv
from models import SnsModel
from helpers.utils import transformation_fields_associated
from datetime import datetime, date, timedelta
import boto3
from PIL import Image
import cv2
from random import randint, uniform
from random import randint
import random
from bson.objectid import ObjectId
import requests
import os
import http.client
import json
from pg import DB

class SnsController(object):
    def __init__(self):
        self.sns_model = SnsModel()
        self.db = DB(dbname='DBDLLO', host='jerdevrds01.cwf68ralqtsp.us-east-1.rds.amazonaws.com', port=5432, user='administrator', passwd='123456789')

    # @authos: Luis Hernandez
    # @description: Metodo que se encarga de guardar los codigos enviados al usuario
    def send_code_register(self, phone):
        conn = http.client.HTTPSConnection("apitellit.aldeamo.com")
        code = random.randint(1000, 9999)
        message = 'Tu código de validación para el registro en logii es '+str(code)
        payload = {
            "country": phone['code'],
            "message": message,
            "encoding": "GSM7",
            "messageFormat": 1,
            "addresseeList": [
                {
                "mobile": phone['phone'],
                "correlationLabel": "test",
                }
            ]
        }
        payloadStr =  json.dumps(payload)
        headers = {
            'authorization': "Basic THVpc19IZXJuYW5kZXo6TDRpU0gzck4yMDIwKg==",
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "28b856c7-4219-a084-4e5a-8c9899f13170"
        }
        if int(self.db.query("INSERT INTO sms_codigo VALUES ("+str(code)+", "+str(phone['phone'])+", "+str(False)+", "+str(self.get_timestamp())+")")):
            conn.request("POST", "/SmsiWS/smsSendPost", payloadStr, headers)
            res = conn.getresponse()
            data = res.read()
            return data
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
        if len(self.db.query("SELECT codigo, validacion FROM sms_codigo WHERE codigo = '"+str(code)+"' AND validacion = "+str(False)+" ")) == 1:
            return int(self.db.query("UPDATE sms_codigo SET validacion = '"+str(True)+"' WHERE codigo = '"+str(code)+"'"))
        else:
            return 0
        
        

        




   
