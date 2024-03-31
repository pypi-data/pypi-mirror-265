import pytest
from am4.utils.aircraft import Aircraft
from am4.utils.game import User


@pytest.mark.parametrize("inp", ["id:1", "shortname:b744", "name:B747-400"])
def test_aircraft_search(inp):
    a0 = Aircraft.search(inp)
    assert a0.ac.valid
    assert a0.ac.shortname == "b744"


@pytest.mark.parametrize("inp", ["b7440", "shortname:b7440" "name:B747-4000"])
def test_aircraft_fail_and_suggest(inp):
    a0 = Aircraft.search(inp)
    assert not a0.ac.valid
    suggs = Aircraft.suggest(a0.parse_result)
    assert suggs[0].ac.shortname == "b744"


@pytest.mark.parametrize("inp", ["74sp", "id:335a"])
def test_aircraft_stoi_trailing(inp):
    a0 = Aircraft.search(inp)
    assert not a0.ac.valid


@pytest.mark.parametrize("inp", ["65590", "id:65590"])
def test_aircraft_stoi_overflow(inp):
    a0 = Aircraft.search(inp)
    assert not a0.ac.valid


@pytest.mark.parametrize(
    "inp",
    [
        "b744[sfcx]",
        "b744[s,fc,x]",
        "b744[sf,cx]",
        "b744[s,f,cx]",
        "b744[s, f, cx]",
        "b744[ , s, f,, c,,,  x,,x,xx]",
        "id:1[sfcx]",
        "shortname:b744[sfcx]",
        "name:B747-400[sfcx]",
    ],
)
def test_aircraft_modifiers_syntax(inp):
    a0 = Aircraft.search(inp)
    assert a0.ac.shortname == "b744"
    assert a0.parse_result.speed_mod is True
    assert a0.ac.speed_mod is True
    assert a0.parse_result.fuel_mod is True
    assert a0.ac.fuel_mod is True
    assert a0.parse_result.co2_mod is True
    assert a0.ac.co2_mod is True
    assert a0.parse_result.fourx_mod is True
    assert a0.ac.fourx_mod is True


def test_aircraft_engine_modifier():
    a = Aircraft.search("b744")
    a0 = Aircraft.search("b744[0]")
    a1 = Aircraft.search("b744[1]")
    a1sfc = Aircraft.search("b744[1,sfc]")
    assert a0.ac.id == a1.ac.id == a.ac.id == 1
    assert a0.ac.eid == a.ac.eid == 4
    assert a1.ac.eid == 2
    assert a1.ac.fuel == pytest.approx(21.21)
    assert a1.ac.co2 == pytest.approx(0.18)
    assert a1sfc.ac.speed / a1.ac.speed == pytest.approx(1.1)
    assert a1sfc.ac.fuel / a1.ac.fuel == pytest.approx(0.9)
    assert a1sfc.ac.co2 / a1.ac.co2 == pytest.approx(0.9)


def test_aircraft_fourx():
    a0 = Aircraft.search("b744").ac
    user = User.Default()
    user.fourx = True
    a1 = Aircraft.search("b744", user=user).ac
    assert a1.speed / a0.speed == pytest.approx(4.0)
