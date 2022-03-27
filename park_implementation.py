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
    """_summary_
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
        
        for index, spot in enumerate(self.spots[:-1]):
            if isinstance(spot.occupant, Car):
                spot.occupant.car_time -= 1
                if spot.occupant.car_time == 0:
                    spot.occupant = None
            if (spot.occupant is None 
                    and self.spots[index + 1].occupant is None):
                spot.length += self.spots[index + 1].length
                self.spots.pop(index + 1)
    
    def report_utilisation(self) -> float:
        if len(self.spots) == 1 and self.spots[0].occupant is None:
            return 0
        empty_slots: int = sum(
            (spot.length for spot in self.spots if spot.occupant is None)
        )
        return (self.park_length - empty_slots) / self.park_length
    
    def __repr__(self) -> str:
        # Returns the available slots and the ones occupied by each car.
        rep: str = 'Park('
        for spot in self.spots:
            rep += repr(spot) + ', '
        rep = rep.rstrip(', ') + ')'
        return rep
