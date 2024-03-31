from __future__ import annotations

import math
import random
from typing import Optional, Tuple, List, Any

import numpy as np
from playwright.async_api import Page


def mock_mouse(page: Page) -> None:
    mouse_mocker = MouseMock(page)

    # MouseMocking
    async def click_mocker(
        x: int | float,
        y: int | float,
        button: Optional[str] = "left",
        click_count: Optional[int] = 1,
        delay: Optional[int] = 20,
        humanly: Optional[bool] = True,
    ) -> None:
        await mouse_mocker.click(x, y, button, click_count, delay, humanly)

    page.mouse.click = click_mocker

    async def dblclick_mocker(
        x: int | float,
        y: int | float,
        button: Optional[str] = "left",
        delay: Optional[int] = 20,
        humanly: Optional[bool] = True,
    ) -> None:
        await mouse_mocker.dblclick(x, y, button, delay, humanly)

    page.mouse.dblclick = dblclick_mocker

    async def move_mocker(
        x: int | float, y: int | float, steps: Optional[int] = 1, humanly: Optional[bool] = True
    ) -> None:
        await mouse_mocker.move(x, y, steps, humanly)

    page.mouse.origin_move = page.mouse.move
    page.mouse.move = move_mocker


# From https://github.com/riflosnake/HumanCursor/blob/main/humancursor/utilities/human_curve_generator.py
class HumanizeMouseTrajectory:
    def __init__(
        self, from_point: Tuple[int | float, int | float], to_point: Tuple[int | float, int | float]
    ) -> None:
        self.from_point = from_point
        self.to_point = to_point
        self.points = self.generate_curve()

    def easeOutQuad(self, n: float) -> float:
        if not 0.0 <= n <= 1.0:
            raise ValueError('Argument must be between 0.0 and 1.0.')
        return -n * (n - 2)

    def generate_curve(self) -> List[Tuple[int, int]]:
        """Generates the curve based on arguments below, default values below are automatically modified to cause randomness"""
        left_boundary = min(self.from_point[0], self.to_point[0]) - 80
        right_boundary = max(self.from_point[0], self.to_point[0]) + 80
        down_boundary = min(self.from_point[1], self.to_point[1]) - 80
        up_boundary = max(self.from_point[1], self.to_point[1]) + 80

        tween = self.easeOutQuad

        internalKnots = self.generate_internal_knots(
            left_boundary, right_boundary, down_boundary, up_boundary, 2
        )
        points = self.generate_points(internalKnots)
        points = self.distort_points(points, 1, 1, 0.5)
        points = self.tween_points(points, 100)
        return points

    def generate_internal_knots(
        self,
        l_boundary: int | float,
        r_boundary: int | float,
        d_boundary: int | float,
        u_boundary: int | float,
        knots_count: int,
    ) -> List[Tuple[int, int]]:
        """Generates the internal knots of the curve randomly"""
        if not (
            self.check_if_numeric(l_boundary)
            and self.check_if_numeric(r_boundary)
            and self.check_if_numeric(d_boundary)
            and self.check_if_numeric(u_boundary)
        ):
            raise ValueError("Boundaries must be numeric values")
        if not isinstance(knots_count, int) or knots_count < 0:
            knots_count = 0
        if l_boundary > r_boundary:
            raise ValueError("left_boundary must be less than or equal to right_boundary")
        if d_boundary > u_boundary:
            raise ValueError("down_boundary must be less than or equal to upper_boundary")

        try:
            knotsX = np.random.choice(range(l_boundary, r_boundary) or l_boundary, size=knots_count)
            knotsY = np.random.choice(range(d_boundary, u_boundary) or d_boundary, size=knots_count)
        except TypeError:
            knotsX = np.random.choice(range(int(l_boundary), int(r_boundary)), size=knots_count)
            knotsY = np.random.choice(range(int(d_boundary), int(u_boundary)), size=knots_count)

        return list(zip(knotsX, knotsY))

    def generate_points(self, knots: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Generates the points from BezierCalculator"""
        if not self.check_if_list_of_points(knots):
            raise ValueError("knots must be valid list of points")

        midPtsCnt = max(
            abs(self.from_point[0] - self.to_point[0]),
            abs(self.from_point[1] - self.to_point[1]),
            2,
        )
        knots = [self.from_point] + knots + [self.to_point]
        return BezierCalculator.calculate_points_in_curve(int(midPtsCnt), knots)

    def distort_points(
        self,
        points: List[Tuple[int, int]],
        distortion_mean: int,
        distortion_st_dev: int,
        distortion_frequency: float,
    ) -> List[Tuple[int, int]]:
        """Distorts points by parameters of mean, standard deviation and frequency"""
        if not (
            self.check_if_numeric(distortion_mean)
            and self.check_if_numeric(distortion_st_dev)
            and self.check_if_numeric(distortion_frequency)
        ):
            raise ValueError("Distortions must be numeric")
        if not self.check_if_list_of_points(points):
            raise ValueError("points must be valid list of points")
        if not (0 <= distortion_frequency <= 1):
            raise ValueError("distortion_frequency must be in range [0,1]")

        distorted = []
        for i in range(1, len(points) - 1):
            x, y = points[i]
            delta = (
                np.random.normal(distortion_mean, distortion_st_dev)
                if random.random() < distortion_frequency
                else 0
            )
            distorted += ((x, y + delta),)
        distorted = [points[0]] + distorted + [points[-1]]
        return distorted

    def tween_points(
        self, points: List[Tuple[int, int]], target_points: int
    ) -> List[Tuple[int, int]]:
        """Modifies points by tween"""
        if not self.check_if_list_of_points(points):
            raise ValueError("List of points not valid")
        if not isinstance(target_points, int) or target_points < 2:
            raise ValueError("target_points must be an integer greater or equal to 2")

        res = []
        for i in range(target_points):
            index = int(self.easeOutQuad(float(i) / (target_points - 1)) * (len(points) - 1))
            res += (points[index],)
        return res

    @staticmethod
    def check_if_numeric(val: Any) -> bool:
        """Checks if value is proper numeric value"""
        return isinstance(val, (float, int, np.int32, np.int64, np.float32, np.float64))

    def check_if_list_of_points(self, list_of_points: List[Tuple[int, int]]) -> bool:
        """Checks if list of points is valid"""
        if not isinstance(list_of_points, list):
            return False
        try:
            point = lambda p: (
                (len(p) == 2) and self.check_if_numeric(p[0]) and self.check_if_numeric(p[1])
            )
            return all(map(point, list_of_points))
        except (KeyError, TypeError):
            return False


class BezierCalculator:
    @staticmethod
    def binomial(n: int, k: int):
        """Returns the binomial coefficient "n choose k" """
        return math.factorial(n) / float(math.factorial(k) * math.factorial(n - k))

    @staticmethod
    def bernstein_polynomial_point(x: int, i: int, n: int):
        """Calculate the i-th component of a bernstein polynomial of degree n"""
        return BezierCalculator.binomial(n, i) * (x**i) * ((1 - x) ** (n - i))

    @staticmethod
    def bernstein_polynomial(points: list):
        """
        Given list of control points, returns a function, which given a point [0,1] returns
        a point in the Bezier described by these points
        """

        def bernstein(t):
            n = len(points) - 1
            x = y = 0
            for i, point in enumerate(points):
                bern = BezierCalculator.bernstein_polynomial_point(t, i, n)
                x += point[0] * bern
                y += point[1] * bern
            return x, y

        return bernstein

    @staticmethod
    def calculate_points_in_curve(n: int, points: list):
        """
        Given list of control points, returns n points in the Bézier curve,
        described by these points
        """
        curvePoints = []
        bernstein_polynomial = BezierCalculator.bernstein_polynomial(points)
        for i in range(n):
            t = i / (n - 1)
            curvePoints += (bernstein_polynomial(t),)
        return curvePoints


class MouseMock:
    def __init__(self, page: Page):
        self.page = page
        self.last_x = 0
        self.last_y = 0

    async def click(
        self,
        x: int | float,
        y: int | float,
        button: Optional[str] = "left",
        click_count: Optional[int] = 1,
        delay: Optional[int] = 20,
        humanly: Optional[bool] = True,
    ) -> None:
        # Move mouse humanly to the Coordinates and wait some random time
        await self.move(x, y, humanly)
        await self.page.wait_for_timeout(random.randint(4, 8) * 100)

        # Clicking the Coordinates
        await self.page.mouse.down(button=button, click_count=click_count)
        # Waiting as delay
        await self.page.wait_for_timeout(delay)
        await self.page.mouse.up(button=button, click_count=click_count)

        # Waiting random time
        await self.page.wait_for_timeout(random.randint(4, 8) * 100)

    async def dblclick(
        self,
        x: int | float,
        y: int | float,
        button: Optional[str] = "left",
        delay: Optional[int] = 20,
        humanly: Optional[bool] = True,
    ) -> None:
        # Move mouse humanly to the Coordinates and wait some random time
        await self.move(x, y, humanly)
        await self.page.wait_for_timeout(random.randint(4, 8) * 100)

        # Clicking the Coordinates
        await self.page.mouse.down(button=button)
        # Waiting as delay
        await self.page.wait_for_timeout(delay)
        await self.page.mouse.up(button=button)

        # Waiting short random time
        await self.page.wait_for_timeout(random.randint(8, 14) * 10)
        # Clicking the Coordinates
        await self.page.mouse.down(button=button)
        # Waiting as delay
        await self.page.wait_for_timeout(delay)
        await self.page.mouse.up(button=button)

        # Waiting random time
        await self.page.wait_for_timeout(random.randint(4, 8) * 100)

    async def move(
        self,
        x: int | float,
        y: int | float,
        steps: Optional[int] = 1,
        humanly: Optional[bool] = True,
    ) -> None:
        # If you want to move in a straight line
        if not humanly:
            await self.page.mouse.origin_move(x, y, steps=steps)
            return

        if x == self.last_x and y == self.last_y:
            await self.page.wait_for_timeout(random.randint(1, 10))
            return

        humanized_points = HumanizeMouseTrajectory((self.last_x, self.last_y), (x, y))

        # Move Mouse to new random locations
        for x, y in humanized_points.points:
            await self.page.mouse.origin_move(x, y)
            # await page.wait_for_timeout(random.randint(1, 5))
        # Set LastX and LastY cause Playwright does not have mouse.current_location
        self.last_x, self.last_y = humanized_points.points[-1]
