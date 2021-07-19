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
        now = dt.datetime.now()
        stats_today = 0
        for i in self.records:
            if now.date() == i.date.date():
                stats_today = stats_today + i.amount

        print(stats_today, 'today_stats')
        return stats_today

    """Считает, сколько денег потрачено за последние 7 дней."""
    def get_week_stats(self):
        stats = 0
        seven_days = timedelta(7)
        now = dt.datetime.now()
        minusseven = now - seven_days

        for i in self.records:
            if minusseven < i.date:
                stats = stats + i.amount

        print(stats, 'get_week_stats')
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
            self.date = dt.datetime.strptime(date, '%d.%m.%Y')
        elif date is None:
            self.date = dt.datetime.now()
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
                  f'но с общей калорийностью не более {newlimit} кКал')
        elif limit == today_stats:
            print('Хватит есть!')
        elif today_stats > limit:
            today_stats = round(today_stats - limit, 2)
            print('Хватит есть!')


class CashCalculator(Calculator):

    """Определяет, сколько денег можно потратить
    сегодня в рублях, долларах или евро."""
    def get_today_cash_remained(self, currency):
        USD_RATE = 60
        EURO_RATE = 70

        limit = self.limit
        today_stats = self.get_today_stats()
        print('limit', limit)
        print('today_stats', today_stats)
        if currency == 'usd':
            limit = limit / USD_RATE
            today_stats = today_stats / USD_RATE
        elif currency == 'eur':
            limit = limit / EURO_RATE
            today_stats = today_stats / EURO_RATE

        if limit > today_stats:
            newlimit = round(limit - today_stats, 2)
            print(f'На сегодня осталось {newlimit} руб/USD/Euro')
        elif limit == today_stats:
            print('Денег нет, держись')
        elif today_stats > limit:
            today_stats = round(today_stats - limit, 2)
            print(f'Денег нет, держись: твой долг -'
                  f'{today_stats} руб/USD/Euro')
            