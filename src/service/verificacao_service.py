from deepface import DeepFace
import cv2
import numpy as np
import base64

def base64_to_cv2_image(base64_str):
    img_data = base64.b64decode(base64_str)
    np_arr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img

def verify_faces(document_base64, selfie_base64):
    imgDocument = base64_to_cv2_image(document_base64)
    imgSelfie = base64_to_cv2_image(selfie_base64)

    try:
        obj = DeepFace.verify(
            img1_path=imgDocument,
            img2_path=imgSelfie,
            detector_backend="opencv",
            align=True
        )
    except ValueError as ve:
        raise ValueError("Nenhum rosto detectado em uma ou ambas as imagens.") from ve

    return {
        "verified": obj["verified"],
        "distance": obj["distance"],
        "similarity_percent": round((1 - obj["distance"]) * 100, 2),
    }