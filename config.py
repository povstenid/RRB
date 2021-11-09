"""
Конфигурационный файл для сервиса рачсчета депозитов
Задает лимиты на расчет депозитов и настраивает flask service_app
"""

# настройка глобальных ограничений

"""
    period_min - Минимальный период
    period_max - максимальный период депозита
    amount_min - Минимальаня сумма депозита
    amount_max - Максимальная сумма депозита
    rate_min   - Минмальная ставка
    rate_max   - Максимальная ставка
)
"""

deposit_limits = {'period_min': 1, 'period_max': 60, 'amount_min': 10000, 'amount_max': 3000000, 'rate_min': 1.0,
                  'rate_max': 8.0}
