import deposit_calc
def test_default():
    amount=10000
    periods=7
    rate=6.0
    depositDate='31.01.2021'
    print(deposit_calc.month_cap_calc(amount, periods, rate, depositDate))

def test_amount_is_not_real():
    amount='10000'
    periods=7
    rate=6.0
    depositDate='31.01.2021'
    print(deposit_calc.month_cap_calc(amount, periods, rate, depositDate))

def test_too_big():
    amount=1
    periods=99
    rate=1200
    depositDate='31.01.2021'
    print(deposit_calc.month_cap_calc(amount, periods, rate, depositDate))

test_default()
test_amount_is_not_real()
test_too_big()