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

class SnsController(object):
    def __init__(self):
        self.sns_model = SnsModel()

    # @authos: Luis Hernandez
    # @description: Metodo que se encarga de enviar
    # al celular del usuario que esta intentando 
    # registrarse un codigo para poder validar el numero del telefono
    def send_code_register(self, phone):

        url = "https://apitellit.aldeamo.com/SmsiWS/smsSendGet"
        code = random.randint(1000,9999)
        message = 'Tu código de validación para el registro en logii es '+str(code)
        headers = {
            'authorization': "Basic THVpc19IZXJuYW5kZXo6TDRpU0gzck4yMDIwKg==",
            'cache-control': "no-cache",
            'postman-token': "5bc0733b-498c-1ab2-bac6-82fc06ed4221"
            }
        data = {
            'code' : code,
            'phone': phone['phone'],
            'valid': False,
            'dateSave': self.get_timestamp()
        }

        if self.sns_model.insert(data):
            querystring = {"mobile":phone['phone'],"country":phone['country'],"message":message,"messageFormat":"1"}
            response = requests.request("GET", url, headers=headers, params=querystring)

        return response.text

        # print(response.text)
        
        # access_key_id = 'AKIA33GOATY44F4AFNIE'
        # secret_access_key = '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'
        # code = random.randint(1000,9999)
        # numberPhone = phone['phone']

        # data = {
        #     'code' : code,
        #     'phone': numberPhone,
        #     'valid': False,
        #     'dateSave': self.get_timestamp()
        # }

        # if self.sns_model.insert(data):
        #     client = boto3.client('sns', region_name='us-east-1', 
        #                            aws_access_key_id = access_key_id, 
        #                            aws_secret_access_key = secret_access_key)

        #     message = 'Tu código de validación para el registro en logii es '+str(code)
                                
        #     response = client.publish(PhoneNumber=phone['phone'], Message=message)
        #     return response

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
        
        

        




   
