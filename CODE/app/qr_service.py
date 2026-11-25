import os
import uuid
import qrcode

from flask import current_app


def generate_qr_image(data):

    qr_dir = os.path.join(
        current_app.static_folder,
        "image"
    )

    os.makedirs(qr_dir, exist_ok=True)

    filename = f"qr_{uuid.uuid4().hex}.png"

    filepath = os.path.join(qr_dir, filename)

    image = qrcode.make(data)
    image.save(filepath)

    return f"image/{filename}"