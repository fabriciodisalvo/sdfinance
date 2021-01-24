def format_amount_view_expense(amount):
    amount = float(amount) * -1
    formatted_float = "${:,}".format(int(amount // 1))
    formatted_decimals = "{00}".format(int(round(float(amount) % 1, 2) * 100))
    return formatted_float, formatted_decimals
