import logging
import sys
import time
from flask import Flask, Response, request, abort, send_file, session, jsonify, make_response
from PIL import Image
from flask_cors import CORS, cross_origin

from helper.helpers import validate, get_forecast, convert_dates_to_epoch_format
from service import calculation


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
CORS(app)


@app.route('/calculate', methods=['POST'])
@cross_origin()
def calculate_forecast():
    content = request.json
    try:
        start_date = content['startDate']
        end_date = content['endDate']
        print(type(end_date))
        ticker = content['ticker']
        interval = content['interval']
        epochs = content['epochs']
        batch_size = content['batchSize']
        epoch_start_date, epoch_end_date = convert_dates_to_epoch_format(start_date, end_date)
        data_file = get_forecast(period1=epoch_start_date,period2=epoch_end_date, ticker=ticker, interval=interval)
        image = calculation.calculate(
            data_file=data_file,
            end_date=end_date,
            epochs=epochs,
            batch_size=batch_size)

    except KeyError as e:
        bad_request = make_response('Bad request, check the fields: %s' % str(e), 400)
        return bad_request
    except (IOError, ValueError) as CSVError:
        server_error = make_response('Internal server error: %s' % str(CSVError), 500)
        return server_error
    return jsonify(
        imageId=image,
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
    image_id = request.args.get('imageId')
    response = make_response(send_file(sys.path[1] + '/figures/' + image_id, mimetype='image/png'))
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


# @app.after_request
# def after_request_func(response):
#     """
#     This function will run after a request, as long as no exceptions occur.
#     It must take and return the same parameter - an instance of response_class.
#     This is a good place to do some application cleanup.
#     """
#     print("after_request is running!", response)
#     return response
