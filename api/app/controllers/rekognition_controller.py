from io import StringIO
import csv
from models import RekognitionModel
from helpers.utils import transformation_fields_associated
from datetime import date
import boto3
from PIL import Image
import cv2

import os

class RekognitionController(object):
    def __init__(self):
        self.rekognition_model = RekognitionModel()

    def detect_faces(self, foto):

        read = foto.read()
        access_key_id = 'AKIA33GOATY44F4AFNIE'
        secret_access_key = '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'
        client = boto3.client('rekognition', region_name='us-east-1', 
                               aws_access_key_id = access_key_id, 
                               aws_secret_access_key = secret_access_key)
                               
        # response = client.detect_labels(Image={'Bytes': read}, MaxLabels=10)
        response = client.detect_faces(Image={'Bytes': read},Attributes=['ALL'])
        return response
    


    def detect_text(self, foto):

        read = foto.read()
        access_key_id = 'AKIA33GOATY44F4AFNIE'
        secret_access_key = '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'
        client = boto3.client('rekognition', region_name='us-east-1', 
                               aws_access_key_id = access_key_id, 
                               aws_secret_access_key = secret_access_key)
                               
        response = client.detect_text(Image={'Bytes': read})
        return response



   
