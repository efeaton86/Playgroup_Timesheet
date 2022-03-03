import datetime


def convert_int_to_bool(val, field_name):
    if not isinstance(val, int):
        raise ValueError
    if val not in {0, 1}:
        raise ValueError
    return bool(val)

def convert_str_to_bool(val):
    if not isinstance(val, str):
        raise TypeError(f'{val} is not a string type.')

    val = val.casefold()
    if val in {'true', 't', '1'}:
        return True
    elif val in {'false', 'f', '0'}:
        return False
    else:
        raise ValueError

def convert_to_bool(val):
    if isinstance(val, bool):
        return val
    try:
        try:
            b = convert_int_to_bool(val)
        except TypeError:
            try:
                b = convert_str_to_bool(val)
            except TypeError:
                raise TypeError
    except ValueError as ex:
        raise ValueError
    else:
        return b

def convert_to_datetime(dt_format, val):
    if val is None:
        return None
    try:
        converted_date = datetime.datetime.strptime(val, dt_format).date()
    except TypeError as ex:
        print(ex)
    except ValueError as ex:
        print(ex)
    else:
        return converted_date

def parse_text_area(val):
    if val is None:
        return 'empty'
    return val

def parse_pay_rate_type(val):
    val = val.casefold()
    if val in {'overtime', 'true'}:
        return 'overtime'
    elif val in {'base', 'false'}:
        return 'base'

def convert_to_int(val):
    if isinstance(val, str):
        if len(val) == 0:
            return 0
        else:
            return int(val)
    if isinstance(val, int):
        return int(val)




