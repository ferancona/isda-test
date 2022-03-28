import pytest

from park_implementation import Car, Park, Spot


@pytest.fixture
def length1() -> int:
    return 2


@pytest.fixture
def time1() -> int:
    return 2


@pytest.fixture
def car1(length1, time1) -> Car:
    return Car(
        car_length=length1,
        car_time=time1,
    )


@pytest.fixture
def car1_repr(length1, time1) -> str:
    return f'Car({length1}, {time1})'


@pytest.fixture
def length2() -> int:
    return 4


@pytest.fixture
def time2() -> int:
    return 3


@pytest.fixture
def car2(length2, time2) -> Car:
    return Car(
        car_length=length2,
        car_time=time2,
    )


@pytest.fixture
def car2_repr(length2, time2) -> str:
    return f'Car({length2}, {time2})'


@pytest.fixture
def length3() -> int:
    return 4


@pytest.fixture
def time3() -> int:
    return 5


@pytest.fixture
def car3(length3, time3) -> Car:
    return Car(
        car_length=length3,
        car_time=time3,
    )


@pytest.fixture
def car3_repr(length3, time3) -> str:
    return f'Car({length3}, {time3})'


@pytest.fixture
def spot1(car1) -> Spot:
    return Spot(car1, car1.car_length)


@pytest.fixture
def spot2(car2) -> Spot:
    return Spot(car2, car2.car_length)


@pytest.fixture
def spot3(car3) -> Spot:
    return Spot(car3, car3.car_length)


@pytest.fixture
def spot1_repr(car1_repr, length1) -> str:
    return f'Spot({car1_repr}, {length1})'


@pytest.fixture
def spot2_repr(car2_repr, length2) -> str:
    return f'Spot({car2_repr}, {length2})'


@pytest.fixture
def spot3_repr(car3_repr, length3) -> str:
    return f'Spot({car3_repr}, {length3})'


class TestCar:
    def test_repr(self, car1, car1_repr):
        assert repr(car1) == car1_repr


class TestSpot:
    def test_repr_with_occupant(self, spot1, spot1_repr):
        assert repr(spot1) == spot1_repr

    def test_repr_without_occupant(self):
        spot_length = 1
        spot = Spot(None, spot_length)
        expected_repr = f'Spot(None, {spot_length})'
        assert repr(spot) == expected_repr


class TestPark:
    @pytest.fixture
    def park_length(self) -> int:
        return 10

    @pytest.fixture
    def empty_park(self, park_length) -> Park:
        return Park(park_length=park_length)

    @pytest.fixture
    def full_park(self, empty_park, car1, car2, car3) -> Park:
        park = empty_park
        park.park_car(car1)
        park.park_car(car2)
        park.park_car(car3)
        return park

    def test_park_car_empty(self, empty_park, car1):
        res = empty_park.park_car(car1)
        car1_in_park = len(
            [spot for spot in empty_park.spots
             if spot.occupant is car1]
        ) == 1
        assert res is True and car1_in_park

    def test_park_car_not_enough_space(self, full_park, park_length):
        happy_car = Car(park_length + 1, 1)
        res = full_park.park_car(happy_car)
        happy_car_in_park = len(
            [spot for spot in full_park.spots
             if spot.occupant is happy_car]
        ) == 1
        assert not res and not happy_car_in_park

    def test_elapse_period_car_removed(self, full_park, car1):
        for _ in range(car1.car_time):
            full_park.elapse_period()
        car1_in_park = len(
            [spot for spot in full_park.spots
             if spot.occupant is car1]
        ) == 1
        assert not car1_in_park

    def test_elapse_period_no_cars_removed(self, full_park, car1, car2, car3):
        car_times = [car1.car_time, car2.car_time, car3.car_time]
        for _ in range(min(car_times) - 1):
            full_park.elapse_period()
        cars_in_park = len(
            [spot for spot in full_park.spots
             if spot.occupant in (car1, car2, car3)]
        ) == 3
        assert cars_in_park

    def test_elapse_period_empty_spots_cleaup(
            self, empty_park, car1, car2, park_length):
        park = empty_park
        park.park_car(car1)
        park.park_car(car2)
        max_time = max(
            (spot.occupant.car_time for spot in park.spots
             if spot.occupant is not None)
        )
        for _ in range(max_time):
            park.elapse_period()
        assert (
            len(park.spots) == 1
            and park.spots[0].occupant is None
            and park.spots[0].length == park_length
        )

    def test_report_utilisation_empty(self, empty_park):
        assert empty_park.report_utilisation() == 0

    def test_report_utilisation_full(self, full_park):
        assert full_park.report_utilisation() == 1

    def test_report_utilisation_fraction(self, empty_park, car1, park_length):
        park = empty_park
        park.park_car(car1)
        assert park.report_utilisation() == (car1.car_length / park_length)

    def test_repr_empty(self, empty_park, park_length):
        assert repr(empty_park) == f'Park(Spot(None, {park_length}))'

    def test_repr_full(self, full_park, spot1_repr, spot2_repr, spot3_repr):
        expected = f'Park({spot1_repr}, {spot2_repr}, {spot3_repr})'
        assert repr(full_park) == expected

    def test_repr_one_car(self, empty_park, car1, spot1_repr, park_length):
        park = empty_park
        park.park_car(car1)
        remaining_spot_repr = f'Spot(None, {park_length - car1.car_length})'
        expected = f'Park({spot1_repr}, {remaining_spot_repr})'
        assert repr(park) == expected
