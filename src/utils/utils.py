def human_format_to_float(str):
    if "G" in str:
        if str.split("G")[1] != "":
            raise Exception("Invalid format")
        return float(str.split("G")[0]) * 1000000000
    elif "M" in str:
        if str.split("M")[1] != "":
            raise Exception("Invalid format")
        return float(str.split("M")[0]) * 1000000
    elif "K" in str:
        if str.split("K")[1] != "":
            raise Exception("Invalid format")
        return float(str.split("K")[0]) * 1000
    else:
        raise Exception("Invalid format")
    