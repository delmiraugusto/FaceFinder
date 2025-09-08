from deepface import DeepFace
import cv2
import numpy as np
import base64

def base64_to_cv2_image(base64_str):
    img_data = base64.b64decode(base64_str)
    np_arr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img

def validate_image_quality(img, name, min_size=100, blur_threshold=100.0, min_brightness=50, max_brightness=200):
    
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
        obj = DeepFace.verify(
            img1_path=imgDocument,
            img2_path=imgSelfie,
            detector_backend="opencv",
            align=True
        )
    except ValueError:
        raise ValueError("Nenhum rosto detectado em uma ou em ambas as imagens.") 

    return obj

def verify_faces(document_base64, selfie_base64):
    imgDocument = base64_to_cv2_image(document_base64)
    imgSelfie = base64_to_cv2_image(selfie_base64)

    validate_image_quality(imgDocument, name="Documento")
    validate_image_quality(imgSelfie, name="Selfie")

    obj = verify_Presente_face(imgDocument, imgSelfie)

    return {
        "verified": obj["verified"],
        "distance": obj["distance"],
        "similarity_percent": round((1 - obj["distance"]) * 100, 2),
    }