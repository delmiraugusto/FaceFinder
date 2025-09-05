from flask import Flask, request, jsonify
from flask_restful import Resource
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
from deepface import DeepFace
import cv2
import numpy as np
import base64

class Verificacao(Resource):

    def base64_to_cv2_image(base64_str):
        img_data = base64.b64decode(base64_str)
        np_arr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        return img
    
    def crop_face(img, face_area):
        x, y, w, h = face_area['x'], face_area['y'], face_area['w'], face_area['h']

        return img[y:y+h, x:x+w]

    def post(self):
        try:
            data = request.json
            
            imgDocument = Verificacao.base64_to_cv2_image(data['document'])
            imgSelfie = Verificacao.base64_to_cv2_image(data['selfie'])

            detector = "opencv"
            align = True

            try:
                obj = DeepFace.verify(
                    img1_path=imgDocument,
                    img2_path=imgSelfie,
                    detector_backend=detector,
                    align=align
                )
            except ValueError as ve:
                return {
                    "error": "Nenhum rosto detectado em uma ou ambas as imagens.",
                    "details": str(ve)
                }, 400


            # face_doc = obj['facial_areas']['img1']
            # face_selfie = obj['facial_areas']['img2']

            # cropped_doc = Verificacao.crop_face(imgDocument, face_doc)
            # cropped_selfie = Verificacao.crop_face(imgSelfie, face_selfie)

            return {
                "verified": obj["verified"],
                "distance": obj["distance"],
                "similarity_percent": round((1 - obj["distance"]) * 100, 2),
            }, 200
        
        except Exception as e:
            return {"error": str(e)}, 400