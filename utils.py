def calculate_total(quantity, rate_per_unit, tax_percentage):
    sub_total = quantity * rate_per_unit
    tax_amount = sub_total * (tax_percentage / 100)
    total_rate = sub_total + tax_amount
    return sub_total, tax_amount, total_rate