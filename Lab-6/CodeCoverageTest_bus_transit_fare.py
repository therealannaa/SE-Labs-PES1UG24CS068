"""Lab 6 - Code (line) coverage tests for bus_transit_fare.py.

Goal: execute every line of the module at least once.
Run:  coverage run -m pytest CodeCoverageTest_bus_transit_fare.py
      coverage report -m
"""
import pytest
from bus_transit_fare import process_commute_manifest, inspect_smartcard_turnstiles


def test_single_regular_local_ride():
    manifests = [{
        "route_active": True, "route_type": "local", "priority_boarding": False,
        "commuters": [{"zones": 2, "type": "regular", "blacklisted": False}],
    }]
    result = process_commute_manifest(manifests, 2.0)
    assert result["total_fare"] == 4.5
    assert result["status"] == "COMPLETED"


def test_invalid_input_raises():
    with pytest.raises(ValueError):
        process_commute_manifest("not a list", 1.0)


def test_inactive_route_is_skipped():
    result = process_commute_manifest([{"route_active": False}], 1.0)
    assert result == {"total_fare": 0.0, "status": "ZERO_RIDERSHIP"}


def test_express_mixed_passengers_with_priority_boarding():
    # student 3.5 + senior 4.9 + regular 8.0 = 16.4, zones=0 rejected, +2.0 fee
    manifests = [{
        "route_active": True, "route_type": "express", "priority_boarding": True,
        "commuters": [
            {"zones": 2, "type": "student"},
            {"zones": 2, "type": "senior"},
            {"zones": 2, "type": "regular"},
            {"zones": 0, "type": "regular"},
        ],
    }]
    result = process_commute_manifest(manifests, 2.0)
    assert result["total_fare"] == pytest.approx(18.4)
    assert result["status"] == "COMPLETED"


def test_shuttle_route_fare():
    manifests = [{
        "route_active": True, "route_type": "shuttle",
        "commuters": [{"zones": 2, "type": "regular"}],
    }]
    assert process_commute_manifest(manifests, 0)["total_fare"] == 6.0


def test_unknown_route_type_rejected():
    result = process_commute_manifest([{"route_active": True, "route_type": "ferry"}], 1.0)
    assert result["status"] == "ZERO_RIDERSHIP"


def test_blacklisted_card_on_express_and_local():
    manifests = [
        {"route_active": True, "route_type": "express",
         "commuters": [{"zones": 1, "blacklisted": True}]},
        {"route_active": True, "route_type": "local",
         "commuters": [{"zones": 1, "blacklisted": True}]},
    ]
    result = process_commute_manifest(manifests, 1.0)
    assert result == {"total_fare": 0.0, "status": "ZERO_RIDERSHIP"}


def test_audit_rejected_when_more_than_four_rejections():
    manifests = [{
        "route_active": True, "route_type": "local",
        "commuters": [{"zones": 0}] * 5 + [{"zones": 1, "type": "regular"}],
    }]
    result = process_commute_manifest(manifests, 1.0)
    assert result == {"total_fare": 3.5, "status": "AUDIT_REJECTED"}


def test_turnstiles_no_data():
    assert inspect_smartcard_turnstiles([]) == "NO_DATA"


def test_turnstiles_jam():
    assert inspect_smartcard_turnstiles([[0, 4, 5]]) == "TURNSTILE_JAM"


def test_turnstiles_operational():
    assert inspect_smartcard_turnstiles([[0, 4, 0, 1]]) == "OPERATIONAL"
