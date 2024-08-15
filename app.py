from flask import Flask, jsonify
from repository.database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'SECRET_KEY_WEBSOCKET'

db.init_app(app)

#Route responsible for creating the payment.
@app.route('/payments/pix', methods={'POST'})
def create_peyments_pix():
    return jsonify({"message": "the pyment has been created"})

#Route responsible for receiving the payment confirmation. "WebHook"
@app.route('/payments/pix/confirmation', methods={'POST'})
def pix_confirmation():
    return jsonify({"message": "the pyment has been confirmed"})

#Route responsible for displaying the payment confirmation.
@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id):
    return 'peyment pix'

if __name__ == '__main__':
    app.run(debug=True)
