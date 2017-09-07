# coding:utf8
import six


def dispatch_types(value):
    if isinstance(value, six.integer_types):
        print('%s is Integer' % value)
    elif isinstance(value, six.class_types):
        print('%s is Class' % value)
    elif isinstance(value, six.string_types):
        print('%s is String' % value)

if __name__ == '__main__':
    dispatch_types(1)
    dispatch_types(object)
    dispatch_types('aaa')
