#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
import deposit_calc
import traceback

app = Flask(__name__)

# функция проверки на диапазон допустимых значений.
def request_val_validate(in_periods,in_amount,in_rate):
    # Значения ограниячений
    period_min=1
    period_max=60
    amount_min=10000
    amount_max=3000000
    rate_min=1.0
    rate_max=8.0


    if in_periods< period_min or  in_periods > period_max:
        return True, jsonify({'error': 'E200 - Period is out of boundaries '})
    if in_amount < amount_min or in_amount > amount_max:
        return True, jsonify({'error': 'E201 - Amount is out of boundaries '})
    if in_rate < rate_min or rate_min > rate_max:
        return True, jsonify({'error': 'E202 - Rate is out of boundaries '})
    return False,'No error'



@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.route('/deposit_service', methods = ['POST'])
def deposit_service():
    print(request.json)
    try:
        if not request.json:
            return jsonify({'error':'E300 - JSON request not valid'}),400
        if 'date' in request.json and type(request.json['date']) != str:
            return jsonify({'error':'E301 - JSON[date]  not valid'}),400
        if 'periods' in request.json and type(request.json['periods']) !=int:
            return jsonify({'error':'E302 - JSON[periods]  not valid'}),400
        if 'amount' in request.json and type(request.json['amount']) !=int:
            return jsonify({'error': 'E303 - JSON[amount]  not valid'}), 400
        if 'rate' in request.json and type(request.json['rate']) !=float:
            return jsonify({'error': 'E303 - JSON[rate]  not valid'}), 400

        in_date=request.json['date']
        in_periods=request.json['periods']
        in_amount=request.json['amount']
        in_rate=request.json['rate']
        print(in_date,in_periods,in_amount,in_rate)

        val_result,val_error = request_val_validate (in_periods,in_amount,in_rate)
        if val_result:
            return  val_error, 400

        calc_error,calc_res=deposit_calc.month_cap_calc(in_date,in_periods,in_amount,in_rate)
        if calc_error == False:
            return calc_res, 200
        else:
            return calc_res, 400
    except:
        return jsonify({'error': 'unknown in db '+traceback.format_exc()}), 400
app.run()