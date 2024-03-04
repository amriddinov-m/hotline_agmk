import datetime
import locale
locale.setlocale(locale.LC_NUMERIC, 'ru_RU.utf8')


def clear_int_string(int_string):
    """ Приводит значения вида ` 300 000` в `300000` """
    return int_string.strip().replace(' ', '')


def to_locale(value):
    return locale.format('%d', value, grouping=True)


def order_text(order):
    text = f'Номер заказа #{order.id}\n' \
           f'Адрес: {order.address}\n' \
           f'Номер телефона: {order.phone_number}\n' \
           f'Комментарии: {order.comment}\n' \
           f'Состав заказа:\n\n'
    total = 0
    for item in order.orderitem_set.all():
        total_price = item.count * item.product.price
        total += total_price
        text += f"{item.product}✖ {item.count}шт X {to_locale(item.product.price)} = {to_locale(total_price)} \n\n"
    text += f'\nИтого: {to_locale(total)}'
    text += f'\nЗаказ создан в: \n{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n\n'
    return text
