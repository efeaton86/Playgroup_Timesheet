from functools import partial

from .validators import (convert_to_int, convert_to_bool,
                        convert_to_datetime, parse_text_area,
                        parse_pay_rate_type)

field_to_function_parser = {
    'dateRangePickerActive': convert_to_bool,
    'user_id': convert_to_int,
    'date': partial(convert_to_datetime, '%Y-%m-%d'),
    'endDate': partial(convert_to_datetime, '%Y-%m-%d'),
    'hours': convert_to_int,
    'minutes': convert_to_int,
    'comments': parse_text_area,
    'payRate': parse_pay_rate_type,
}


PAY_CYCLE_END_DATE = 25

