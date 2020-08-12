from io import StringIO
import csv
from models import RekognitionModel
from helpers.utils import transformation_fields_associated
from datetime import date
import boto3
from PIL import Image
import numpy as np
import os
import base64
import io
import re



class RekognitionController(object):
    def __init__(self):
        self.rekognition_model = RekognitionModel()

    def detect_faces(self, json):
        # read = foto.read()
        read = base64.b64decode(str(json['photo'])) 
        access_key_id = 'AKIA33GOATY44F4AFNIE'
        secret_access_key = '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'
        client = boto3.client('rekognition', region_name='us-east-1', 
                               aws_access_key_id = access_key_id, 
                               aws_secret_access_key = secret_access_key)

        response = client.detect_faces(Image={'Bytes': read},Attributes=['ALL'])
        if response['FaceDetails']:
            return response['FaceDetails']
        else:
            return 0

    
    def detect_text(self, json):
        fileF = base64.b64decode(str(json['frente'])) 
        fileA = base64.b64decode(str(json['reverso'])) 
        typeDocument = json['typeDocument']
        textDetectionsF = self.read_text_image(fileF)
        textDetectionsA = self.read_text_image(fileA)
        rs = self.detect_cc(typeDocument, textDetectionsF, textDetectionsA)
        information_extracted = []
        if rs == 1:
            data = self.clean_text(textDetectionsF)
            for row in data:
                information_extracted.append(row['DetectedText'])
            return self.clean_advance_text(information_extracted)
        else:
            return rs


    def clean_text(self, textDetectionsF):
        lines = []
        linesClean = []
        linesCleanText = []
        for row in textDetectionsF:
            if row.get("Type") == "LINE":
                lines.append(row)
        for row in lines:
            if row.get("DetectedText").isupper():
                linesClean.append(row)
        return linesClean
    

    def clean_advance_text(self, information_extracted):
        dictionary = self.data_dictionary_info()
        clean_info = []
        for row in information_extracted:
            exist = 0
            for row_dictionary in dictionary:
                if row.find(row_dictionary) != -1: 
                    exist = 1
            if exist == 0:
                clean_info.append(row)

        search_finish = self.search_number_document(clean_info)
        clean_info.append(search_finish)
        clean_info = self.clean_advance_text_number(clean_info)
        return clean_info
    



    def clean_advance_text_number(self, search_finish):
        dictionary = self.data_dictionary_info_two()
        clean_info = []
        for row in search_finish:
            exist = 0
            for row_dictionary in dictionary:
                if row.find(row_dictionary) != -1: 
                    exist = 1
            if exist == 0:
                clean_info.append(row)
        return clean_info



    def search_number_document(self, info):
        result = []
        for row in info:
            rs = re.findall(r'\d+', row)
            if len(rs) > 0:
                result = rs
                break
        d = ''
        if len(result) > 1:
            for w in result:
                d = d + w
            return d
        else:
            return result[0]


    def data_dictionary_info(self):
        data_dictionary = [
            'REPUBLICA', 
            'republica', 
            'COLOMBIA', 
            'colombia', 
            'IDENTIFICACION', 
            'identificacion', 
            'PERSONAL', 
            'personal',
            'CEDULA',
            'cedula',
            'CIUDADANIA',
            'ciudadania',
            'APELLIDOS',
            'apellidos',
            'NOMBRES',
            'nombres'
        ]
        return data_dictionary
    


    def data_dictionary_info_two(self):
        data_dictionary = [
            'NUMERO', 
            'numero'
        ]
        return data_dictionary



    def read_text_image(self, image):
        access_key_id = 'AKIA33GOATY44F4AFNIE'
        secret_access_key = '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'
        client = boto3.client('rekognition', region_name='us-east-1', 
                               aws_access_key_id = access_key_id, 
                               aws_secret_access_key = secret_access_key)
        response = client.detect_text(Image={'Bytes': image})
        return response['TextDetections']


    def detect_cc(self, typeDocument, textDetectionsF, textDetectionsA):
        textDetectF = self.get_text_array(textDetectionsF)
        textDetectA = self.get_text_array(textDetectionsA)
        palabrasFunction = self.get_arrays_f_a(typeDocument)
        palabrasF = palabrasFunction['F']
        palabrasA = palabrasFunction['A']
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

        if rsp >= 8:
            return 1
        else:
            return 0


    
    def get_text_array(self, textDetections):
        textDetectI = []
        for textF in textDetections:
            textDetectI.append(textF['DetectedText'])
        return textDetectI

    
    def get_arrays_f_a(self, typeDocument):
        if typeDocument == 'CC':
            return {
                'F': ['REPUBLICA DE COLOMBIA','IDENTIFICACION','PERSONAL','NOMBRES','APELLIDOS','NUMERO','FIRMA','CEDULA','DE','CIUDADANIA'],
                'A': ['ESTATURA','SEXO','INDICE','DERECHO','LUGAR','EXPEDICION','INDICE DERECHO REGISTRADOR NACIONAL','FECHA','DE LUGAR NACIMIENTO','G.S. RH']
            }
        elif typeDocument == 'PEP':
            return {
                'F': ['REPUBLICA','Migracion','Permiso','Especial','de','Permanencia','(PEP)','Cedula','Identidad','de'],
                'A': ['REPUBLICA DE COLOMBIA','PASAPORTE','REPUBLICA','COL','P','PASSPORT']
            }
        elif typeDocument == 'CE':
            return {
                'F': ['REPUBLICA DE COLOMBIA','FIRMA','REPUBLICA','CEDULA','DE','EXTRANJERIA','APELLIDOS:','NOMBRES:','NACIONALIDAD:','FIRMA'],
                'A': ['','','','','','','','','','']
            }
        elif typeDocument == 'TI':
            return {
                'F': ['REPUBLICA DE COLOMBIA','IDENTIFICACION PERSONAL','TARJETA DE IDENTIDAD','NOMBRES','APELLIDOS','TARJETA','FIRMA','CEDULA','DE','IDENTIDAD'],
                'A': ['LUGAR DE NACIMIENTO','FECHA','DE','NACIMIENTO','DD-MM-YYYY','CIUDAD','LUGAR','SEXO','VENCIMIENTO','EXPEDICION']
            }
        else:
            raise Exception("the type of document is not what was expected")

      



   
