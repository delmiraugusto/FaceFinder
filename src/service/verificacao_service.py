from deepface import DeepFace
import cv2
import numpy as np
import base64
import pytesseract
import re
from sqlalchemy.orm import Session

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

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

def extract_document_data(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3,3), 0)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    text = pytesseract.image_to_string(gray, lang="por")

    dob_pattern = r"(\d{2}[/-]\d{2}[/-]\d{4})"
    dob_match = re.search(dob_pattern, text)
    nascimento = dob_match.group(1) if dob_match else None

    lines = [line.strip() for line in text.split("\n") if line.strip()]
    invalid_keywords = ["FILAÇÃO", "NOME DO PAI", "NOME DA MÃE", "ESTADO", "GOVERNO", "IDENTIFICAÇÃO"]

    name_candidates = []
    for i, line in enumerate(lines):
        upper_line = line.upper()
        if any(keyword in upper_line for keyword in ["NOME", "NAME"]):
            next_lines = lines[i+1:i+3] if i+1 < len(lines) else []
            for nl in next_lines:
                nl_clean = re.sub(r"^[^A-Za-z]+|[^A-Za-z]+$", "", nl).strip()
                if nl_clean and len(nl_clean.split()) >= 2 and not any(k in nl_clean.upper() for k in invalid_keywords):
                    name_candidates.append(nl_clean)

    if not name_candidates:
        cleaned_lines = [re.sub(r"^[^A-Za-z]+|[^A-Za-z]+$", "", line) for line in lines]
        valid_lines = [line for line in cleaned_lines if len(line.split()) >= 2 and not any(k in line.upper() for k in invalid_keywords)]
        uppercase_names = [line for line in valid_lines if all(word.isupper() for word in line.split())]
        name_candidates = uppercase_names if uppercase_names else valid_lines

    name = name_candidates[0] if len(name_candidates) > 0 else None

    return {
        "nome": name,
        "data_nascimento": nascimento
    }

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

    document_data = extract_document_data(imgDocument)
    
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