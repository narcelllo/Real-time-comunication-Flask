from flask import Flask, jsonify, request
from repository.database import db
from db_models.payment import Payment
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/Real-time'
app.config['SECRET_KEY'] = 'SECRET_KEY_WEBSOCKET'

db.init_app(app)

#Route responsible for creating the payment.
@app.route('/payments/pix', methods={'POST'})
def create_payments_pix():
    data = request.get_json()
    
    if 'value' not in data:
        return jsonify({"message": "Invalid value"}), 400
    
    expiration_date = datetime.now() + timedelta(minutes=30)

    new_payment = Payment(value=data['value'],
                          expiration_date=expiration_date)
    db.session.add(new_payment)
    db.session.commit()

    return jsonify({"message": "the pyment has been created",
                    "payment": new_payment.to_dict()})

#Route responsible for receiving the payment confirmation. "WebHook"
@app.route('/payments/pix/confirmation', methods={'POST'})
def pix_confirmation():
    return jsonify({"message": "The pyment has been confirmed"})

#Route responsible for displaying the payment confirmation.
@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id):
    return 'payment pix'

if __name__ == '__main__':
    app.run(debug=True)
