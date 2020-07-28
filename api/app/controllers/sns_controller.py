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

class SnsController(object):
    def __init__(self):
        self.sns_model = SnsModel()

    # @authos: Luis Hernandez
    # @description: Metodo que se encarga de guardar los codigos enviados al usuario
    def send_code_register(self, phone):


        url = "https://apitellit.aldeamo.com/SmsiWS/smsSendPost/"

        payload = "{\n\t\"country\": \"57\",\n\t\"message\": \"hey\",\n\t\"encoding\": \"GSM7\",\n\t\"messageFormat\": 1,\n\t\"addresseeList\": [\n\t\t{\n\t\t\"mobile\": \"3024135330\",\n\t\t\"correlationLabel\": \"test\"\n\t\t}\n\t]\n}"
        headers = {
            'authorization': "Basic THVpc19IZXJuYW5kZXo6TDRpU0gzck4yMDIwKg==",
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "28b856c7-4219-a084-4e5a-8c9899f13170"
            }

        return requests.request("POST", url, data=payload, headers=headers)

        # conn = http.client.HTTPSConnection("apitellit.aldeamo.com")
        # code = random.randint(1000, 9999)
        # message = 'Tu código de validación para el registro en logii es '+str(code)
        # payload = "{  \n \"country\": \""+phone['code']+"\",\n \"message\": \""+message+"\",\n \"encoding\": \"GSM7\",\n \"messageFormat\": 1,\n \"addresseeList\": [\n    {\n      \"mobile\": \""+phone['phone']+"\",\n      \"correlationLabel\": \"test\"\n    }\n ]\n}"

        # headers = {
        #     'authorization': "Basic THVpc19IZXJuYW5kZXo6TDRpU0gzck4yMDIwKg==",
        #     'content-type': "application/json",
        #     'cache-control': "no-cache",
        #     'postman-token': "08037200-7d41-ddb0-33ec-ca1a727ef5a7"
        # }

        # conn.request("POST", "/SmsiWS/smsSendPost", payload, headers)
        # res = conn.getresponse()
        # data = res.read()
        # return data

        # data = {
        #     'code' : phone['code'],
        #     'phone': phone['phone'],
        #     'valid': False,
        #     'dateSave': self.get_timestamp()
        # }

        # if self.sns_model.insert(data):
        #     conn.request("POST", "/SmsiWS/smsSendPost", payload, headers)
        #     res = conn.getresponse()
        #     data = res.read()
        #     return data
        # else:
        #     raise Exception("Problems savings the code")


    # @authos: Luis Hernandez
    # @description: Metodo que devuelve la fecha y hora en formato int
    def get_timestamp(self):
        now = datetime.now()
        return int(datetime.timestamp(now))

    
    # @authos: Luis Hernandez
    # @description: Metodo que devuelve la fecha y hora en formato int
    def valid_code(self, code):
        
        query = [
            {"$match": {"code": int(code), "valid": False}},
        ]
        data = self.sns_model.get_account(query)
        if data:
            self.sns_model.update({"_id": ObjectId(data[0].get('_id'))}, {"valid":True})
            return 1
        else:
            return 0
        
        

        




   
