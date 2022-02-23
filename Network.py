
from Perceptron import Perceptron, Synapse
import random
import copy

class Network:

    nenter = 0
    input = []
    output = []
    solve = []

    perceptron = []
    pos = []
    activ = []

    def __init__(self, descFileName, structFileName, initValue, nenter) -> None:
        self.nenter = nenter
        self.fillInNetwork(descFileName, structFileName)
        self.generatesPreceptron()
        self.initValueRandom()

    def fillInNetwork(self, descFileName, structFileName):
        descFile = open(descFileName, "r")
        descLines = descFile.readlines()

        self.nPerceptron = int(descLines[3].split("//")[0])
        self.input = self.fm(descLines[4])
        self.output = self.fm(descLines[5])
        self.solve = self.fm(descLines[6])

        structFile = open(structFileName, "r")
        structLines = structFile.readlines()
        
        for ligne in structLines:
            data = ligne.split("//")[0].split(";")
            self.activ.append(data[0])
            self.pos.append([int(numeric_string) for numeric_string in data[1:]])

    def fm(self, txt):
        return [int(numeric_string) for numeric_string in txt.split("//")[0].split(";")]


    def generatesPreceptron(self):
        for n in range(self.nPerceptron):
            perceptron = Perceptron(n, self.nenter, self.activ[n])
            self.perceptron.append(perceptron)
            for enter in range(self.nenter):
                self.perceptron[n].exit.append(0)
                self.perceptron[n].exitDelta.append(0)

        for n in range(self.nPerceptron):
            for pos in self.pos[n]:
                if pos != -42:
                    self.perceptron[n].next.append(self.perceptron[pos])
                    self.perceptron[pos].prev.append(self.perceptron[n])
                    self.perceptron[pos].synapses.append(Synapse(self.perceptron[n].id))
                print("Neural:" + str(n) + " -> " + str(pos))
            
        for perceptron in self.perceptron:
            for output in self.output:
                perceptron.output = self.perceptron[output]
            for solve in self.solve:
                perceptron.solve = self.perceptron[solve]

    def initValueRandom(self):
        for perceptron in self.perceptron:
            for prev in range(len(perceptron.prev)):
                perceptron.synapses[prev].weight = random.random()

    def inputData(self):
        for i in range(self.nenter):
            for inpt in self.input:
                self.perceptron[inpt].exit[i] = float(input(str(i) + "x" + str(inpt) + ": "))
            
            for solve in self.solve:    
                self.perceptron[solve].exit[i] = float(input("y" + str(i) + ": "))
    
    def inputDataCsv(self, filename):
        lines = open(filename, "r").readlines()
        lines.pop(0)
        for n in range(len(lines)):
            data = lines[n].split(";")
            for i in range(len(self.input)):
                self.perceptron[self.input[i]].exit[n] =  float(data[i])
            
            for i in range(len(self.solve)):
                self.perceptron[self.solve[i]].exit[n] =  float(data[len(self.input) + i])

    def train(self,iter):
        err = 0
        for i in range(iter):
            err = 0
            for input in self.input:
                for next in self.perceptron[input].next:
                    next.forming()
            for enter in range(self.nenter):
                err += abs(self.perceptron[self.output[0]].exit[enter] - self.perceptron[self.solve[0]].exit[enter])
            print(err)
            for output in self.output:
                self.perceptron[output].nformedDelta = len(self.perceptron[output].next) - 1
                self.perceptron[output].formingDelta() 

            for perceptron in self.perceptron[:-1]:
                perceptron.update()
        print(err)

    def testNetwork(self):
        perceptronTEST = copy.deepcopy(self.perceptron)
        for inpt in self.input:
            perceptronTEST[inpt].exit[0] = float(input("X" + str(inpt) + ": "))

        for inpt in self.input:
            for next in perceptronTEST[inpt].next:
                next.forming()
        
        print(perceptronTEST[self.output[0]].exit[0])

    def testNetworkCsv(self, filename):
        perceptronTEST = copy.deepcopy(self.perceptron)

        lines = open(filename, "r").readlines()
        lines.pop(0)
        for n in range(len(lines)):
            data = lines[n].split(";")
            for i in range(len(self.input)):
                perceptronTEST[self.input[i]].exit[n] =  float(data[i])

        for inpt in self.input:
            for next in perceptronTEST[inpt].next:
                next.forming()
        
        print(perceptronTEST[self.output[0]].exit)