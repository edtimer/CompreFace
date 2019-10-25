import os
from pathlib import Path

import imageio
import pytest

from src.face_recognition.embedding_calculator.calculator import calculate_embedding
from src.face_recognition.embedding_classifier.classifier import get_face_predictions, train
from src.face_recognition.face_cropper.cropper import crop_faces
from src.storage.storage_factory import get_storage

CURRENT_DIR = Path(os.path.dirname(os.path.realpath(__file__)))


def add_image(path, name, api_key):
    im = imageio.imread(path)
    cropped_faces = crop_faces(im)[0].img
    embedding = calculate_embedding(cropped_faces)
    get_storage().add_face(raw_img=im, face_img=cropped_faces, embedding=embedding, face_name=name,
                           api_key=api_key)


@pytest.mark.integration
def test_integration__given_2_faces_in_db__when_asked_to_recognize_known_face__then_recognizes_correct_face():
    api_key = 'api-key'
    add_image(CURRENT_DIR / 'files' / 'personA-img1.jpg', 'Person A', api_key)
    add_image(CURRENT_DIR / 'files' / 'personB-img1.jpg', 'Person B', api_key)
    train(api_key)
    img = imageio.imread(CURRENT_DIR / 'files' / 'personA-img2.jpg')

    face_predictions = get_face_predictions(img=img, limit=1, api_key=api_key)

    assert face_predictions[0].prediction == 'Person A'
