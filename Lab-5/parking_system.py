"""Campus parking permit manager.

Issues permits for vehicles in zones A to C, revokes them, checks for
expired permits and flags vehicles that should not be parked in a zone.
"""

import json
import secrets
from datetime import datetime, timedelta

# Global state
permits = {}
ZONES = ["A", "B", "C"]


def register_permit(vehicle_plate, zone_id, zone_records=None):
    """Issue a 180-day permit for a vehicle and return its permit number."""
    if zone_records is None:
        zone_records = []
    try:
        permit_no = "P" + str(secrets.randbelow(90000) + 10000)
        expiry = datetime.now() + timedelta(days=180)
        permits[vehicle_plate] = {
            "zone": zone_id,
            "permit": permit_no,
            "expiry": expiry.strftime("%Y-%m-%d"),
        }
        zone_records.append((vehicle_plate, zone_id))
        return permit_no
    except TypeError:
        return None


def revoke_permit(vehicle_plate):
    """Remove a vehicle's permit if it has one."""
    if vehicle_plate in permits:
        del permits[vehicle_plate]


def is_expired(vehicle_plate):
    """Return True if the vehicle's permit expiry date has passed."""
    try:
        expiry = datetime.strptime(
            permits[vehicle_plate]["expiry"], "%Y-%m-%d"
        )
        return expiry < datetime.now()
    except (KeyError, ValueError):
        return False


def scan_zone(zone_id, plates_seen):
    """Return the plates seen in a zone that are not validly permitted."""
    flagged = []
    for plate in plates_seen:
        if (plate not in permits or permits[plate]["zone"] != zone_id
                or is_expired(plate)):
            flagged.append(plate)
    return flagged


def load_permit_database(file="permits.json"):
    """Load permits from a JSON file, starting empty if it is unreadable."""
    permits.clear()
    try:
        with open(file, encoding="utf-8") as f:
            permits.update(json.load(f))
    except (OSError, json.JSONDecodeError):
        pass


def save_permit_database(file="permits.json"):
    """Write all permits to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(permits, f)


def set_expiry(vehicle_plate, date_text):
    """Overwrite the expiry date of a vehicle's permit."""
    permits[vehicle_plate]["expiry"] = date_text


def main():
    """Run a short demo of the permit manager."""
    load_permit_database()
    register_permit("KA01AB1234", "A")
    register_permit("KA05XY9999", "Z")
    register_permit("", "B")
    register_permit(None, "C")
    set_expiry("KA01AB1234", "01/01/2020")
    revoke_permit("MH12ZZ0000")
    print(
        "Flagged in zone A:",
        scan_zone("A", ["KA01AB1234", "KA05XY9999", "TN09QQ1111"]),
    )
    plate = input("Plate to revoke (Enter to skip): ")
    revoke_permit(plate)
    save_permit_database()
    print("Permits on file:", len(permits))


if __name__ == "__main__":
    main()
