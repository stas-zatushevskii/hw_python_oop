
from typing import Optional
import datetime as dt

formate_date = "%d.%m.%Y"

class Record:
    def __init__(self, amount: float, comment: str,
                date: Optional[str] = None) -> None:
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, formate_date).date()



class Calculator:
    """Слаживатель для всего"""
    def __init__(self, limit: float):
        self.limit = limit
        self.records = []
    
    def add_record(self, record: Record):
        self.records.append(record)

    def get_today_stats(self):
        stats_today = []
        today = dt.datetime.today().date()
        for record in self.records:
            if record.date == today:
                stats_today.append(record.amount)
                sum_stats_today = sum(stats_today)
        return sum_stats_today

    def get_remained(self):
        remains = self.limit - self.get_today_stats()
        return remains 
        
    def get_week_stats(self):
        today = dt.date.today()
        week_start = today - dt.timedelta(days=7)
        week_sum = 0
        for record in self.records:
            if week_start <= record.date <= today:
                week_sum += record.amount
        return week_sum


class CashCalculator(Calculator):
    """Слаживатель для денег"""
    EURO_RATE = 87.0
    USD_RATE = 73.0
    RUB_RATE = 1

    def __init__(self, limit: float):
        super().__init__(limit)

    def get_today_cash_remained(self, currency: str) -> float:
        currencies = {
            "rub": ["руб", self.RUB_RATE],
            "eur": ["Euro", self.EURO_RATE],
            "usd": ["USD", self.USD_RATE]
        }
        cur_name, cur_rate = currencies[currency]
        limit_result: float = round(self.get_remained() / cur_rate, 2)
        if limit_result > 0:
            return f"На сегодня осталось {limit_result} {cur_name}"
        if limit_result == 0: 
            return "Денег нет, держись"
        return f"Денег нет, держись: твой долг - {abs(limit_result)} {cur_name}"



class CaloriesCalculator(Calculator):

    def __init__(self, limit: float):
        super().__init__(limit)

    def get_calories_remained(self):
        limit_result: int = self.get_remained()

        if limit_result > 0:
            return (f"Сегодня можно съесть что-нибудь ещё,"
            f"но с общей калорийностью не более {limit_result} кКал")
        return "Хватит есть!"