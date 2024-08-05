import logging
import json

from flask import Flask, request
from python_on_whales import docker


app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    app.logger.debug("Webhook JSON: %s", json.dumps(data))

    for alert in data['alerts']:
        if alert['labels']['alertname'] != 'ScaleUp':
            continue

        if alert['status'] == 'firing':
            app.logger.info("Scale up to 5")
            docker.compose.up(scales={'webapp': 5}, detach=True)
        elif alert['status'] == 'resolved':
            app.logger.info("Scale down to 1")
            docker.compose.up(scales={'webapp': 1}, detach=True)

    return '', 200


if __name__ == '__main__':
    app.logger.info("Running auto scaling webhook")
    app.run(host='0.0.0.0', port=5000)