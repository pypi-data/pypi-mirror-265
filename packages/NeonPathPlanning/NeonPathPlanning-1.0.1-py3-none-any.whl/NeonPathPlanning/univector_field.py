import math
from .commons import Point, angle_between, reduce_angle, norm, dist


class UnivectorField:
    """
    An implementation of the uni vector field path planning algorithm

    The UnivectorField will generate vector that guides a given point to the target so that it gets there with an angle
    directed at the guiding point. This algorithm is also capable of contouring obstacles and generating a rectangle
    behind the target where the vectors have the save directions as the target-guide vector.
    """

    def __init__(self, n, rect_size=0, field=None, field_margin=0.0525):
        """Inits UnivectorField class.

        Parameters
        ----------
        n : float
            Constant the related to how much the path will avoid hitting the target from the wrong direction
        rect_size : float
            The base side size of the rectangle behind the target where all the vectors are the same angle of the
            target-guide line
        field : Field, optional
            The size and origin of the field
        field_margin : float, optional
            The size of the field margin in which a repulsion vector filed will be applied
        """
        self.obstacles = {}
        self.N = n
        self.delta_g = rect_size
        self.field = field

        self.target_pos = None
        self.target_guide = None

        self.field_margin = field_margin

    def to_json(self):
        out = {
            'n': self.N,
            'dg': self.delta_g,
            'margin': self.field_margin
        }

        if self.target_pos:
            out['target'] = ((self.target_pos.x, self.target_pos.y), (self.target_guide.x, self.target_guide.y))

        if self.obstacles:
            out['obstacles'] = [(pos.x, pos.y, radius) for pos, radius in self.obstacles.values()]

        return out

    @classmethod
    def from_json(cls, json_dict, field=None):
        out = cls(json_dict['n'], json_dict['dg'], field, json_dict['margin'])

        if target := json_dict.get('target', None):
            out.set_target(Point(target[0][0], target[0][1]), Point(target[1][0], target[1][1]))

        for x, y, radius in json_dict.get('obstacles', []):
            out.add_obstacle(Point(x, y), radius)

        return out

    def add_obstacle(self, pos, radius):
        """
        Add one obstacle

        Parameters
        ----------
        pos : Point
            Obstacle center x and y coordinates, any object with x and y parameters works
        radius : float
            The radius of the obstacle avoidance field

        Returns
        -------
        pos : object
            The identifier of the obstacle created
        """

        self.obstacles[pos] = (pos, radius)
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

    def set_target(self, target, guide, guide_type='p'):
        """
        Defines the target position and a guiding point

        Parameters
        ----------
        target : Point
            Target x and y coordinates,  any object with x and y parameters works
        guide : Point or float
            Either guide point x and y coordinates or the desired target hitting angle
        guide_type : {'p', 'a'}
            Type of guide given position or angle
        """

        self.target_pos = target  # self.g

        if guide_type == 'a':
            self.target_guide = Point(
                self.target_pos.x + .05 * math.cos(guide),
                self.target_pos.y + .05 * math.sin(guide)
            )

        if guide_type == 'p':
            self.target_guide = guide  # self.r

    def __call__(self, p):
        return self.compute(p)

    def __check_border(self, p):
        if self.field is None:
            return False

        if p.x <= self.field.o_x + self.field_margin:
            return True

        if p.y <= self.field.o_y + self.field_margin:
            return True

        if p.x >= self.field.o_x - self.field_margin + self.field.w:
            return True

        return False

    def __weighted_sum(self, ang_guide, *args, wmax=2, wmin=1):
        """
        Calculate the weighted mean between the angle of any number of vectors
        The weight of each vector is calculated based on the angle of a guide vector

        Parameters
        ----------
        ang_guide : float
            Angle of the guide vector
        *args : float
            One or more angles used for the calculation
        wmax : float, optional
            Maximum weight for the sum
        wmin : float, optional
            Minimum weight for the sum

        Returns
        -------
        new_angle (float): the angle resulted by the weighted mean
        """
        sum_sin = 0
        sum_cos = 0

        for angle in args:
            dif_ang = abs(ang_guide - angle)

            weight = ((wmax - wmin) * abs(math.cos(dif_ang / 2)) + wmin)

            sum_sin += weight * math.sin(angle)
            sum_cos += weight * math.cos(angle)

        new_angle = math.atan2(sum_sin, sum_cos)

        return new_angle

    def compute(self, p):
        """
        Calculate the desired angle for the given position

        Parameters
        ----------
        p : Point
            The position for which the angle will be calculated, any object with x and y parameters works

        Returns
        -------
        angle : float
            The angle of the vector in the field at the given position
        """
        behind_angle = None

        ang_pr = angle_between(p, self.target_guide)
        ang_rg = angle_between(self.target_pos, self.target_guide)
        ang_pg = angle_between(p, self.target_pos)

        phi = ang_pr - ang_pg
        phi = reduce_angle(phi)
        angle_f_p = ang_pg - self.N * phi
        angle_f_p = reduce_angle(angle_f_p)

        # check if the position is inside the rectangle behind obstacle
        j = ang_rg + math.pi * .5

        x = self.target_guide.x + self.delta_g * .5 * math.cos(j)
        y = self.target_guide.y + self.delta_g * .5 * math.sin(j)
        a = math.tan(ang_rg)
        b = y - math.tan(ang_rg) * x

        d_pg1 = abs(a * p[0] - p[1] + b) / math.sqrt(a ** 2 + 1)

        x = self.target_guide.x - self.delta_g * .5 * math.cos(j)
        y = self.target_guide.y - self.delta_g * .5 * math.sin(j)
        a = math.tan(ang_rg)
        b = y - math.tan(ang_rg) * x

        d_pg2 = abs(a * p[0] - p[1] + b) / math.sqrt(a ** 2 + 1)

        if d_pg1 < self.delta_g and d_pg2 < self.delta_g:
            if dist(self.target_guide, p) >= dist(p, self.target_pos):
                angle_f_p = ang_rg

        # check if the position is close to one of the borders
        on_border = self.__check_border(p)
        if on_border:
            new_angle = self.__weighted_sum(ang_pg, ang_pg, angle_f_p)
            return reduce_angle(new_angle)

        for pos, margin in self.obstacles.values():

            # check if the obstacle is close to one of the borders
            ang_bo1 = self.__check_border(Point(pos.x + margin, pos.y + margin))
            ang_bo2 = self.__check_border(Point(pos.y - margin, pos.y - margin))

            # check if the position is inside the margin of the obstacle
            if margin >= dist(pos, p):
                margin_ang = (2 * angle_between(pos, p) + angle_f_p) / 3
                margin_ang = reduce_angle(margin_ang)
                if abs(angle_between(pos, p) - angle_f_p) > math.pi:
                    margin_ang = reduce_angle(margin_ang + math.pi)
                if ang_bo1:
                    return reduce_angle(self.__weighted_sum(margin_ang, margin_ang, ang_pg, wmax=3))
                if ang_bo2:
                    return reduce_angle(self.__weighted_sum(margin_ang, ang_pg, margin_ang, wmax=3))
                return margin_ang

            # check if the line pg is secant to the obstacle
            a = p.y - self.target_pos.y
            b = self.target_pos.x - p.x
            c = p.x * self.target_pos.y - p.y * self.target_pos.x

            if norm(a, b) != 0 and margin >= abs(a * pos.x + b * pos.y + c) / norm(a, b):
                # check if p is behind the obstacle
                if (dist(self.target_pos, pos) <= dist(self.target_pos, p)
                        and dist(self.target_pos, p) > dist(p, pos)):

                    # check if the obstacle is in the way of f(p)
                    ang_t1 = angle_between(p, pos) + math.atan(margin/dist(p, pos))
                    ang_t2 = angle_between(p, pos) - math.atan(margin/dist(p, pos))

                    if ang_t1 > angle_f_p > ang_t2:
                        if angle_f_p > angle_between(p, pos):
                            behind_angle = ang_t1
                            pass
                        else:
                            behind_angle = ang_t2

        if behind_angle is not None:
            return behind_angle
        angle_f_p = reduce_angle(angle_f_p)
        return angle_f_p
