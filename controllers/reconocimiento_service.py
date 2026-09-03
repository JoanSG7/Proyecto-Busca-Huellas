import os
from functools import lru_cache
from urllib.parse import urlparse

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import numpy as np
from flask import current_app
from PIL import Image, ImageOps
from sklearn.metrics.pairwise import cosine_similarity


FORMATOS_VALIDOS = (".jpg", ".jpeg", ".png", ".webp")


@lru_cache(maxsize=1)
def _modelo_reconocimiento():
    from tensorflow.keras.applications.vgg16 import VGG16

    return VGG16(weights="imagenet", include_top=False, pooling="max")


def _embedding_vgg16(ruta_imagen):
    from tensorflow.keras.applications.vgg16 import preprocess_input
    from tensorflow.keras.preprocessing import image

    img = image.load_img(ruta_imagen, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return _modelo_reconocimiento().predict(x, verbose=0)


def _embedding_histograma(ruta_imagen):
    with Image.open(ruta_imagen) as img:
        img = ImageOps.exif_transpose(img).convert("RGB").resize((128, 128))
        histogramas = []
        for canal in img.split():
            histograma, _ = np.histogram(np.asarray(canal), bins=32, range=(0, 256), density=True)
            histogramas.extend(histograma)
        return np.asarray([histogramas], dtype=np.float32)


def ruta_local_desde_url(url_imagen):
    if not url_imagen:
        return None

    parsed = urlparse(url_imagen)
    if parsed.scheme and parsed.scheme not in {"", "file"}:
        return None

    ruta = parsed.path or url_imagen
    ruta = ruta.lstrip("/")
    if not ruta.startswith("static/"):
        return None

    ruta_local = os.path.join(current_app.root_path, ruta.replace("/", os.sep))
    if not os.path.isfile(ruta_local):
        return None

    if not ruta_local.lower().endswith(FORMATOS_VALIDOS):
        return None

    return ruta_local


def obtener_embeddings(ruta_imagen):
    try:
        return _embedding_vgg16(ruta_imagen)
    except Exception:
        return _embedding_histograma(ruta_imagen)


def calcular_porcentaje_real(vec1, vec2):
    similitud_base = cosine_similarity(vec1, vec2)[0][0]
    if similitud_base < 0.5:
        return 0.0
    return float(((similitud_base - 0.5) / 0.5) * 100)


def evaluar_conclusion(porcentaje):
    if porcentaje > 70.0:
        return "Coincidencia alta"
    if porcentaje > 40.0:
        return "Raza o especie similar"
    if porcentaje > 30.0:
        return "Parecido moderado"
    return "Coincidencia baja"


def buscar_mascotas_similares(ruta_foto_usuario, mascotas_con_fotos, limite=10):
    try:
        vec_usuario = _embedding_vgg16(ruta_foto_usuario)
        generar_embedding = _embedding_vgg16
    except Exception:
        vec_usuario = _embedding_histograma(ruta_foto_usuario)
        generar_embedding = _embedding_histograma

    mejores_por_mascota = {}

    for mascota in mascotas_con_fotos:
        ruta_foto_mascota = ruta_local_desde_url(mascota.get("url_imagen"))
        if not ruta_foto_mascota:
            continue

        try:
            vec_mascota = generar_embedding(ruta_foto_mascota)
            porcentaje = calcular_porcentaje_real(vec_usuario, vec_mascota)
        except Exception:
            continue
        id_mascota = mascota["id_mascota"]
        resultado_actual = mejores_por_mascota.get(id_mascota)

        if not resultado_actual or porcentaje > resultado_actual["porcentaje"]:
            mejores_por_mascota[id_mascota] = {
                **mascota,
                "porcentaje": porcentaje,
                "conclusion": evaluar_conclusion(porcentaje),
            }

    resultados = sorted(
        mejores_por_mascota.values(),
        key=lambda item: item["porcentaje"],
        reverse=True,
    )
    return resultados[:limite]
