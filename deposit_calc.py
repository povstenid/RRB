# Расчет депозитов


import datetime
import json
from calendar import monthrange
import traceback

from pipenv.vendor.dateutil.relativedelta import relativedelta


# Функция расчета депозита
# amount - сумма депозита
# periods - количество месяцев депозита
# rate - процентная ставка
# depositDated - дата заявки dd.mm.YYYY


def month_cap_calc(depositDate,periods,amount,rate):
    # Иницаализация встроенных переменных
    val_error = False
    errorcode = 'E000 - No error'
    result = '{}'
    val_pos = 0
    deposit_date_conv=None
    # Проверка на валидность входных параметров
    try:
        while val_error == False:

            # Депозит должен быть Float
            try:
                if type(amount) == int:
                    pass
                else:
                    errorcode = "E002 - Amount is not Int"
                    val_error = True
                    break

            except:
                errorcode = "E002 - Amount is not Float"
                val_error = True
                break
            val_pos = 1

            # депозит должен быть больше 0
            if amount < 0:
                errorcode = "E001 - Amount less than 0"
                val_error = True
                break
            val_pos = 2

            # Депозит должен быть указан с точностью не больше копейки - домножаем на 100, не должно остаться копеек
            if not float.is_integer(amount * 100.0):
                errorcode = "E003 - Amount have more than 2 digits in decimal part"
                val_error = True
                break
            val_pos = 3
            # Количество месяцев должно быть целым положительным числом числом
            if not isinstance(periods, int):
                errorcode = "E004 - Periods is not positive int"
                val_error = True
                break
            val_pos = 4
            # Количество месяцев должно быть 1 и более
            if periods < 1:
                errorcode = "E005- Periods must be bigger than 1 "
                val_error = True
                break
            val_pos = 5
            print('periods='+str(periods))
            # Количество месяцев дольжно быть разумно большим
            if periods > 100:
                errorcode = "E006 - Periods must be less than one century "
                val_error = True
                break
            val_pos = 6
            # rate должнен быть float
            try:
                float(rate)
            except ValueError:
                errorcode = "E007 - Rate is not Float"
                val_error = True
                break
            val_pos = 7
            # Дата депозита должна быть строкой формата dd.mm.YYYY

            if not (isinstance(depositDate, str) and len(depositDate) == 10):
                errorcode = "E008 - depositDate is not well formed"
                val_error = True
                break
            val_pos = 8

            # Дата депозита должна быть существующей
            try:
                # преобразуем строку в дату, если выйдет - будем ее исрользовать дальше
                deposit_date_conv = datetime.datetime.strptime(depositDate, '%d.%m.%Y').date()

            except:
                errorcode = "E009 - depositDate not real date"
                val_error = True
                break

            # Если ошибки нет - рвем цикл
            val_pos = 9
            if val_error == False:
                break
    except:
        errorcode = "E010 - Unknown error in validation after check # " + str(val_pos) + ' ' + traceback.format_exc()

        val_error = True

    # Проеверяем, чем кончилась валидация. Если ошибки нет - продолжаем. Если есть - возвращем результат и выходим

    if val_error == True:
        # print (errorcode)
        calculated = dict()
        calculated.update({'error': errorcode})
        return True, json.dumps(calculated)

    else:
        try:
            # Считаем депозит по формуле из Excel.
            # запись пойдет в список
            calculated = dict()

            for period_pos in range(1, periods + 1):
                # рассчитываем дату конца месяца
                end_date = datetime.date(deposit_date_conv.year, deposit_date_conv.month,
                                         monthrange(deposit_date_conv.year, deposit_date_conv.month)[1])
                amount = amount + amount * rate / (12 * 100)
                # провверим выход значения за разумные пределы
                if amount>10E16: raise TypeError
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
