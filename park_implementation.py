from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Car:
    car_length: int
    car_time: int

    def __repr__(self) -> str:
        return f'Car({self.car_length}, {self.car_time})'


@dataclass
class Spot:
    occupant: Optional[Car]
    length: int

    def __len__(self) -> str:
        return self.length

    def __repr__(self) -> str:
        return f'Spot({self.occupant}, {len(self)})'


class Park:
    """
    Class that provides an interface for allocating cars in available slots
    and keeping track of its book-keeping usage.

    A Park instance contains a list of Spot instances. Initially, the park
    contains a single Spot of size park_length. A car can be added to the Park
    as long as there is at least one available Spot of length greater or equal
    to the car's length.

    Usage:
        >>> park = Park(park_length=10)
        >>> repr(park)
        Park(Spot(None, 10))
        >>> park.park_car(car=Car(car_length=2, car_time=2))
        >>> repr(park)
        Park(Spot(Car(2, 2), 2), Spot(None, 8))
        >>> park.report_utilisation()
        0.2
        >>> park.park_car(car=Car(car_length=4, car_time=3))
        >>> repr(park)
        Park(Spot(Car(2, 2), 2), Spot(Car(4, 3), 4), Spot(None, 4))
        >>> park.elapse_period()
        >>> park.elapse_period()
        >>> repr(park)
        Park(Spot(None, 2), Spot(Car(4, 1), 4), Spot(None, 4))
        >>> park.elapse_period()
        >>> repr(park)
        Park(Spot(None, 10))
    """

    def __init__(self, park_length: int) -> None:
        self.park_length: int = park_length
        self.spots: List[Spot] = [Spot(None, self.park_length)]

    def park_car(self, car: Car) -> bool:
        """
        Parks a car following a first fit parking policy.

        The first fit policy was chosen considering the data structure where
        the spots are stored and the anatomy of a Spot object.
        """
        car_parked: bool = False
        for index, spot in enumerate(self.spots):
            if spot.occupant is None and len(spot) >= car.car_length:
                self.spots.insert(index, Spot(car, car.car_length))
                # If empty Spot's length is 0, remove from list.
                if (len(self.spots[index + 1]) - car.car_length) == 0:
                    self.spots.pop(index + 1)
                else:
                    self.spots[index + 1].length -= car.car_length
                car_parked = True
                break
        return car_parked

    def elapse_period(self) -> None:
        index: int = 0
        while index < len(self.spots):
            spot: Spot = self.spots[index]
            if isinstance(spot.occupant, Car):
                spot.occupant.car_time -= 1
                if spot.occupant.car_time == 0:
                    spot.occupant = None  # Remove car from park.
            if spot.occupant is None:
                self.cleanup_empty_spots(
                    spots=self.spots,
                    index=index,
                )
            index += 1

    def report_utilisation(self) -> float:
        if len(self.spots) == 1 and self.spots[0].occupant is None:
            return 0
        empty_slots: int = sum(
            (len(spot) for spot in self.spots if spot.occupant is None)
        )
        return (self.park_length - empty_slots) / self.park_length

    def __repr__(self) -> str:
        """Returns available and occupied spots in the park."""
        rep: str = 'Park('
        for spot in self.spots:
            rep += repr(spot) + ', '
        rep = rep.rstrip(', ') + ')'
        return rep

    @classmethod
    def cleanup_empty_spots(cls, spots: List[Spot], index: int):
        """
        Recursive method to remove the subsequent empty spots while adding up
        its lengths.
        """
        if index < len(spots) - 1:
            spot: Spot = spots[index]
            next_spot: Spot = spots[index + 1]
            # If next spot empty or has a car whose time is over, merge spots.
            if (next_spot.occupant is None
                    or next_spot.occupant.car_time - 1 == 0):
                spot.length += len(next_spot)  # Merge spots' length.
                spots.pop(index + 1)  # Remove car or empty spot from park.
                cls.cleanup_empty_spots(spots=spots, index=index)


def example_usage():
    park = Park(park_length=10)

    print(repr(park))
    print(f' - utilisation: {park.report_utilisation()}')

    park.park_car(car=Car(car_length=2, car_time=2))
    print(repr(park))
    print(f' - utilisation: {park.report_utilisation()}')

    park.park_car(car=Car(car_length=4, car_time=3))
    print(repr(park))
    print(f' - utilisation: {park.report_utilisation()}')

    park.elapse_period()
    park.elapse_period()
    print(repr(park))
    print(f' - utilisation: {park.report_utilisation()}')

    park.elapse_period()
    print(repr(park))
    print(f' - utilisation: {park.report_utilisation()}')


if __name__ == '__main__':
    example_usage()
