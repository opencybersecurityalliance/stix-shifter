#!/usr/bin/python


class Base(object):

    def __str__(self):
        if hasattr(self, "id"):
            id_str = " %s" % self.id
        elif hasattr(self, "guid"):
            id_str = " %s" % self.guid
        elif hasattr(self, "name"):
            id_str = " %s" % self.name
        if hasattr(self, "user_id"):
            id_str = " %s (user_id)" % self.user_id
        else:
            id_str = " "

        return "%s%s:  %r" % (self.__class__.__name__, id_str, self.__dict__)
