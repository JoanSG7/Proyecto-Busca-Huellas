import base64
from io import BytesIO
import os
import uuid

from flask import current_app, url_for
from PIL import Image, UnidentifiedImageError


ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
MAX_IMAGE_BYTES = 10 * 1024 * 1024
MAX_IMAGE_PIXELS = 24_000_000
IMAGE_FORMAT_EXTENSIONS = {"PNG": "png", "JPEG": "jpg", "GIF": "gif", "WEBP": "webp"}


def _upload_folder(subfolder):
    folder = os.path.join(current_app.root_path, "static", "uploads", subfolder)
    os.makedirs(folder, exist_ok=True)
    return folder


def _static_path_for(filename, subfolder):
    return url_for("static", filename=f"uploads/{subfolder}/{filename}")


def _extension_imagen_valida(image_bytes):
    """Comprueba que los bytes sean una imagen segura y devuelve su extensión real."""
    if not image_bytes or len(image_bytes) > MAX_IMAGE_BYTES:
        return None

    try:
        with Image.open(BytesIO(image_bytes)) as image:
            image.verify()
        with Image.open(BytesIO(image_bytes)) as image:
            if image.width * image.height > MAX_IMAGE_PIXELS:
                return None
            image.load()
            return IMAGE_FORMAT_EXTENSIONS.get(image.format)
    except (Image.DecompressionBombError, OSError, UnidentifiedImageError, ValueError):
        return None


def guardar_imagen(file_storage, subfolder):
    if not file_storage or not file_storage.filename:
        return None

    image_bytes = file_storage.read(MAX_IMAGE_BYTES + 1)
    extension = _extension_imagen_valida(image_bytes)
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        return None

    unique_name = f"{uuid.uuid4().hex}.{extension}"
    with open(os.path.join(_upload_folder(subfolder), unique_name), "wb") as image_file:
        image_file.write(image_bytes)
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
        image_bytes = base64.b64decode(encoded, validate=True)
    except ValueError:
        return None

    if _extension_imagen_valida(image_bytes) != extension:
        return None

    unique_name = f"{uuid.uuid4().hex}.{extension}"
    with open(os.path.join(_upload_folder(subfolder), unique_name), "wb") as image_file:
        image_file.write(image_bytes)
    return _static_path_for(unique_name, subfolder)
