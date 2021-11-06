import deposit_calc
import config

from config import deposit_limits
def test_default():
    amount=10000
    periods=7
    rate=6.0
    depositDate='31.01.2021'
    print(deposit_calc.request_val_validate(depositDate,periods,amount,rate,config.deposit_limits))
    print(deposit_calc.month_cap_calc(depositDate,periods,amount,rate))

def test_amount_is_not_real():
    amount=10000
    periods=7
    rate=6.0
    depositDate='31.01.2021'
    print(deposit_calc.month_cap_calc(depositDate,periods,amount,rate))

def test_too_big():
    amount=1
    periods=99
    rate=1200
    depositDate='31.01.2021'
    print(deposit_calc.month_cap_calc(depositDate,periods,amount,rate))

test_default()
test_amount_is_not_real()
test_too_big()