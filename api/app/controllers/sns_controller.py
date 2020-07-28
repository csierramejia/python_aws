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
    # @description: Metodo que se encarga de guardar los codigos enviados al usuario
    def send_code_register(self, phone):
        data = {
            'code' : phone['code'],
            'phone': phone['phone'],
            'valid': False,
            'dateSave': self.get_timestamp()
        }

        if self.sns_model.insert(data):
            return 1
        else:
            raise Exception("Problems savings the code")


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
        
        

        




   
