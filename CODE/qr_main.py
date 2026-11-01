
import qrcode
import os
import uuid

def getnerateQR(text):

    # Create folder if it doesn't exist
    folder = os.path.join("static", "qrcodes")
    os.makedirs(folder, exist_ok=True)

    # Generate unique filename
    filename = f"{uuid.uuid4().hex}.png"
    filepath = os.path.join(folder, filename)

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )

    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    img.save(filepath)

    # Return path relative to static folder
    return f"qrcodes/{filename}"
