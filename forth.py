from third import BaseRandom
import matplotlib.pyplot as plt


class DiscreteRandom(BaseRandom):
    def __init__(self, y, P):
        super(DiscreteRandom, self).__init__()
        self.y = y
        self.P = P

    def next(self):
        R = self.generator.next()
        for k in range(len(self.P)):
            if R <= sum(self.P[0:k + 1]):
                return self.y[k]


if __name__ == '__main__':
    P = [0.162, 0.323, 0.291, 0.155, 0.054, 0.013, 0.002]
    if sum(p) > 1:
        raise AttributeError(" >1!!!!")
    y = range(len(P))
    generator = DiscreteRandom(y, P)
    a = [generator.next() for _ in range(1000)]
    plt.hist(a, sorted(y), normed=True, cumulative=True, color='green')
    plt.show()
