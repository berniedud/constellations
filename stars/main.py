"""
create some random stars in a graph, so that all stars are connected to at least one other star,
and any star can be reached by traversal of the graph, form any other star
"""
from math import sqrt
from random import random
from typing import Tuple


STAR_COUNT = 5


def get_random_location() -> Tuple[float]:
    location = (random(), random())
    return location


def create_stars() -> dict:
    stars = dict()
    for star_no in range(STAR_COUNT):
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


def find_nearest(target: int, stars: dict) -> int:
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


def connect_stars(stars: dict) -> dict:
    """
    connect each star to it's nearest neighbour
    :param stars:
    :return:
    """
    stars_to_connect = set(stars.keys())
    while stars_to_connect:
        connect_me = stars_to_connect.pop()
        nearest_neighbour = find_nearest(connect_me, stars)
        stars[connect_me]['connections'].add(nearest_neighbour)
        stars[nearest_neighbour]['connections'].add(connect_me)

    return stars


def create_and_connect_stars() -> dict:
    stars = create_stars()
    stars = connect_stars(stars)

    return stars
