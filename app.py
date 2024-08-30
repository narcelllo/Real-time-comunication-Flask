from flask import Flask, jsonify, request, send_file, render_template
from repository.database import db
from db_models.payment import Payment
from datetime import datetime, timedelta
from payments.pix import Pix
from flask_socketio import SocketIO

create_app = Flask(__name__)
create_app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/Real-time'
create_app.config['SECRET_KEY'] = 'SECRET_KEY_WEBSOCKET'

db.init_app(create_app)
socketio = SocketIO(create_app)

# Creating the payment.
@create_app.route('/payments/pix', methods={'POST'})
def create_payments_pix():
    data = request.get_json()
    
    if 'value' not in data:
        return jsonify({"message": "Invalid value"}), 400
    
    expiration_date = datetime.now() + timedelta(minutes=30)

    new_payment = Payment(value=data['value'],
                          expiration_date=expiration_date)
    
    pix_obj = Pix()
    data_payment_pix = pix_obj.create_payment()
    new_payment.bank_payment_id = data_payment_pix["bank_payment_id"]
    new_payment.qr_code = data_payment_pix["qr_code_path"]

    db.session.add(new_payment)
    db.session.commit()

    return jsonify({"message": "the pyment has been created",
                    "payment": new_payment.to_dict()})
# Show qr code .png
@create_app.route('/payments/pix/qr_code/<file_name>', methods=["GET"])
def get_image(file_name):
    return send_file(f"static/img/{file_name}.png", mimetype='image/png')

# Receiving the payment confirmation. "WebHook"
@create_app.route('/payments/pix/confirmation', methods={'POST'})
def pix_confirmation():
    data = request.get_json()

    # Validations
    if "bank_payment_id" not in data and "value" not in data:
        return jsonify({"message": "Invalid payment data"}), 400
    
    # Payment?
    payment = Payment.query.filter_by(bank_payment_id=data.get("bank_payment_id")).first()

    if not payment or payment.paid:
        return jsonify({"message": "Payment not found"}), 404

    if data.get("value") != payment.value:
        return jsonify({"message": "Invalid payment data"}), 400
    
    payment.paid = True
    db.session.commit()
    socketio.emit(f'payment-confirmed-{payment.id}')

    return jsonify({"message": "The pyment has been confirmed"})

# Displaying the payment confirmation.
@create_app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id):
    payment = Payment.query.get(payment_id)

    if payment.paid:
        return render_template('confirmed_payment.html',
                            payment_id=payment.id,
                            value=payment.value)

    return render_template('payment.html',
                            payment_id=payment.id,
                            value=payment.value,
                            host="http://127.0.0.1:5000/",
                            qr_code=payment.qr_code)

#  Websockets
@socketio.on('connect')
def handle_connect():
    print("Client connected to the server")
    
if __name__ == '__main__':
    socketio.run(create_app, debug=True)
