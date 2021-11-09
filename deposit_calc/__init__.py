"""
# Расчет депозитов
"""

import datetime
import json
from calendar import monthrange
import traceback
from dateutil.relativedelta import relativedelta


def request_val_validate(depositdate: str, periods: int, amount: int, rate: float, in_limits: dict) -> [bool, str]:
    '''
    Функция проверки ограничений
    :param depositdate: Starting date for deposit
    :param periods: Количество периодов (месяцев)
    :param amount: Сумма вклада
    :param rate: Процентная ставка по вклад
    :param in_limits: dict with limits to check
    :return:  false/truе без ошибок/с ошибками, коды ошибок
    '''

    # Иницаализация встроенных переменных
    val_error = False
    error_code = 'E000 - No error'
    val_pos = 0

    # проверяем входные значения настроек
    try:
        period_max = in_limits['period_max']
        period_min = in_limits['period_min']
        amount_min = in_limits['amount_min']
        amount_max = in_limits['amount_max']
        rate_min = in_limits['rate_min']
        rate_max = in_limits['rate_max']
    except:
        error_code = "E100 - Limits load fail on validation - check config.py "
        val_error = True

    # Основной набор проверок
    try:
        # Депозит должен быть Int
        if not val_error:
            try:
                if type(amount) != int:
                    error_code = "E002 - Amount is not Int"
                    val_error = True
            except:
                error_code = "E002 - Amount is not Int"
                val_error = True
        val_pos = 1

        # депозит должен быть больше 0
        if not val_error:
            if amount < 0:
                error_code = "E001 - Amount less than 0"
                val_error = True
        val_pos = 2

        # Депозит должен быть указан с точностью не больше копейки - домножаем на 100, не должно остаться копеек
        if not val_error:
            if not float.is_integer(amount * 100.0):
                error_code = "E003 - Amount have more than 2 digits in decimal part"
                val_error = True
        val_pos = 3

        # Количество месяцев должно быть целым положительным числом числом
        if not val_error:
            if not isinstance(periods, int):
                error_code = "E004 - Periods is not positive int"
                val_error = True
        val_pos = 4

        # Количество месяцев должно быть 1 и более
        if not val_error:
            if periods < 1:
                error_code = "E005- Periods must be bigger than 1 "
                val_error = True
        val_pos = 5

        # Количество месяцев дольжно быть разумно большим
        if not val_error:
            if periods > 100:
                error_code = "E006 - Periods must be less than one century "
                val_error = True
        val_pos = 6

        # rate должнен быть float
        if not val_error:
            try:
                float(rate)
            except ValueError:
                error_code = "E007 - Rate is not Float"
                val_error = True
        val_pos = 7

        # Дата депозита должна быть строкой формата dd.mm.YYYY
        if not val_error:
            if not (isinstance(depositdate, str) and len(depositdate) == 10):
                error_code = "E008 - depositdate is not well formed"
                val_error = True
        val_pos = 8

        # Дата депозита должна быть существующей
        if not val_error:
            try:
                # преобразуем строку в дату, если выйдет - будем ее исрользовать дальше
                deposit_date_conv = datetime.datetime.strptime(depositdate, '%d.%m.%Y').date()
            except:
                error_code = "E009 - depositdate not real date"
                val_error = True

        # проверка на периоды в рамках заданных лимитов
        if not val_error:
            if periods < period_min or periods > period_max:
                error_code = 'E200 - Period is out of boundaries '
                val_error = True

        # проверка на процентную ставку в рамках заданных лимитов
        if not val_error:
            if amount < amount_min or amount > amount_max:
                error_code = 'E201 - Amount is out of boundaries '
                val_error = True

        # проверка на сумму вклада в рамках заданных лимитов
        if not val_error:
            if rate < rate_min or rate > rate_max:
                error_code = f'E202 - Rate is out of boundaries {rate_min}< {rate}<{rate_max}'
                val_error = True

    except:
        error_code = "E010 - Unknown error in validation after check # " + str(val_pos) + ' ' + traceback.format_exc()
        val_error = True

    # Проеверяем, чем кончилась валидация. Если ошибки нет - продолжаем. Если есть - возвращем результат и выходим
    finally:
        if val_error:
            # print (errorcode)
            return True, error_code
        else:
            return False, 'No errors'


def month_cap_calc(depositdate: str, periods: int, amount: int, rate: float) -> [bool, str]:
    """
    Функция расчета депозита
    :param depositdate: дата заявки dd.mm.YYYY
    :param periods: количество месяцев депозита
    :param amount: сумма депозита
    :param rate: процентная ставка
    :return: false/truе без ошибок/с ошибками, result
    """
    # Проверка на валидность входных параметров не производится - используйте валидирующий декоратор

    try:
        # Считаем депозит по формуле из Excel.
        # запись пойдет в список
        calculated = dict()
        deposit_date_conv = datetime.datetime.strptime(depositdate, '%d.%m.%Y').date()
        deposit_day = deposit_date_conv.day

        for period_pos in range(1, periods + 1):
            # рассчитываем дату конца месяца

            calculated_end_date = datetime.date(deposit_date_conv.year, deposit_date_conv.month,
                                                monthrange(deposit_date_conv.year, deposit_date_conv.month)[1])
            if deposit_day > calculated_end_date.day:
                end_date = calculated_end_date
            else:
                end_date = datetime.date(deposit_date_conv.year, deposit_date_conv.month, deposit_day)
            amount = amount + amount * rate / (12 * 100)
            # провверим выход значения за разумные пределы
            if amount > 10E16:
                raise TypeError
            end_date_str = end_date.strftime('%d.%m.%Y')
            calculated.update({end_date_str: float("%10.2f" % amount)})
            deposit_date_conv = deposit_date_conv + relativedelta(months=1)
        # возвращаем расчет
        result = json.dumps(calculated, indent=1)
        return False, result
    except TypeError:
        calculated = dict()
        calculated.update({'error': 'E012 - calculated value is too big'})
        return True, json.dumps(calculated)
    except:
        calculated = dict()
        calculated.update({'error': 'E011 - unknown error in calculation'})
        return True, json.dumps(calculated)
