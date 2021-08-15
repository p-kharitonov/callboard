from django import template

register = template.Library()


@register.filter(name=
                 'is_plural')
def is_plural(value, args):
    value = int(value)
    args = args.split(',')
    my_dict = {
        0: 2,
        1: 0,
        2: 1,
        3: 1,
        4: 1,
        5: 2,
        6: 2,
        7: 2,
        8: 2,
        9: 2,
    }
    if 11 <= value <= 19:
        return f'{value} {args[2]}'
    else:
        value = value % 10
        return f'{value} {args[my_dict[value]]}'

