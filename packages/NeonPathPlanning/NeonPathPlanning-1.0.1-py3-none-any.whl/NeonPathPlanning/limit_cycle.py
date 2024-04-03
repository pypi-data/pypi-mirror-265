import math
from .commons import line_circle_intersection, Point


class LimitCycle:
    def __init__(self, fitness=15):
        """
        Constructor of the Limit Cycle class

        Parameters
        ----------
        fitness : float, optional
            Parameter to increase/decrease the 'fitness' of the trajectory
        """
        self.target = None
        self.obstacles = {}

        self.fitness = fitness
        self.dt = 0.01

    def to_json(self):
        out = {
            'fitness': self.fitness,
        }

        if self.target:
            out['target'] = (self.target.x, self.target.y)

        if self.obstacles:
            out['obstacles'] = [
                (pos.x, pos.y, radius, force_direction, clockwise)
                for pos, radius, force_direction, clockwise in self.obstacles.values()
            ]

        return out

    @classmethod
    def from_json(cls, json_dict, field=None):
        out = cls(json_dict['fitness'])

        if target := json_dict.get('target', None):
            out.set_target(Point(target[0], target[1]))

        for x, y, radius, force_direction, clockwise in json_dict.get('obstacles', []):
            out.add_obstacle(Point(x, y), radius, force_direction, clockwise)

        return out

    def add_obstacle(self, pos, radius, force_direction=False, clockwise=False):
        """
        Add one obstacle

        Parameters
        ----------
        pos : Point
            Obstacle center x and y coordinates, any object with x and y parameters works
        radius : float
            The radius of the obstacle avoidance field
        force_direction : bool, optional
            Whether to force a direction around obstacle
        clockwise : bool, optional
            If forcing direction go clockwise or counter-clockwise

        Returns
        -------
        pos : object
            The identifier of the obstacle created
        """

        self.obstacles[pos] = (pos, radius, force_direction, clockwise)
        return pos

    def del_obstacle(self, *args, all=False):
        """
        Delete any amount of obstacles

        Parameters
        ----------
        *args : object
            a variable amount of obstacles to be deleted
        all : bool
            whether to delete all obstacles
        """
        if all:
            self.obstacles.clear()
            return

        for obstacle in args:
            del self.obstacles[obstacle]

    def set_target(self, target):
        """
        Defines the target position

        Parameters
        ----------
        target : Point
            Target x and y coordinates, any object with x and y parameters works
        """

        self.target = target

    def __call__(self, p):
        return self.compute(p)

    def __contour(self, p, a, b, c, obstacle):
        dx = p.x - obstacle[0].x
        dy = p.y - obstacle[0].y

        # this multiplier is used to increase/decrease the fitness of the path around the obstacle based on the
        # 'fitness' variable taken as a parameter
        mlt = int(self.fitness / math.sqrt(dx ** 2 + dy ** 2))

        # if the obstacle is a virtual one the rotation direction shouldn't change
        if obstacle[2]:
            d = 1 if obstacle[3] else -1
        else:
            d = (a * obstacle[0].x + b * obstacle[0].y + c) / math.sqrt(a ** 2 + b ** 2)

        ddx = (d / abs(d)) * dy + mlt * dx * (obstacle[1] ** 2 - dx ** 2 - dy ** 2)
        ddy = -(d / abs(d)) * dx + mlt * dy * (obstacle[1] ** 2 - dx ** 2 - dy ** 2)

        return Point(p.x + self.dt * ddx, p.y + self.dt * ddy)

    def compute(self, p):
        """
        Runs the Limit Cycle algorithm

        Parameters
        ----------
        p : Point
            The position for which the vector will be calculated, any object with x and y parameters works

        Returns
        -------
        next : Point
            The next point on the path
        """

        # a, b and c are the indexes of a linear equation: a*x + b*y + c = 0
        a = self.target.y - p.y
        b = p.x - self.target.x
        c = self.target.x * p.y - self.target.y * p.x

        # separate all the obstacles on the way
        intersections = list(filter(lambda x: line_circle_intersection(a, b, c, *x[:2]), self.obstacles.values()))

        # if the path is clear return the target
        if len(intersections) == 0:
            return self.target

        # sort the obstacles by their distance from the robot, ascending
        intersections.sort(key=lambda x: math.sqrt((x[0].x - p.x) ** 2 + (x[0].y - p.y) ** 2))

        # contour the nearest target
        return self.__contour(p, a, b, c, intersections[0])
