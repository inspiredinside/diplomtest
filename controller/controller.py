import logging
import sys
import time
from flask import Flask, Response, request, abort, send_file, session, jsonify, make_response
from PIL import Image
from helper.helpers import generate, validate, get_forecast


def create_logger(level=logging.INFO):
    log = logging.getLogger("kafka_exporter")
    log.setLevel(level)
    # handler = logging.StreamHandler(sys.stdout)
    fh = logging.FileHandler("trace.log")
    fh.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - PID:%(process)d - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    log.addHandler(fh)
    return log


log = create_logger(level=logging.INFO)
app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate_forecast():
    content = request.json
    try:
        start_date = content['startDate']
        end_date = content['endDate']
        ticker = content['ticker']
        epochs = content['epochs']
        batch_size = content['batchSize']
    except KeyError as e:
        bad_request = make_response('Bad request, check the fields: %s' % str(e), 400)
        return bad_request
    check = get_forecast()
    return jsonify(
        filename="sheeeit filename!"
    )



@app.route('/getImage', methods=['GET'])
def send_image():
    # content = request.json
    # print(content)
    # img = Image.new('RGB', [500, 500], 255)
    # data = img.load()
    # for x in range(img.size[0]):
    #     for y in range(img.size[1]):
    #         data[x, y] = (
    #             x % 255,
    #             y % 255,
    #             (x ** 2 - y ** 2) % 255,
    #         )
    # saved_file_name = generate()
    # yield img.save('%s.png' % saved_file_name)
    # filename = '%s.png' % saved_file_name
    return send_file(sys.path[1] + '/savedfile_0x386cc4f0.png', mimetype='image/png')

@app.after_request
def after_request_func(response):

    """
    This function will run after a request, as long as no exceptions occur.
    It must take and return the same parameter - an instance of response_class.
    This is a good place to do some application cleanup.
    """
    print("after_request is running!", response)
    return response