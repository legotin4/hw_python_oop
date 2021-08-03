import datetime as dt
from datetime import timedelta


class Calculator:
    def __init__(self, limit):
        """Дневной лимит трат/калорий, который задал пользователь."""
        self.limit = limit
        self.records = []

    """Сохраняет новую запись о приёме пищи."""
    def add_record(self, record_obj):
        self.records.append(record_obj)

    """Считает сколько денег потрачено сегодня."""
    def get_today_stats(self):
        now = dt.datetime.now().date()
        stats_today = 0
        for i in self.records:
            if now == i.date:
                stats_today = stats_today + i.amount

        return stats_today

    """Считает, сколько денег потрачено за последние 7 дней."""
    def get_week_stats(self):
        stats = 0
        seven_days = timedelta(7)
        now = dt.datetime.now().date()
        minusseven = now - seven_days

        for i in self.records:
            if minusseven < i.date:
                stats = stats + i.amount

        return stats


class Record:
    def __init__(self, amount, comment, date=None):
        """Денежная сумма или количество килокалорий."""
        self.amount = amount

        """Комментарий на что потрачено или откуда взялись калории."""
        self.comment = comment

        """Дата созданя записи. Передаётся в явном виде в конструктор,
        либо присваивается значение по умолчанию - текущая дата.
        """
        if type(date) == str:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        elif date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = date


class CaloriesCalculator(Calculator):
    """Определяет, сколько ещй калорий можно/нужно получить сегодня."""
    def get_calories_remained(self):
        limit = self.limit
        today_stats = self.get_today_stats()

        if limit > today_stats:
            newlimit = round(limit - today_stats, 2)
            print(f'Сегодня можно съесть что-нибудь ещё,'
                  f' но с общей калорийностью не более {newlimit} кКал')
        elif limit == today_stats:
            print('Хватит есть!')
        elif today_stats > limit:
            today_stats = round(today_stats - limit, 2)
            print('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = 60
    EURO_RATE = 70
    RUB_RATE = 1.0

    """Определяет, сколько денег можно потратить
    сегодня в рублях, долларах или евро."""
    def get_today_cash_remained(self, currency):
        limit = self.limit
        today_stats = self.get_today_stats()
        if currency == 'usd':
            today_stats = (limit - today_stats) / self.USD_RATE
            name = 'USD'
        elif currency == 'eur':
            today_stats = (limit - today_stats) / self.EURO_RATE
            name = 'Euro'
        elif currency == 'rub':
            today_stats = (limit - today_stats) / self.RUB_RATE
            name = 'руб'

        if limit > today_stats:
            newlimit = round(limit - today_stats, 2)
            print(f'На сегодня осталось {newlimit} {name}')
        elif limit == today_stats:
            print('Денег нет, держись')
        elif today_stats > limit:
            today_stats = round(today_stats - limit, 2)
            print(f'Денег нет, держись: твой долг -'
                  f'{today_stats} {name}')


cash_calculator = CashCalculator(1000)

r = Record(amount=300, comment='бар в Танин др', date='08.11.2019')
cash_calculator.add_record(r)
cash_calculator.add_record(Record(amount=30, comment='обед', date='4.05.2021'))
cash_calculator.add_record(Record(amount=60, comment='обед', date='8.05.2021'))
cash_calculator.add_record(Record(amount=300, comment='Паше на пиццу'))
cash_calculator.add_record(Record(amount=400, comment='Саше на суши'))
cash_calculator.add_record(Record(amount=400, comment='Сергею на сушки'))
cash_calculator.add_record(Record(amount=400, comment='Николаю на завтраки'))
cash_calculator.add_record(Record(amount=400, comment='Павлухе на мидии'))
cash_calculator.add_record(Record(amount=400, comment='Игорёхе на ватруши'))

cash_calculator.get_week_stats()


cash_calculator.get_today_stats()

cash_calculator.get_today_cash_remained('usd')
cash_calculator.get_today_cash_remained('rub')
cash_calculator.get_today_cash_remained('eur')
calories = CaloriesCalculator(13100)

calories.add_record(Record(amount=2000, comment='Печеньки'))
calories.add_record(Record(amount=400, comment='Сырок'))
calories.add_record(Record(amount=100, comment='Сушки'))
calories.add_record(Record(amount=400, comment='Сакэ'))
calories.add_record(Record(amount=400, comment='Колбаса варёно-сушённая'))
calories.add_record(Record(amount=200, comment='Трюфили'))
calories.add_record(Record(amount=1400, comment='Обед'))
calories.add_record(Record(amount=400, comment='Суши'))

calories.get_today_stats()
calories.get_week_stats()
calories.get_calories_remained()
