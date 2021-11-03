from pyvar.ml.utils.timer import Timer

foo = Timer()
with foo.timeit():
    ...

print(f"Time: {foo.time}")
