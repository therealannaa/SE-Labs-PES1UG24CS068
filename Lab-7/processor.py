import math

MAX_ZONES = 100

CONCESSION_DISCOUNTS = {
    "STANDARD": 1.00,
    "STUDENT": 0.50,
    "SENIOR": 0.35,
    "MILITARY": 0.20,
    "CHILD": 0.00
}


def parse_transit_corridor(corridor_code):
    """Parse 'ORIG-DEST-ZONES'. Returns a description string, or None if invalid."""
    # Bug fix: None / non-string input crashed on .strip()
    if not isinstance(corridor_code, str):
        return None

    parts = corridor_code.strip().split('-')
    # Bug fix: wrong number of '-' separated parts crashed the tuple unpacking
    if len(parts) != 3:
        return None
    orig, dest, zones_str = (p.strip() for p in parts)

    # Bug fix: empty / non-alphanumeric station codes were accepted
    if not (orig.isascii() and orig.isalnum() and dest.isascii() and dest.isalnum()):
        return None

    # Bug fix: non-numeric zones crashed int(); only plain ASCII digits allowed
    if not (zones_str.isascii() and zones_str.isdigit()):
        return None
    zones = int(zones_str)

    # Bug fix: zero zones and huge zone counts (float overflow) were accepted
    if zones < 1 or zones > MAX_ZONES:
        return None

    base_fare = 2.50 + (zones * 0.75)
    return f"Route {orig.upper()}->{dest.upper()}: {zones} Zones, Fare ${base_fare:.2f}"


def lookup_concession_discount(category_name):
    """Return the fare multiplier for a category, or None if the category is unknown."""
    # Bug fix: None / non-string input crashed on .strip()
    if not isinstance(category_name, str):
        return None
    category = category_name.strip()
    # Bug fix: non-ASCII look-alikes (e.g. 'ſtudent'.upper() == 'STUDENT') are rejected
    if not category.isascii():
        return None
    # Bug fix: unknown category raised KeyError
    return CONCESSION_DISCOUNTS.get(category.upper())


def compute_passenger_density(occupancy_ratio_str):
    """Compute passengers per km from 'PASSENGERS/KM'. Returns a float, or None if invalid."""
    # Bug fix: None / non-string input crashed on .split()
    if not isinstance(occupancy_ratio_str, str):
        return None

    parts = occupancy_ratio_str.split('/')
    # Bug fix: missing or extra '/' crashed the tuple unpacking
    if len(parts) != 2:
        return None

    # Bug fix: empty or non-numeric values crashed float()
    try:
        passengers = float(parts[0])
        km = float(parts[1])
    except ValueError:
        return None

    # Bug fix: nan / inf were accepted
    if not (math.isfinite(passengers) and math.isfinite(km)):
        return None
    # Bug fix: km == 0 raised ZeroDivisionError; negative values gave negative density
    if passengers < 0 or km <= 0:
        return None

    density = passengers / km
    # Bug fix: very large / very small values overflowed to inf
    if not math.isfinite(density):
        return None
    return round(density, 2)


def main():
    print("==== Running parse_transit_corridor ====")
    c_input = input("Enter corridor (e.g. DT-UP-3): ")
    result = parse_transit_corridor(c_input)
    print(result if result is not None else "Invalid corridor code. Expected format ORIG-DEST-ZONES, e.g. DT-UP-3")

    print("\n==== Running lookup_concession_discount ====")
    cat_input = input("Enter concession category (e.g. STUDENT, SENIOR): ")
    multiplier = lookup_concession_discount(cat_input)
    if multiplier is not None:
        print("Multiplier:", multiplier)
    else:
        print("Unknown concession category. Valid:", ", ".join(CONCESSION_DISCOUNTS))

    print("\n==== Running compute_passenger_density ====")
    d_input = input("Enter passengers/km (e.g. 50/10.0): ")
    density = compute_passenger_density(d_input)
    if density is not None:
        print("Density:", density)
    else:
        print("Invalid input. Expected PASSENGERS/KM with passengers >= 0 and km > 0, e.g. 50/10.0")


if __name__ == "__main__":
    main()
