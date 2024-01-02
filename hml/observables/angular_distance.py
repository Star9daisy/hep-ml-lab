from ..types import Observable
from ..utils import get_observable


class AngularDistance(Observable):
    def __init__(self, physics_object, sorted_by="pt", reverse=True):
        super().__init__(physics_object)
        self.sorted_by = sorted_by
        self.reverse = reverse
        self.orders = [
            get_observable(f"{i}.{sorted_by}") for i in physics_object.split(",")
        ]

    def get_value(self):
        if len(self.main_objs) != 2:
            return

        for i in self.orders:
            i.read(self.event)

        if len(self.sub_objs[0]) != 0:
            flat_obj0 = [i for subs in self.sub_objs[0] for i in subs]
            flat_order0 = [i for subs in self.orders[0].value for i in subs]
        else:
            flat_obj0 = [i for i in self.main_objs[0]]
            flat_order0 = [i for i in self.orders[0].value]

        if len(self.sub_objs[1]) != 0:
            flat_obj1 = [i for subs in self.sub_objs[1] for i in subs]
            flat_order1 = [i for subs in self.orders[1].value for i in subs]
        else:
            flat_obj1 = [i for i in self.main_objs[1]]
            flat_order1 = [i for i in self.orders[1].value]

        sorted_obj0 = [
            obj
            for _, obj in sorted(
                zip(flat_order0, flat_obj0),
                key=lambda pair: pair[0],
                reverse=self.reverse,
            )
        ]
        sorted_obj1 = [
            obj
            for _, obj in sorted(
                zip(flat_order1, flat_obj1),
                key=lambda pair: pair[0],
                reverse=self.reverse,
            )
        ]

        values = []
        for i in sorted_obj0:
            distance_per_i = []

            for j in sorted_obj1:
                if i is None or j is None:
                    distance_per_i.append(float("nan"))
                else:
                    distance_per_i.append(i.P4().DeltaR(j.P4()))
            values.append(distance_per_i)

        return values


class DeltaR(AngularDistance):
    ...


AngularDistance.add_alias("angular_distance")
DeltaR.add_alias("delta_r")
