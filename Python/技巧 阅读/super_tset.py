# coding:utf8
import collections
import pprint


class LoggingDict(dict):
    def __setitem__(self, key, value):
        print "Settingto %s: %s" % (key, value)
        super(self.__class__, self).__setitem__(key, value)

ld = LoggingDict()
ld['a'] = 'a'


class LoggingOD(LoggingDict, collections.OrderedDict):
    pass

lod = LoggingOD()
lod['b'] = 'b'
# Settingto b: b
# [Finished in 1.8s]

print LoggingOD.__base__
# 在多种继承且符合菱形继承时, Python2.4 以后会广度顺序进行继承.
# pprint(LoggingOD.__mro__)

# 多继承的super调用顺序

# class Root:
#     def draw(self):
#         # the delegation chain stops here
#         assert not hasattr(super(Root, self), 'draw')


# class Shape(Root):
#     def __init__(self, shapename, **kwds):
#         self.shapename = shapename
#         super(Shape, self).__init__(**kwds)

#     def draw(self):
#         print('Drawing.  Setting shape to:', self.shapename)
#         super(Shape, self).draw()


# class ColoredShape(Shape):
#     def __init__(self, color, **kwds):
#         self.color = color
#         super(ColoredShape, self).__init__(**kwds)

#     def draw(self):
#         print('Drawing.  Setting color to:', self.color)
#         super(ColoredShape, self).draw()

# cs = ColoredShape(color='blue', shapename='square')
# cs.draw()
