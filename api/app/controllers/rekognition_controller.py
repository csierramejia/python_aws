from io import StringIO
import csv
from models import RekognitionModel
from helpers.utils import transformation_fields_associated
from datetime import date
import boto3
from PIL import Image
import cv2
import numpy as np
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
    


    def detect_text(self, fileF, fileA, typeDocument):

        readF = fileF.read()
        readA = fileA.read()

        access_key_id = 'AKIA33GOATY44F4AFNIE'
        secret_access_key = '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'
        client = boto3.client('rekognition', region_name='us-east-1', 
                               aws_access_key_id = access_key_id, 
                               aws_secret_access_key = secret_access_key)
        responseF = client.detect_text(Image={'Bytes': readF})
        responseA = client.detect_text(Image={'Bytes': readA})
        textDetectionsF = responseF['TextDetections']
        textDetectionsA = responseA['TextDetections']

        if typeDocument == 'CC':
            rs = self.detect_cc(typeDocument, textDetectionsF, textDetectionsA)
        elif typeDocument == 'PEP':
            rs = self.detect_cc(typeDocument, textDetectionsF, textDetectionsA)
            # rs = self.detect_pep(typeDocument, textDetections)
        elif typeDocument == 'CE':
            rs = self.detect_cc(typeDocument, textDetectionsF, textDetectionsA)
            # rs = self.detect_ce(typeDocument, textDetections)
        elif typeDocument == 'TI':
            rs = self.detect_cc(typeDocument, textDetectionsF, textDetectionsA)
            # rs = self.detect_ti(typeDocument, textDetections)
        else:
            raise Exception("the type of document is not what was expected")

        return rs

    

    def detect_cc(self, cc, textDetectionsF, textDetectionsA):
        textDetectF = []
        textDetectA = []
        for textF in textDetectionsF:
            textDetectF.append(textF['DetectedText'])
        for textA in textDetectionsA:
            textDetectA.append(textA['DetectedText'])
        palabrasF = ['REPUBLICA DE COLOMBIA','IDENTIFICACION','PERSONAL','NOMBRES','APELLIDOS','NUMERO','FIRMA','CEDULA','DE','CIUDADANIA']
        palabrasA = ['ESTATURA','SEXO','INDICE','DERECHO','LUGAR','EXPEDICION','INDICE DERECHO REGISTRADOR NACIONAL','FECHA','DE LUGAR NACIMIENTO','G.S. RH']
        contF = 0
        for palabraF in palabrasF:
            res = [(indice, string)for indice, string in enumerate(textDetectF) if palabraF in string]
            if len(res) > 0:
                contF = contF + 1
        contA = 0
        for palabraA in palabrasA:
            res = [(indice, string)for indice, string in enumerate(textDetectA) if palabraA in string]
            if len(res) > 0:
                contA = contA + 1
        f = np.array([[contF], [len(palabrasF)]])
        a = np.array([[contA], [len(palabrasA)]])
        s = np.array([[np.mean(f)], [np.mean(a)]])

        rsp = np.mean(s)

        if rsp >= 7.5:
            return 1
        else:
            return 0
        
        return np.mean(s)

        # return contF

    
    # def detect_pep(self, pep, response):
    #     return 1
    

    # def detect_ce(self, ce, response):
    #     return 1
    

    # def detect_ti(self, ti, response):
    #     return 1



   
