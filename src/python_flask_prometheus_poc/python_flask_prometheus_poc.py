import random
import time
import logging
from flask import Flask, request, Response
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
app.logger.setLevel(logging.INFO)
metrics = PrometheusMetrics(app)

# static information as metric
metrics.info('app_info', 'Example python flask application and dummy load generator to test prometheus metrics from flask', version='1.0.0')


@app.route('/')
def main():
    msg = '/ called'
    app.logger.info(msg)
    return Response(msg, mimetype='text/plain')


@app.route('/skip')
@metrics.do_not_track()
def skip():
    return Response('/skip called', mimetype='text/plain')


@app.route('/<item_type>')
@metrics.do_not_track()
@metrics.counter('invocation_by_type', 'Number of invocations by type', labels={'item_type': lambda: request.view_args['item_type']})
def by_type(item_type):
    msg = '/{} called'.format(item_type)
    app.logger.info(msg)
    return Response(msg, mimetype='text/plain')


@app.route('/long-running')
@metrics.gauge('in_progress', 'Long running requests in progress')
def long_running():
    sleep_time = random.randint(2,5)
    msg = '/long-running called - sleeping for {} seconds'.format(sleep_time)
    time.sleep(sleep_time)
    app.logger.info(msg)
    return Response(msg, mimetype='text/plain')


@app.route('/status/<int:status>')
@metrics.do_not_track()
@metrics.summary('requests_by_status', 'Request latencies by status', labels={'status': lambda r: r.status_code})
@metrics.histogram('requests_by_status_and_path', 'Request latencies by status and path', labels={'status': lambda r: r.status_code, 'path': lambda: request.path})
def echo_status(status):
    msg = '/status/{} called'.format(status)
    app.logger.info(msg)
    return Response(msg, mimetype='text/plain')


@app.route('/maybe-error')
def maybe_error():
    error_codes = [
        400,
        401,
        403,
        404,
        500,
        414,
        501,
        503,
    ]
    success_codes = [
        200,
        201,
        202,
        304,
    ]
    random.shuffle(error_codes)
    random.shuffle(success_codes)
    response_code = 200
    draw = random.choice(range(0,100))
    if draw > 70:
        response_code = random.choice(error_codes)
    else:
        response_code = random.choice(success_codes)
    app.logger.info('draw={}   response_code={}'.format(draw, response_code))
    return 'served', response_code
