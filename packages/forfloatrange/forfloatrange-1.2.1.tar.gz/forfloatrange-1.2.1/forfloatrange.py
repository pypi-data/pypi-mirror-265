from decimal import Decimal

def ffrange(*args):
    length = len(args)
    if length == 0 or length > 3:
        raise ValueError("Error: ffrange() takes 1 to 3 arguments.")

    min_val = Decimal(str(args[0])) if length > 0 else Decimal(0)
    max_val = Decimal(str(args[1])) if length > 1 else Decimal(str(args[0]))
    step_val = Decimal(str(args[2])) if length > 2 else Decimal(1)

    if step_val == 0:
        raise ValueError("Error: Step cannot be 0.")

    results = []

    current_val = min_val
    while (step_val > 0 and current_val < max_val+step_val) or (step_val < 0 and current_val > max_val+step_val):
        results.append(current_val)
        current_val += step_val


    return results
