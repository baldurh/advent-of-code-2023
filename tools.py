import re
from functools import partial, reduce
from itertools import accumulate, chain
from operator import getitem as get_item


def side_effect(func):
    def inner(args):
        func(args)
        return args

    return inner


def each_c(func):
    def inner(iter):
        for x in iter:
            func(x)

    return inner


def reduce_c(func, start=None):
    if start is not None:
        return lambda args: reduce(func, args, start)
    return partial(reduce, func)


def reducei_c(func, start=None, istart=None):
    if istart is not None:
        return lambda args: reduce(func, enumerate(args, start), start)
    return lambda args: reduce(func, enumerate(args), start)


def mapi_c(func, start=None):
    if start is not None:
        return lambda seq: map(lambda x: func(x[0], x[1]), enumerate(seq, start))
    return lambda seq: map(lambda x: func(x[0], x[1]), enumerate(seq))


def accumulate_c(func, start=None):
    if start is not None:
        return lambda args: accumulate(args, func, start)
    return lambda args: accumulate(args, func)


identity = lambda x: x
pipe = lambda *args: reduce(lambda p, func: func(p), args)
compose = lambda *funcs: lambda *args: pipe(*args, *funcs)
map_c = lambda func: partial(map, func)
flat_map_c = lambda func: compose(map_c(func), chain.from_iterable)
filter_c = lambda func: partial(filter, func)
chain_c = lambda args: lambda it: chain(it, args)
spread = lambda func: lambda args: func(*args)
fork = lambda *funcs: lambda *args: map(
    lambda func: args[0] if func is None else func(*args), funcs
)
split = lambda *funcs: lambda *args: [
    a if funcs[i] is None else funcs[i](a) for i, a in enumerate(args)
]
split_args = lambda *funcs: spread(split(*funcs))
join = lambda func: lambda *args: func(*args)
getitem = lambda key: lambda obj: get_item(obj, key)
rev_arg = lambda func: lambda *args: func(*args[1:], args[0])
curry_1 = lambda func: lambda x: partial(func, x)
curry_2 = lambda func: lambda x1, x2: partial(func, x1, x2)

str_split = curry_1(rev_arg(str.split))
re_split = curry_1(re.split)
re_sub = curry_2(re.sub)
