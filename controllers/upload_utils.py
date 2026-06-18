import base64
import os
import uuid

from flask import url_for
from werkzeug.utils import secure_filename


ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def _upload_folder(subfolder):
    folder = os.path.join("static", "uploads", subfolder)
    os.makedirs(folder, exist_ok=True)
    return folder


def _static_path_for(filename, subfolder):
    return url_for("static", filename=f"uploads/{subfolder}/{filename}")


def guardar_imagen(file_storage, subfolder):
    if not file_storage or not file_storage.filename:
        return None

    filename = secure_filename(file_storage.filename)
    extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        return None

    unique_name = f"{uuid.uuid4().hex}.{extension}"
    file_storage.save(os.path.join(_upload_folder(subfolder), unique_name))
    return _static_path_for(unique_name, subfolder)


def guardar_imagen_base64(data_url, subfolder):
    if not data_url or "," not in data_url:
        return None

    header, encoded = data_url.split(",", 1)
    mime_type = header.split(";")[0].replace("data:", "")
    extension = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/webp": "webp",
    }.get(mime_type)

    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        return None

    try:
        image_bytes = base64.b64decode(encoded)
    except ValueError:
        return None

    unique_name = f"{uuid.uuid4().hex}.{extension}"
    with open(os.path.join(_upload_folder(subfolder), unique_name), "wb") as image_file:
        image_file.write(image_bytes)
    return _static_path_for(unique_name, subfolder)
