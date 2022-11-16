from typing import Union


def check_type(data: dict, name: str, types: list):
    """
    Check data types contained within a dictionary is one of a list of types.

    Args:
        data: The dictionary
        name: The name of the key of the item to check
        types: A list of types that the item must belong to
    """
    if None in types and data[name] is None:
        return
    if type(data[name]) not in types:
        raise ValueError(
            "'" + name + "' needs to be of type: " + " or ".join(map(str, types))
        )


def check_within_range(
    data: dict,
    name: str,
    lower: Union[None, float],
    upper: Union[None, float],
    l_inclusive: bool,
    u_inclusive: bool,
):
    """
    Check that an item belonging to a dictionary fits within a certain numerical range (either inclusive or not).

    If upper or lower are None then ignores that direction.

    Args:
        data: The dictionary where the item is held
        name: The name of the key that corresponds to the item
        lower: The lower bound for the range (None means no lower bound)
        upper: The upper bound for the range (None means no upper bound)
        l_inclusive: Boolean - True for inclusive, False for not
        u_inclusive: Boolean - True for inclusive, False for not
    """
    if lower is not None:
        if l_inclusive is False:
            if data[name] <= lower:
                raise ValueError(
                    "'"
                    + name
                    + "' Needs to have a value greater than: "
                    + str(lower)
                    + " (not inclusive)"
                )
        else:
            if data[name] < lower:
                raise ValueError(
                    "'"
                    + name
                    + "' Needs to have a value greater than: "
                    + str(lower)
                    + " (inclusive)"
                )
    if upper is not None:
        if u_inclusive is False:
            if data[name] >= upper:
                raise ValueError(
                    "'"
                    + name
                    + "' Needs to have a value less than: "
                    + str(upper)
                    + " (not inclusive)"
                )
        else:
            if data[name] > upper:
                raise ValueError(
                    "'"
                    + name
                    + "' Needs to have a value less than: "
                    + str(upper)
                    + " (inclusive)"
                )
