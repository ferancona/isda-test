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

    def __repr__(self) -> str:
        return f'Spot({self.occupant}, {self.length})'


class Park:
    """
    Class that provides an interface for allocating cars in available slots
    and keeping track of its book-keeping usage.
    
    A Park instance will contain a list of Spot instances. Initially, the park
    will contain a single Spot of size park_length. A car can be added as long
    as there is at least one available Spot of size greater or equal to the 
    car's size.
    
    Usage:
        >>> park = Park(park_length=10)
        >>> repr(park)
        Park(Spot(None, 10))
        >>> park.park_car(car=Car(car_length=2, car_time=2))
        >>> repr(park)
        Park(Spot(Car(2, 2), 2), Spot(None, 8))
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
        car_parked: bool = False
        for index, spot in enumerate(self.spots):
            if spot.occupant is None and spot.length >= car.car_length:
                self.spots.insert(index, Spot(car, car.car_length))
                # If empty Spot's length is 0, remove from list.
                if (self.spots[index + 1].length - car.car_length) == 0:
                    self.spots.pop(index + 1)
                else:
                    self.spots[index + 1].length -= car.car_length
                car_parked = True
                break
        return car_parked

    def elapse_period(self) -> None:
        last_spot: Spot = self.spots[-1]
        if isinstance(last_spot.occupant, Car):
            last_spot.occupant.car_time -= 1
            if last_spot.occupant.car_time == 0:
                last_spot.occupant = None

        # for index, spot in enumerate(self.spots[:-1]):
        index = 0
        while index < len(self.spots):
            spot = self.spots[index]
            if isinstance(spot.occupant, Car):
                spot.occupant.car_time -= 1
                if spot.occupant.car_time == 0:
                    spot.occupant = None

            if spot.occupant is None:
                next_spot = self.spots[index + 1]
                if (next_spot.occupant is None 
                        or next_spot.occupant.car_time - 1 == 0):
                    spot.length += next_spot.length
                    self.spots.pop(index + 1)
            index += 1

    def report_utilisation(self) -> float:
        if len(self.spots) == 1 and self.spots[0].occupant is None:
            return 0
        empty_slots: int = sum(
            (spot.length for spot in self.spots if spot.occupant is None)
        )
        return (self.park_length - empty_slots) / self.park_length

    def __repr__(self) -> str:
        """Returns available and occupied spots in the park."""
        rep: str = 'Park('
        for spot in self.spots:
            rep += repr(spot) + ', '
        rep = rep.rstrip(', ') + ')'
        return rep

    def remove_car(spots: List[Spot], index: int):
        # if 
        pass


if __name__ == '__main__':
    park = Park(park_length=10)
    print(repr(park))
    park.park_car(car=Car(car_length=2, car_time=2))
    print(repr(park))
    park.park_car(car=Car(car_length=4, car_time=3))
    print(repr(park))
    park.elapse_period()
    park.elapse_period()
    print(repr(park))
    park.elapse_period()
    print(repr(park))