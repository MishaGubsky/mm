from random import Random as PyRandom


def simpson(a=0, b=2, rand1=PyRandom(83349), rand2=PyRandom(115535)):
    def generator(a, b, rand, rand2):
        while True:
            yield round(rand.random() + rand2.random(), 2)
    return generator(a,b,rand1, rand2).next()
