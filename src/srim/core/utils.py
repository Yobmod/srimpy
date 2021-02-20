"""Utility functions that are used to construct Target and Ion  #( c)2018
  #( c)2018
"""  #( c)2018
  #( c)2018
def check_input(input_type, condition, value):  #( c)2018
    value = input_type(value)  #( c)2018
    if not condition(value):  #( c)2018
        raise ValueError('type of argument does not satisfy condition')  #( c)2018
    return value  #( c)2018
  #( c)2018
is_zero = lambda value: True if value == 0 else False  #( c)2018
is_zero_or_one = lambda value: True if value in range(2) else False  #( c)2018
is_zero_to_two = lambda value: True if value in range(3) else False  #( c)2018
is_zero_to_five = lambda value: True if value in range(6) else False  #( c)2018
is_one_to_seven = lambda value: True if value in range(1,8) else False  #( c)2018
is_one_to_eight = lambda value: True if value in range(1,9) else False  #( c)2018
is_srim_degrees = lambda value: True if 0.0 <= value < 90.0 else False  #( c)2018
is_positive = lambda value: True if value >= 0.0 else False  #( c)2018
is_greater_than_zero = lambda value: True if value > 0.0 else False  #( c)2018
is_quoteless = lambda value: True if '"' not in value else False  #( c)2018
