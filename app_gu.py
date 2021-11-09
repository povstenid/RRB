#!flask/bin/python
from flask import Flask, jsonify, request, make_response
import deposit_calc
import config
import json

service_app = Flask(__name__)


@service_app.errorhandler(400)
def not_found():
    return make_response(jsonify({'error': 'Bad request'}), 400)


@service_app.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


@service_app.route('/deposit_service', methods=['POST'])
def deposit_service():
    """
    Service for deposit calculation
    """
    try:
        for name in request.json:
            if name not in ('date', 'periods', 'amount', 'rate'):
                return jsonify({'error': 'E305 - JSON too many fields'}), 400
    except:
        return jsonify({'error': 'E306 - error in parsing JSON '}), 400

    try:
        if not request.json:
            return jsonify({'error': 'E300 - JSON request not valid'}), 400
        if 'date' in request.json and type(request.json['date']) != str:
            return jsonify({'error': 'E301 - JSON[date]  not valid'}), 400
        if 'periods' in request.json and type(request.json['periods']) != int:
            return jsonify({'error': 'E302 - JSON[periods]  not valid'}), 400
        if 'amount' in request.json and type(request.json['amount']) != int:
            return jsonify({'error': 'E303 - JSON[amount]  not valid'}), 400
        if 'rate' in request.json and type(request.json['rate']) != float:
            return jsonify({'error': 'E304 - JSON[rate]  not valid'}), 400

        in_date = request.json['date']
        in_periods = request.json['periods']
        in_amount = request.json['amount']
        in_rate = request.json['rate']

    except:
        return jsonify({'error': 'unknown error in JSON check '}), 400

    try:
        val_result, val_error = deposit_calc.request_val_validate(in_date, in_periods, in_amount, in_rate,
                                                                  config.deposit_limits)

        if val_result:
            return jsonify({'error': val_error}), 400

        calc_error, calc_res = deposit_calc.month_cap_calc(in_date, in_periods, in_amount, in_rate)
        if not calc_error:
            response = service_app.response_class(
                response=json.loads(json.dumps(calc_res, indent=4)),
                status=200,
                mimetype='application/json'
            )
            return response
        else:
            return jsonify({'error': calc_res}), 400
    except:
        return jsonify({'error': 'unknown error in validation/calculation'}), 400


if __name__ == '__main__':
    service_app.run()
