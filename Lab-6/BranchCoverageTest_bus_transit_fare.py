"""Lab 6 - Branch coverage tests for bus_transit_fare.py.

Every decision is exercised for both its True and False outcome, including
boundary values (booking_fee == 0, zones == 0, rejected == 4 vs 5, failures == 3).
Run:  coverage run --branch -m pytest BranchCoverageTest_bus_transit_fare.py
      coverage report -m
"""
import pytest
from bus_transit_fare import process_commute_manifest, inspect_smartcard_turnstiles


def ride(route_type="local", commuters=None, active=True, priority=False):
    return {"route_active": active, "route_type": route_type,
            "priority_boarding": priority,
            "commuters": commuters if commuters is not None else []}


# ---- input validation (line 2: `not list` OR `fee < 0`) ----
def test_valid_input_does_not_raise():
    assert process_commute_manifest([], 0)["status"] == "ZERO_RIDERSHIP"

def test_non_list_raises():
    with pytest.raises(ValueError):
        process_commute_manifest({}, 1.0)

def test_negative_fee_raises():
    with pytest.raises(ValueError):
        process_commute_manifest([], -0.01)


# ---- route_active True / False ----
def test_inactive_route_skipped_active_route_counted():
    m = [ride(active=False, commuters=[{"zones": 1}]),
         ride(commuters=[{"zones": 1}])]
    assert process_commute_manifest(m, 0)["total_fare"] == 3.5

def test_missing_route_active_defaults_to_inactive():
    assert process_commute_manifest([{"route_type": "local"}], 0)["status"] == "ZERO_RIDERSHIP"


# ---- route_type: express / shuttle / local / unknown ----
@pytest.mark.parametrize("rtype,expected", [("express", 8.0), ("shuttle", 6.0), ("local", 4.5)])
def test_base_seat_per_route_type(rtype, expected):
    m = [ride(rtype, [{"zones": 2, "type": "regular"}])]
    assert process_commute_manifest(m, 0)["total_fare"] == expected

def test_unknown_route_type_counts_as_rejection_and_skips_commuters():
    m = [ride("ferry", [{"zones": 1}])]
    assert process_commute_manifest(m, 0) == {"total_fare": 0.0, "status": "ZERO_RIDERSHIP"}

def test_default_route_type_is_local():
    m = [{"route_active": True, "commuters": [{"zones": 2}]}]
    assert process_commute_manifest(m, 0)["total_fare"] == 4.5


# ---- commuters loop: empty / non-empty ----
def test_route_with_no_commuters():
    assert process_commute_manifest([ride()], 0)["status"] == "ZERO_RIDERSHIP"


# ---- zones <= 0: True (0, negative) / False (1) ----
@pytest.mark.parametrize("zones", [0, -1])
def test_non_positive_zones_rejected(zones):
    assert process_commute_manifest([ride(commuters=[{"zones": zones}])], 0)["status"] == "ZERO_RIDERSHIP"

def test_one_zone_is_valid_boundary():
    assert process_commute_manifest([ride(commuters=[{"zones": 1}])], 0)["total_fare"] == 3.5


# ---- blacklisted: True/False, express (break) vs non-express ----
def test_blacklisted_on_express_breaks_and_zeroes_fare():
    m = [ride("express", [{"zones": 1}, {"zones": 1, "blacklisted": True}, {"zones": 1}])]
    assert process_commute_manifest(m, 0)["status"] == "ZERO_RIDERSHIP"

@pytest.mark.parametrize("rtype", ["shuttle", "local"])
def test_blacklisted_on_non_express_continues_with_next_commuter(rtype):
    m = [ride(rtype, [{"zones": 1, "blacklisted": True}, {"zones": 2}])]
    base = {"shuttle": 4.0, "local": 2.5}[rtype]
    assert process_commute_manifest(m, 0)["total_fare"] == pytest.approx(base + 2)

