from flask import Flask, jsonify

app = Flask(__name__)

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
