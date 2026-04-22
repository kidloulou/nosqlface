import face_recognition
import base64
import io
import numpy as np

def get_face_encoding(image_base64):
    try:
        if "," in image_base64:
            image_base64 = image_base64.split(",")[1]

        img_data = base64.b64decode(image_base64)
        img_file = io.BytesIO(img_data)

        image = face_recognition.load_image_file(img_file)

        encodings = face_recognition.face_encodings(image)

        if len(encodings) > 0:
            return encodings[0].tolist()
        return None
    except Exception as e:
        print(f"Erreur encodage: {e}")
        return None

def verify_face(stored_encoding, current_image_base64):
    current_encoding = get_face_encoding(current_image_base64)

    if current_encoding is None:
        return False

    matches = face_recognition.compare_faces(
        [np.array(stored_encoding)],
        np.array(current_encoding),
        tolerance=0.5
    )
    return matches[0]