def test_blacklisted_express_still_adds_priority_fee():
    m = [ride("express", [{"zones": 1, "blacklisted": True}], priority=True)]
    r = process_commute_manifest(m, 2.0)
    assert r == {"total_fare": 2.0, "status": "COMPLETED"}


# ---- passenger type: student / senior / regular / unknown ----
def test_student_discount():
    assert process_commute_manifest([ride(commuters=[{"zones": 2, "type": "student"}])], 0)["total_fare"] == 1.75

def test_senior_discount():
    assert process_commute_manifest([ride(commuters=[{"zones": 2, "type": "senior"}])], 0)["total_fare"] == pytest.approx(2.45, abs=0.01)

def test_regular_and_unknown_type_pay_full_fare():
    m = [ride(commuters=[{"zones": 2, "type": "regular"}, {"zones": 2, "type": "tourist"}])]
    assert process_commute_manifest(m, 0)["total_fare"] == 9.0


# ---- priority_boarding True / False ----
def test_priority_boarding_adds_fee_once_per_manifest():
    m = [ride(commuters=[{"zones": 2}, {"zones": 2}], priority=True)]
    assert process_commute_manifest(m, 1.5)["total_fare"] == 10.5

def test_no_priority_boarding_no_fee():
    m = [ride(commuters=[{"zones": 2}])]
    assert process_commute_manifest(m, 1.5)["total_fare"] == 4.5

def test_priority_fee_with_zero_fee_boundary():
    assert process_commute_manifest([ride(commuters=[{"zones": 2}], priority=True)], 0)["total_fare"] == 4.5


# ---- final status: rejected > 4, total == 0, completed ----
def test_four_rejections_is_not_audit():
    m = [ride(commuters=[{"zones": 0}] * 4 + [{"zones": 1}])]
    assert process_commute_manifest(m, 0)["status"] == "COMPLETED"

def test_five_rejections_is_audit_rejected():
    m = [ride(commuters=[{"zones": 0}] * 5 + [{"zones": 1}])]
    assert process_commute_manifest(m, 0) == {"total_fare": 3.5, "status": "AUDIT_REJECTED"}

def test_audit_takes_priority_over_zero_ridership():
    m = [ride(commuters=[{"zones": 0}] * 5)]
    assert process_commute_manifest(m, 0) == {"total_fare": 0.0, "status": "AUDIT_REJECTED"}

def test_zero_ridership():
    assert process_commute_manifest([ride()], 0) == {"total_fare": 0.0, "status": "ZERO_RIDERSHIP"}

def test_completed_rounds_to_two_decimals():
    m = [ride("express", [{"zones": 1, "type": "senior"}])]
    assert process_commute_manifest(m, 0)["total_fare"] == round(6.5 * 0.7, 2)


# ---- inspect_smartcard_turnstiles ----
@pytest.mark.parametrize("matrix", [[], None])
def test_no_data(matrix):
    assert inspect_smartcard_turnstiles(matrix) == "NO_DATA"

def test_two_consecutive_failures_jam():
    assert inspect_smartcard_turnstiles([[4, 4]]) == "TURNSTILE_JAM"

def test_failures_equal_to_threshold_are_not_failures():
    assert inspect_smartcard_turnstiles([[3, 3, 3]]) == "OPERATIONAL"

def test_single_failure_not_jam():
    assert inspect_smartcard_turnstiles([[9]]) == "OPERATIONAL"

def test_streak_reset_by_good_reading():
    assert inspect_smartcard_turnstiles([[4, 0, 4, 0, 4]]) == "OPERATIONAL"

def test_streak_does_not_carry_across_devices():
    assert inspect_smartcard_turnstiles([[0, 4], [4, 0]]) == "OPERATIONAL"

def test_jam_found_on_later_device():
    assert inspect_smartcard_turnstiles([[0, 0], [1, 5, 6]]) == "TURNSTILE_JAM"

def test_empty_device_readings():
    assert inspect_smartcard_turnstiles([[], []]) == "OPERATIONAL"
