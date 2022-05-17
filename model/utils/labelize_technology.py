import validate


def labelize_technology(key, *, capitalize=True):
    """
    Return the label for a specific technology key
    """
    assert validate.is_technology(key)
    assert validate.is_bool(capitalize)

    if key == "pv":
        label = "solar PV"
    if key == "onshore":
        label = "onshore wind"
    if key == "offshore":
        label = "offshore wind"
    if key == "lion":
        label = "Li-ion"
    if key == "hydrogen":
        label = "hydrogen"

    return (label[0].upper() + label[1:]) if capitalize else label
