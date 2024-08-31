import uuid
import qrcode

class Pix:
    def __init__(self):
        pass

    def create_payment(self, base_dir=""):

        # Create payment in the financial institution
        bank_payment_id = uuid.uuid4()

        # Create payment ID
        hash_payment = f'hash_payment_{bank_payment_id}'

        # Create qr code image 
        img = qrcode.make(hash_payment)

        # Save qr code image
        img.save(f"{base_dir}static/img/qr_code_payment{bank_payment_id}.png")

        return {"bank_payment_id": bank_payment_id,
                "qr_code_path": f"qr_code_payment{bank_payment_id}"}