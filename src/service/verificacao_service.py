from deepface import DeepFace
import cv2
import numpy as np
import base64
import pytesseract
from openai import OpenAI
import os
import re
from sqlalchemy.orm import Session
import json
from google import genai

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def base64_to_cv2_image(base64_str):
    img_data = base64.b64decode(base64_str)
    np_arr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img

def validate_image_quality(img, name, min_size=100, blur_threshold=100.0, min_brightness=30, max_brightness=300):
    
    if img.shape[0] < min_size or img.shape[1] < min_size:
        raise ValueError(f"A imagem: {name}, é muito pequena para análise.")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    if variance < blur_threshold:
        raise ValueError(f"A imagem: {name}, está borrada, envie uma foto mais nítida.")

    mean_brightness = np.mean(gray)
    if mean_brightness < min_brightness or mean_brightness > max_brightness:
        raise ValueError(f"A imagem: {name}, está muito escura ou muito clara.")

    return True

def verify_Presente_face(imgDocument, imgSelfie):
    try:
        result = DeepFace.verify(
            img1_path=imgDocument,
            img2_path=imgSelfie, 
            model_name="ArcFace", 
            distance_metric="euclidean_l2")
    except ValueError:
        raise ValueError("Nenhum rosto detectado em uma ou em ambas as imagens.") 

    return result

def ocr_image(img, langs="por+eng"):
    text = pytesseract.image_to_string(img, lang=langs)
    return text

def extract_with_ai(text, wishlist):
    prompt = f"""
        Você é um assistente de extração de dados.  
        Extraia os seguintes campos do texto abaixo e retorne em JSON.  
        Campos: {wishlist}, no campo pais_de_origem_do_documento, tente estivar o país onde foi emitido o documento.

        O retorno deve ser um json, estritamente desta forma:

        {{
            "campo1": "valor",
            "campo2": "valor",
            ...
        }}

        sem \\n, espaços extras ou qualquer outra coisa.

        Texto do documento:
        {text}

        Se algum campo não existir, retorne null para ele.

        """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    output_text = response.candidates[0].content.parts[0].text.strip()

    try:
        return json.loads(output_text)
    except json.JSONDecodeError:
        return output_text


def crop_face(img, face_coords):
    x, y, w, h = face_coords['x'], face_coords['y'], face_coords['w'], face_coords['h']
    face_img = img[y:y+h, x:x+w]
    return face_img

def cv2_to_base64(img):
    _, buffer = cv2.imencode('.jpg', img)
    return base64.b64encode(buffer).decode('utf-8')
    
def verify_faces(document_base64, selfie_base64):
    imgDocument = base64_to_cv2_image(document_base64)
    imgSelfie = base64_to_cv2_image(selfie_base64)

    validate_image_quality(imgDocument, name="Documento")
    validate_image_quality(imgSelfie, name="Selfie")

    wishlist = ["nome", "data_nascimento", "naturalidade", "pais_de_origem_do_documento", "lingua_nativa_do_documento"]

    document_data = ocr_image(imgDocument)

    document_data = extract_with_ai(document_data, wishlist)

    result = verify_Presente_face(imgDocument, imgSelfie)

    face_document_img = crop_face(imgDocument, result['facial_areas']['img1'])
    face_selfie_img = crop_face(imgSelfie, result['facial_areas']['img2'])

    result2 = verify_Presente_face(face_document_img, face_selfie_img)

    face_document_base64 = cv2_to_base64(face_document_img)
    face_selfie_base64 = cv2_to_base64(face_selfie_img)

    return {
        "verification": result2,
        "document_data": document_data,
        "faces": {
            "document_face": face_document_base64,
            "selfie_face": face_selfie_base64
        }
    }