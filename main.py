import datetime as dt


class Record:
    # здесь в качестве дефолтного параметра лучше использовать None,
    # потому что в любом случае значение будет переопределено и в пустой строке необходимости нет
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # здорово, что использовал тернарный оператор:)
        # но еще важно сохранить читаемость кода и сделать переносы так, чтобы все было понятно сразу
        # чисто интуитивно -- хочется not date в 14-ю строчку унести, а в целом, есть классная либа:
        # https://pypi.org/project/black/ которая умеет красиво форматировать код сама)
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # вот здесь IDE-шка еще должна была ругнуться - в питоне переменные принято писать в snake case:
        # https://en.wikipedia.org/wiki/Snake_case
        # с большой буквы можно называть классы, но тут еще произошла коллизия - переменная названа так же,
        # как класс в 4 строке, это тоже не очень хорошо
        # есть еще такая аналогия - не принято использовать в качестве переменных
        # "while", "next", "iter"..., потому что такие названия уже зарезервированы (встроенные методы)
        # в некоторых случаях конечно удастся обмануть питон, но не всегда:)
        for Record in self.records:
            # dt.datetime.now().date() лучше записать в переменную и вынести из цикла,
            # чтобы не вычислять на каждой итерации. в 41 строке чисто стилистически - можно += поставить,
            # так будет капельку красивее)
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        # а вот здесь правильно назвал переменную:)
        # внутри цикла - смотри, если приходится больше 1 раза вычислять одно и то же значение,
        # лучше вынести его в отдельную переменную
        # а еще питон вот так умеет: 0 < variable <= 3, бывает удобно)
        for record in self.records:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            # за f-строки лайк:)
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            # вот тут скобочки не нужны, просто return 'Хватит есть!'
            # судя по использованию тернарного оператора, тебе нравится экономить строчки)
            # в таком случае можно убрать этот else, работать будет так же
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # вот здесь в параметрах курсы не нужны, ты же вынес их в константы, к ним можно обращаться)
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # а почему в первом ифе сравниваешь с currency, а потом с currency_type? там, конечно, то же самое лежит,
        # но лучше в таких случаях использовать одну переменную)
        # можно было еще кстати сделать мапку вида {'usd': 'USD'} и вынести в константы в начало класса,
        # тогда currency_type можно чуть красивее вычислять. плюс тебе в последствии может добавиться еще какая-то
        # валюта, чтобы не дописывать иф, можно просто в словарь значение добавить
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # вот здесь думаю опечатка, но должен быть один знак равно
            cash_remained == 1.00
            currency_type = 'руб'
        # вот здесь хочется перенос строки)
        # вроде мелочь, но разделение кода на смысловые блоки сильно помогает улучшить читабельность
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # вот здесь можно поставить else и не вычислять "cash_remained < 0", но в коммерческой разработке иногда
        # пишут и так - в случае, когда нужно сделать акцент на таком кейсе
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

        # кстати, в 3.10 питоне появился switch case:) https://habr.com/ru/post/585216/

    def get_week_stats(self):
        # вот здесь return забыл
        super().get_week_stats()
