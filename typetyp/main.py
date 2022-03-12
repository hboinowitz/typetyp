from typing import Callable, Dict
import typing

def parse_single_typehint(typehint):
    description = ""
    if getattr(typehint, '__module__', None) == typing.__name__:
        try: 
            type_str = typing.get_origin(typehint).__name__
            description += type_str
        except AttributeError:
            type_str = str(typing.get_origin(typehint))
        if type_str in ['list', 'tuple']:
            subtype = typing.get_args(typehint)[0]
            description += f' of {parse_single_typehint(subtype)}'
        elif type_str == 'dict':
            key_subtype, value_subtype = typing.get_args(typehint)
            if len(typing.get_args(typehint)) != 2:
                raise ValueError('Dict accepts two arguments')
            description += (
                f' mapping a {parse_single_typehint(key_subtype)} to a {parse_single_typehint(value_subtype)}'
            )
        elif type_str == 'typing.Union': 
            if str(typing.get_args(typehint)[1]) == "<class 'NoneType'>":
                subtype = typing.get_args(typehint)[0]
                description += f'optional {parse_single_typehint(subtype)}'
            else:
                num_subtypes = len(typing.get_args(typehint))
                for idx, subtype in enumerate(typing.get_args(typehint)):
                    description += parse_single_typehint(subtype)
                    if idx == num_subtypes - 2:
                        description += " or "
                    elif idx != num_subtypes - 1:
                        description += ", "
        return description
    else:
        description += typehint.__name__
        return description

def parse_type_hints(type_hints: Dict[str, typing.Type]):
    descriptions = {}
    for key, val in type_hints.items():
        parsed_typehint = parse_single_typehint(val)
        if key == 'return':
            if parsed_typehint.startswith('o') or parsed_typehint.startswith('i'):
                descriptions[key] = f"an {parse_single_typehint(val)}"
            else:
                descriptions[key] = f"a {parse_single_typehint(val)}"
            continue
        if parsed_typehint.startswith('o') or parsed_typehint.startswith('i'):
            descriptions[key] = f"`{key}` is an {parse_single_typehint(val)}"
        else:
            descriptions[key] = f"`{key}` is a {parse_single_typehint(val)}"

    return descriptions

def typetyps(func: Callable):
    narration = ""
    parsed_type_hints = parse_type_hints(typing.get_type_hints(func))
    num_accepted_parameters = len(parsed_type_hints.values())
    if 'return' in parsed_type_hints.keys():
        num_accepted_parameters -= 1
    parameters = ""
    for i in range(num_accepted_parameters):
        parameters += f"`{list(parsed_type_hints.keys())[i]}`"
        if i == num_accepted_parameters - 2:
             parameters += " and "
        elif i != num_accepted_parameters - 1:
            parameters += ", "
    
    descriptions = ""
    for i in range(num_accepted_parameters):
        descriptions += list(parsed_type_hints.values())[i]
        if i == num_accepted_parameters - 2:
             descriptions += " and "
        elif i != num_accepted_parameters - 1:
            descriptions += ", "

    narration += (
        f"`{func.__name__}` is a function accepting {num_accepted_parameters} {'parameters' if num_accepted_parameters > 1 else 'parameter'} {parameters} -  {descriptions}."
    )
    if 'return' in parsed_type_hints.keys():
        narration += f"`{func.__name__}` returns {parsed_type_hints['return']}"
    return narration