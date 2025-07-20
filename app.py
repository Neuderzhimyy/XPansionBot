from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

# === НАСТРОЙКИ ===
CRYPTOBOT_TOKEN = '433414:AAO3ZEu6tjCG3FKKn4KEAQdZ4hL6anNbJjX'  # <-- ВСТАВЬ СВОЙ ТОКЕН
CRYPTOBOT_CURRENCY = 'USDT'  # или 'TON', 'BTC', 'ETH', ...

# --- Функция создания инвойса только для CryptoBot ---
def create_crypto_invoice(user_id, amount, description):
    url = 'https://pay.crypt.bot/api/createInvoice'
    payload = {
        'asset': CRYPTOBOT_CURRENCY,
        'amount': amount,
        'description': description,
        'hidden_message': f'UserID:{user_id}',
        'paid_btn_name': 'openChannel',
        'paid_btn_url': 'https://t.me/YourChannel',
        'payload': str(user_id)
    }
    headers = {'Crypto-Pay-API-Token': CRYPTOBOT_TOKEN}
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    if data.get('ok'):
        return data['result']['pay_url']
    else:
        return None

# --- Эндпоинт для генерации платежных ссылок ---
@app.route('/api/pay', methods=['POST'])
def pay():
    data = request.json
    if not data:
        return jsonify({'ok': False, 'error': 'Нет данных'}), 400
    user_id = data.get('user_id')
    amount = data.get('amount')
    description = data.get('description')
    method = data.get('method')
    if not all([user_id, amount, description, method]):
        return jsonify({'ok': False, 'error': 'Не все параметры переданы'}), 400
    if method == 'cryptobot':
        url = create_crypto_invoice(user_id, amount, description)
    else:
        url = None
    if url:
        return jsonify({'ok': True, 'url': url})
    else:
        return jsonify({'ok': False, 'error': 'Ошибка при создании платежа'}), 400

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
