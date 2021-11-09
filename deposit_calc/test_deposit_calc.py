import config
import deposit_calc


def test_default():
    amount=10000
    periods=7
    rate=6.0
    depositDate='31.01.2021'
    assert deposit_calc.month_cap_calc(depositDate, periods, amount, rate)[0]==False
    assert deposit_calc.request_val_validate(depositDate,periods,amount,rate,config.deposit_limits)[0]==False


def test_amount_is_too_small():
    amount=9999
    periods=7
    rate=6.0
    depositDate='31.01.2021'
    assert deposit_calc.month_cap_calc(depositDate, periods, amount, rate)[0] == False
    assert deposit_calc.request_val_validate(depositDate, periods, amount, rate, config.deposit_limits)[0] == True

def test_amount_is_too_big():
    amount=6000000
    periods=7
    rate=6.0
    depositDate='31.01.2021'
    assert deposit_calc.month_cap_calc(depositDate, periods, amount, rate)[0] == False
    assert deposit_calc.request_val_validate(depositDate, periods, amount, rate, config.deposit_limits)[0] == True


def test_period_too_long():
    amount=1
    periods=101
    rate=1200
    depositDate='31.01.2021'
    assert deposit_calc.month_cap_calc(depositDate, periods, amount, rate)[0] == True
    assert deposit_calc.request_val_validate(depositDate, periods, amount, rate, config.deposit_limits)[0] == True

def test_perod_too_small():
    amount=1
    periods=0
    rate=6
    depositDate='31.01.2021'
    assert deposit_calc.month_cap_calc(depositDate, periods, amount, rate)[0] == False
    assert deposit_calc.request_val_validate(depositDate, periods, amount, rate, config.deposit_limits)[0] == True

def test_rate_small():
    amount=2000
    periods=7
    rate=0.9
    depositDate='31.01.2021'
    assert deposit_calc.month_cap_calc(depositDate, periods, amount, rate)[0]==False
    assert deposit_calc.request_val_validate(depositDate,periods,amount,rate,config.deposit_limits)[0]==True

def test_rate_big():
    amount=2000
    periods=7
    rate=9.1
    depositDate='31.01.2021'
    assert deposit_calc.month_cap_calc(depositDate, periods, amount, rate)[0]==False
    assert deposit_calc.request_val_validate(depositDate,periods,amount,rate,config.deposit_limits)[0]==True

def test_date_format_wrong():
    amount=10000
    periods=7
    rate=6.0
    depositDate='01.31.2021'
    assert deposit_calc.month_cap_calc(depositDate, periods, amount, rate)[0]==True
    assert deposit_calc.request_val_validate(depositDate,periods,amount,rate,config.deposit_limits)[0]==True

def test_amount_format_wrong():
    amount=0.99
    periods=7
    rate=6.0
    depositDate='31.01.2021'
    #print(deposit_calc.month_cap_calc(depositdate, periods, amount, rate))
    #print( deposit_calc.request_val_validate(depositdate,periods,amount,rate,config.deposit_limits))
    assert deposit_calc.month_cap_calc(depositDate, periods, amount, rate)[0]==False
    assert  deposit_calc.request_val_validate(depositDate,periods,amount,rate,config.deposit_limits)[0]==True

def test_amount_format2():
    amount='money'
    periods=7
    rate=6.0
    depositDate='31.01.2021'
    assert deposit_calc.month_cap_calc(depositDate, periods, amount, rate)[0]==True
    assert deposit_calc.request_val_validate(depositDate,periods,amount,rate,config.deposit_limits)[0]==True

def test_periods_format():
    amount=20000
    periods=6.6
    rate=6.0
    depositDate='31.01.2021'
    assert deposit_calc.month_cap_calc(depositDate, periods, amount, rate)[0]==True
    assert  deposit_calc.request_val_validate(depositDate,periods,amount,rate,config.deposit_limits)[0]==True

def test_periods_format2():
    amount=20000
    periods='month'
    rate=6.0
    depositDate='31.01.2021'
    assert deposit_calc.month_cap_calc(depositDate, periods, amount, rate)[0]==True
    assert deposit_calc.request_val_validate(depositDate,periods,amount,rate,config.deposit_limits)[0]==True

def test_rate_format():
    amount=20000
    periods=6.6
    rate=6
    depositDate='31.01.2021'
    assert deposit_calc.month_cap_calc(depositDate, periods, amount, rate)[0]==True
    assert deposit_calc.request_val_validate(depositDate,periods,amount,rate,config.deposit_limits)[0]==True

def test_rate_format2():
    amount=20000
    periods=6
    rate='month'
    depositDate='31.01.2021'
    assert deposit_calc.month_cap_calc(depositDate, periods, amount, rate)[0]==True
    assert deposit_calc.request_val_validate(depositDate,periods,amount,rate,config.deposit_limits)[0]==True

def test_date_format2():
    amount=20000
    periods=6
    rate=6.0
    depositDate=31012021
    assert deposit_calc.month_cap_calc(depositDate, periods, amount, rate)[0]==True
    assert deposit_calc.request_val_validate(depositDate,periods,amount,rate,config.deposit_limits)[0]==True