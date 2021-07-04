"""
create some random stars in a graph, so that all stars are connected to at least one other star,
and any star can be reached by traversal of the graph, form any other star
"""
from math import sqrt
from random import random
from typing import Tuple, Optional, Set, List

DEFAULT_STAR_COUNT = 5


def get_random_location() -> Tuple[float, float]:
    location = (random(), random())
    return location


def create_stars(star_count: Optional[int] = None) -> dict:
    stars = dict()
    for star_no in range(star_count or DEFAULT_STAR_COUNT):
        location = get_random_location()
        stars[star_no] = dict(
            location=location,
            connections=set()
        )

    return stars


def get_distance(coords1: Tuple[float, float], coords2: Tuple[float, float]) -> float:
    x1, y1 = coords1
    x2, y2 = coords2
    distance = sqrt(
        ((x2 - x1) ** 2) +
        ((y2 - y1) ** 2)
    )
    return distance


def find_nearest_star(target: int, stars: dict) -> int:
    """
    find the nearest star to the target
    :param target:
    :param stars:
    :return:
    """
    nearest = None
    nearest_distance = None
    target_coords = stars[target]['location']
    for candidate, details in stars.items():
        if candidate == target:
            continue
        distance = get_distance(target_coords, details['location'])
        if not nearest_distance or distance < nearest_distance:
            nearest_distance = distance
            nearest = candidate

    return nearest


def connect_stars(stars: dict, connect1: int, connect2: int) -> dict:
    stars[connect1]['connections'].add(connect2)
    stars[connect2]['connections'].add(connect1)

    return stars


def connect_stars_to_nearest(stars: dict) -> dict:
    """
    connect each star to it's nearest neighbour
    :param stars:
    :return:
    """
    stars_to_connect = set(stars.keys())
    while stars_to_connect:
        connect_me = stars_to_connect.pop()
        nearest_neighbour = find_nearest_star(connect_me, stars)
        stars = connect_stars(stars, connect_me, nearest_neighbour)

    return stars


def create_and_connect_stars(star_count: Optional[int] = None) -> dict:
    stars = create_stars(star_count)
    stars = connect_stars_to_nearest(stars)

    return stars


def find_connected_recursively(stars: dict, start_at_star: int,
                               connected: Optional[set]) -> Set[int]:
    connected = connected if connected else set()    # make an empty set if None
    this_star = stars[start_at_star]
    this_stars_connections = this_star['connections']
    new_connections = this_stars_connections - connected
    connected |= new_connections
    for connected_star in new_connections:
        connected = find_connected_recursively(stars, connected_star, connected)

    return connected


def find_connected_stars(stars: dict, start_at_star: int) -> Set[int]:
    """
    A wrapper for the 'real' recursive function, so we don't have to set the value of
    the third parameter (connected) to None to use the function
    :param stars:
    :param start_at_star:
    :return:
    """
    return find_connected_recursively(stars, start_at_star, None)


def find_all_constellations(stars: dict) -> List[set]:
    all_constellations = list()
    stars_not_in_constellations = set(stars.keys())
    while stars_not_in_constellations:
        start_at_star = stars_not_in_constellations.pop()
        this_constellation = find_connected_stars(stars, start_at_star)
        all_constellations.append(this_constellation)
        stars_not_in_constellations -= this_constellation

    return all_constellations


def get_average_location(stars, this_constellation) -> Tuple[float, float]:
    star_count = len(this_constellation)
    all_x_y = [
        stars[this_star]['location']
        for this_star in this_constellation
    ]
    avg_x = sum([coords[0] for coords in all_x_y]) / star_count
    avg_y = sum([coords[1] for coords in all_x_y]) / star_count
    return avg_x, avg_y


def find_nearest_pair(stars: dict, constellation1: Set[int],
                      constellation2: Set[int]) -> Tuple[int, int]:
    nearest_distance = None
    nearest_pair = None
    for star_from_1 in constellation1:
        for star_from_2 in constellation2:
            distance = get_distance(
                stars[star_from_1]['location'],
                stars[star_from_2]['location']
            )
            if not nearest_pair or distance < nearest_distance:
                nearest_pair = (star_from_1, star_from_2)
                nearest_distance = distance

    return nearest_pair


def connect_constellations(stars: dict, constellations: List[set]) -> dict:
    while len(constellations) > 1:
        # we will find the nearest to the first one, merge them, carry on until only one left
        this_constellation = constellations.pop(0)
        this_avg_location = get_average_location(stars, this_constellation)
        nearest_index = None
        nearest_distance = None
        for constellation_index, candidate_constellation in enumerate(constellations):
            candidate_avg_location = get_average_location(stars, candidate_constellation)
            distance = get_distance(this_avg_location, candidate_avg_location)
            if not nearest_distance or distance < nearest_distance:
                nearest_distance = distance
                nearest_index = constellation_index
        nearest_constellation = constellations.pop(nearest_index)
        nearest_pair = find_nearest_pair(stars, this_constellation, nearest_constellation)
        stars = connect_stars(stars, *nearest_pair)
        constellations.append(this_constellation | nearest_constellation)

    return stars
