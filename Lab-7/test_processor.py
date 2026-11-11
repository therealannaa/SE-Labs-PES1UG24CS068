"""
Lab 7 - Fuzz testing processor.py with Hypothesis.

Each function gets:
  1. A "no crash" fuzz test: random text / None must never raise an exception.
  2. A structured fuzz test: inputs shaped like real data (e.g. "AB-CD-3",
     "50/10.0") so Hypothesis reaches the deeper code paths.
  3. A property test: valid inputs must still give the correct answer.

Contract of the hardened processor: on invalid input a function returns None
instead of raising.
"""
import math

from hypothesis import given, settings, strategies as st
from processor import parse_transit_corridor, lookup_concession_discount, compute_passenger_density

VALID_CATEGORIES = {
    "STANDARD": 1.00,
    "STUDENT": 0.50,
    "SENIOR": 0.35,
    "MILITARY": 0.20,
    "CHILD": 0.00,
}

# Strings made of the characters each parser cares about, so the fuzzer
# hits separators, signs, digits and special float words often.
corridor_like = st.text(alphabet="AB09-+ .\t_x", max_size=15)
ratio_like = (
    st.text(alphabet="0123456789./-+eE ", max_size=15)
    | st.tuples(
        st.sampled_from(["50", "-5", "0", "nan", "inf", "-inf", "1e308", "", "abc"]),
        st.sampled_from(["10.0", "0", "-0.0", "nan", "inf", "1e-308", "", "x"]),
    ).map(lambda t: f"{t[0]}/{t[1]}")
)
codes = st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", min_size=1, max_size=5)


# ---------------------------------------------------------------------------
# parse_transit_corridor
# ---------------------------------------------------------------------------
@given(st.text() | st.none())
def test_parse_transit_corridor_no_crash(s):
    try:
        result = parse_transit_corridor(s)
    except Exception as e:
        assert False, f"parse_transit_corridor crashed on {s!r} with: {type(e).__name__}: {e}"
    assert result is None or isinstance(result, str)


@given(corridor_like | st.integers().map(lambda n: f"AB-CD-{n}"))
def test_parse_transit_corridor_structured_no_crash(s):
    try:
        result = parse_transit_corridor(s)
    except Exception as e:
        assert False, f"parse_transit_corridor crashed on {s!r} with: {type(e).__name__}: {e}"
    assert result is None or isinstance(result, str)


@given(codes, codes, st.integers(min_value=1, max_value=100))
def test_parse_transit_corridor_valid(orig, dest, zones):
    result = parse_transit_corridor(f"  {orig}-{dest}-{zones} ")
    fare = 2.50 + zones * 0.75
    assert result == f"Route {orig}->{dest}: {zones} Zones, Fare ${fare:.2f}"


# ---------------------------------------------------------------------------
# lookup_concession_discount
# ---------------------------------------------------------------------------
@given(st.text() | st.none())
def test_lookup_concession_discount_safe(s):
    try:
        result = lookup_concession_discount(s)
    except Exception as e:
        assert False, f"lookup_concession_discount crashed on {s!r} with: {type(e).__name__}: {e}"
    assert result is None or result in VALID_CATEGORIES.values()


@given(st.sampled_from(sorted(VALID_CATEGORIES)), st.sampled_from([str.lower, str.upper, str.title]),
       st.sampled_from(["", " ", "\t"]))
def test_lookup_concession_discount_valid(category, case, pad):
    assert lookup_concession_discount(pad + case(category) + pad) == VALID_CATEGORIES[category]


# ---------------------------------------------------------------------------
# compute_passenger_density
# ---------------------------------------------------------------------------
@given(st.text() | st.none())
def test_compute_passenger_density_safe(s):
    try:
        result = compute_passenger_density(s)
    except Exception as e:
        assert False, f"compute_passenger_density crashed on {s!r} with: {type(e).__name__}: {e}"
    assert result is None or isinstance(result, float)


@settings(max_examples=300)
@given(ratio_like)
def test_compute_passenger_density_structured_safe(s):
    try:
        result = compute_passenger_density(s)
    except Exception as e:
        assert False, f"compute_passenger_density crashed on {s!r} with: {type(e).__name__}: {e}"
    # A density must be a real, non-negative number - never nan / inf / negative.
    assert result is None or (math.isfinite(result) and result >= 0), \
        f"invalid density {result!r} for input {s!r}"


@given(st.integers(min_value=0, max_value=10_000), st.floats(min_value=0.1, max_value=1000))
def test_compute_passenger_density_valid(passengers, km):
    assert compute_passenger_density(f"{passengers}/{km}") == round(passengers / km, 2)
