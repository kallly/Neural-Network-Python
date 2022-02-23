import math
from operator import ne
from typing import List

class Synapse:
    id = 0
    weight = 0

    def __init__(self, id):
        self.id = id

class Perceptron:
    id = 0
    nenter = 0
    activFunc = None

    prev = None
    next = None
    synapses = None
    
    exit = None
    exitDelta = None

    output = None
    solve = None

    nformed = 0
    nformedDelta = 0

    def __init__(self, id, nenter, activ) -> None:
        self.id = id
        self.nenter = nenter
        self.selectActivFunc(activ)

        self.prev = []
        self.next = []
        self.synapses = []
        self.exit = []
        self.exitDelta = []
        self.output = []
        self.solve = []


    def get_synapse(self,id):
        for synapse in self.synapses:
            if synapse.id == id:
                return synapse
        return None
    
    def set_synapse(self, id, weight):
        for synapse in self.synapses:
            if synapse.id == id:
                synapse.weight = weight
                return synapse

    def forming(self):
        self.nformed += 1
        if self.nformed == len(self.prev):
            r = [0] * self.nenter
            s = [0] * self.nenter

            for e in range(self.nenter):
                for prev in self.prev:
                    weight = self.get_synapse(prev.id).weight
                    r[e] += prev.exit[e] * weight
        
                s[e] = self.activFunc(r[e])

            self.exit = s

            for next in self.next:
                next.forming()
        
            self.nformed = 0

    def formingDelta(self):
        self.nformedDelta += 1

        if self.nformedDelta == len(self.next) and len(self.prev) > 0:
            s = [0] * self.nenter

            for e in range(self.nenter):
                s[e] = 0

                if len(self.next) == 0:
                    s[e] += self.output.exit[e] - self.solve.exit[e]

                for next in self.next:
                    diff = next.exitDelta[e]
                    s[e] += diff * self.exit[e] * next.get_synapse(self.id).weight

            self.exitDelta = s

            for prev in self.prev:
                prev.formingDelta()

    def update(self):
        self.nformedDelta = 0
        alpha = 0.05
        for prev in self.prev:
            r = 0
            for e in range(self.nenter):
                delta = self.exitDelta[e]
                input = prev.exit[e]
                r += input * delta

            weight = self.get_synapse(prev.id).weight
            r = weight - (alpha * r)
            self.set_synapse(prev.id, r)

    def selectActivFunc(self, activ):
        if activ == "sigmoid":
            self.activFunc = lambda x : 1/(1+math.exp(-x))
        if activ == "reLU":
            self.activFunc = lambda x : 0 if (x<=0) else x