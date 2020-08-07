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
import psycopg2
from sshtunnel import SSHTunnelForwarder

class SnsController(object):
    def __init__(self):
        self.sns_model = SnsModel()
        # self.db = DB(dbname='DBDLLO', host='jerdevrds01.cwf68ralqtsp.us-east-1.rds.amazonaws.com', port=5432, user='administrator', passwd='123456789')
        self.db = DB(dbname='DBDLLO', host='instancedbdllo.cbg8artgeyju.us-east-2.rds.amazonaws.com', port=5432, user='core_application', passwd='c0r3_4ppl1c4t10n')

    # @authos: Luis Hernandez
    # @description: Metodo que se encarga de guardar y enviar el codigo de validacion
    def send_code_register(self, phone):
        conn = http.client.HTTPSConnection("api.messaging-service.com")
        code = random.randint(1000, 9999)
        message = 'Tu código de validación para el registro en logii es '+str(code)
        payload = {
            "from":"logii",
            "to": phone['code']+phone['phone'],
            "text": message
        }
        payloadStr =  json.dumps(payload)
        headers = {
            'authorization': "Basic a29uZXhpbm5vdmF0aW9uOktvbmV4X3NtczIwMjAu",
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "28b856c7-4219-a084-4e5a-8c9899f13170"
        }
        if int(self.db.query("INSERT INTO sms_codigo VALUES ("+str(code)+", "+str(phone['phone'])+", "+str(False)+", "+str(self.get_timestamp())+")")):
            conn.request("POST", "/sms/1/text/single", payloadStr, headers)
            res = conn.getresponse()
            data = res.read()
            return {
                    "status": 200,
                    "message": "codigo entregado"
            }
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
        if len(self.db.query("SELECT codigo, validacion FROM sms_codigo WHERE codigo = '"+str(code)+"' AND validacion = "+str(False)+" ")) == 1:
            return int(self.db.query("UPDATE sms_codigo SET validacion = '"+str(True)+"' WHERE codigo = '"+str(code)+"'"))
        else:
            return 0
        
        

        




   
