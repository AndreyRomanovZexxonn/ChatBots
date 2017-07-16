__author__ = 'zexxonn'

import inspect

class AttrHellpers:
    @staticmethod
    def getAttrToValueInfo(classInfo):
        attributes = inspect.getmembers(classInfo, lambda a : not(inspect.isroutine(a)))
        return dict([a for a in attributes \
                    if not(a[0].startswith('__') and a[0].endswith('__'))
                       and not (a[0] == "attrToValueMap") and not (a[0] == "valueToAttrMap")])

    @staticmethod
    def getValueToAttrInfo(classInfo):
        attributes = inspect.getmembers(classInfo, lambda a : not(inspect.isroutine(a)))
        x = dict([a for a in attributes \
                if not (a[0].startswith('__') and a[0].endswith('__'))
                   and not (a[0] == "attrToValueMap") and not (a[0] == "valueToAttrMap") ])

        return dict((v,k) for k,v in x.iteritems())

class ServerStateId(object):
    SERVER_BASE_STATE, \
    SERVER_ASKED_USER_FOR_CCY_PAIR, \
    SERVER_REQUESTED_USERS_LOCATION, \
        = range(3)

    def __init__(self, value):
        if isinstance(value, int):
            self.value = value
            return
        if isinstance(value, basestring):
            if value in self.__class__.attrToValueMap:
                self.value = self.__class__.attrToValueMap[value]
                return
        raise Exception("ServerStateId() constructor: invalid initialization value = " + str(value))

    def __str__(self):
        if self.value in self.__class__.valueToAttrMap:
            return self.__class__.valueToAttrMap[self.value]
        return "Error: unknown State type."

    def __eq__(self,y):
        if isinstance(y, int):
            return self.value == y
        return self.value == y.value

ServerStateId.attrToValueMap = AttrHellpers.getAttrToValueInfo(ServerStateId)
ServerStateId.valueToAttrMap = AttrHellpers.getValueToAttrInfo(ServerStateId)

class MessageTypeId(object):
    SIMPLE_MESSAGE,\
    CCY_PAIR_REQUEST, \
    LOCATION_INFO \
        = range(3)

    def __init__(self, value):
        if isinstance(value, int):
            self.value = value
            return
        if isinstance(value, str):
            if value in self.__class__.attrToValueMap:
                self.value = self.__class__.attrToValueMap[value]
                return
        raise Exception("MessageTypeId() constructor: invalid initialization value = " + str(value))

    def __str__(self):
        if self.value in self.__class__.valueToAttrMap:
            return self.__class__.valueToAttrMap[self.value]
        return "Error: unknown State type."

    def __eq__(self,y):
        if isinstance(y, int):
            return self.value == y
        return self.value == y.value

MessageTypeId.attrToValueMap = AttrHellpers.getAttrToValueInfo(MessageTypeId)
MessageTypeId.valueToAttrMap = AttrHellpers.getValueToAttrInfo(MessageTypeId)

