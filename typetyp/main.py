from typing import Callable, Dict
import typing

long_forms = {
    "str": "string",
    "int": "integer",
    "bool": "boolean",
    "dict": "dictionary",
}


def parse_single_typehint(typehint, plural_form=False):
    description = ""
    if getattr(typehint, "__module__", None) == typing.__name__:
        try:
            type_str = typing.get_origin(typehint).__name__
            if type_str in long_forms.keys():
                description += long_forms[type_str]
            else:
                description += type_str
            if plural_form:
                description += "s"
        except AttributeError:
            type_str = str(typing.get_origin(typehint))
        if type_str in ["list", "tuple"]:
            subtype = typing.get_args(typehint)[0]
            description += f" of {parse_single_typehint(subtype, True)}"
        elif type_str == "dict":
            key_subtype, value_subtype = typing.get_args(typehint)
            if len(typing.get_args(typehint)) != 2:
                raise ValueError("Dict accepts two arguments")
            if not plural_form:
                description += f" mapping a {parse_single_typehint(key_subtype, plural_form)} to a {parse_single_typehint(value_subtype, plural_form)}"
            else:
                description += f" mapping {parse_single_typehint(key_subtype, plural_form)} to {parse_single_typehint(value_subtype, plural_form)}"
        elif type_str == "typing.Union":
            if str(typing.get_args(typehint)[1]) == "<class 'NoneType'>":
                subtype = typing.get_args(typehint)[0]
                description += f"optional {parse_single_typehint(subtype, plural_form)}"
            else:
                num_subtypes = len(typing.get_args(typehint))
                for idx, subtype in enumerate(typing.get_args(typehint)):
                    description += parse_single_typehint(subtype, plural_form)
                    if idx == num_subtypes - 2:
                        description += " or "
                    elif idx != num_subtypes - 1:
                        description += ", "
        return description
    else:
        if typehint.__name__ in long_forms.keys():
            description += long_forms[typehint.__name__]
        else:
            description += typehint.__name__
        if plural_form:
            description += "s"
        return description


def parse_type_hints(type_hints: Dict[str, typing.Type]):
    descriptions = {}
    for key, val in type_hints.items():
        parsed_typehint = parse_single_typehint(val)
        descriptions[key] = ""
        if key != "return":
            descriptions[key] = f"`{key}` is "
        descriptions[key] += (
            f"{'an' if parsed_typehint.startswith(('a', 'o', 'i')) else 'a'} "
            f"{parsed_typehint}"
        )

    return descriptions


def typetyps(func: Callable):
    parsed_type_hints = parse_type_hints(typing.get_type_hints(func))
    cleaned_parsed_typehints = {
        param: parsed
        for param, parsed in parsed_type_hints.items()
        if param != "return"
    }

    cleaned_parameters = list(
        map(lambda x: f"`{x}`", list(cleaned_parsed_typehints.keys()))
    )
    cleaned_descriptions = list(cleaned_parsed_typehints.values())
    num_accepted_parameters = len(cleaned_parameters)

    if num_accepted_parameters:
        parameters = ""
        descriptions = ""
        if num_accepted_parameters > 1:
            parameters += f"{', '.join(cleaned_parameters[:-1])} and "
            descriptions += f"{', '.join(cleaned_descriptions[:-1])} and "
        parameters += cleaned_parameters[-1]
        descriptions += cleaned_descriptions[-1]

        narration = (
            f"`{func.__name__}` is a function accepting {num_accepted_parameters} "
            f"{'parameters' if num_accepted_parameters > 1 else 'parameter'} {parameters} -\n"
            f"{descriptions}."
        )
        if "return" in parsed_type_hints.keys():
            narration += f"\n`{func.__name__}` returns {parsed_type_hints['return']}."
    elif "return" in parsed_type_hints.keys():
        narration = (
            f"`{func.__name__}` is a function returning {parsed_type_hints['return']}.\n"
            f"It does not accept any parameters."
        )
    else:
        narration = (
             f"`{func.__name__}` is a function that is neither returning nor accepting any parameters."
        )
    return narration
