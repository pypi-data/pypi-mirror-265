from ..interface import IPacker


class LoginDataPacker(IPacker):
    def __init__(self, obj) -> None:
        super().__init__(obj)

    def obj_to_tuple(self):
        return [str(self._obj.UserID), str(self._obj.PassWord)]

    def tuple_to_obj(self, t):
        if len(t) >= 2:
            self._obj.UserID = t[0]
            self._obj.PassWord = t[1]
            return True
        return False
