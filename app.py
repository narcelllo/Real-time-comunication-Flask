from flask import Flask, jsonify, request
from repository.database import db
from db_models.payment import Payment
from datetime import datetime, timedelta
from payments.pix import Pix

create_app = Flask(__name__)
create_app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/Real-time'
create_app.config['SECRET_KEY'] = 'SECRET_KEY_WEBSOCKET'

db.init_app(create_app)

#Route responsible for creating the payment.
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
    
    db.session.add(new_payment)
    db.session.commit()

    return jsonify({"message": "the pyment has been created",
                    "payment": new_payment.to_dict()})

#Route responsible for receiving the payment confirmation. "WebHook"
@create_app.route('/payments/pix/confirmation', methods={'POST'})
def pix_confirmation():
    return jsonify({"message": "The pyment has been confirmed"})

#Route responsible for displaying the payment confirmation.
@create_app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id):
    return 'payment pix'

if __name__ == '__main__':
    create_app.run(debug=True)
