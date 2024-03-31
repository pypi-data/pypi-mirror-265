# import common libraries
from dataclasses import dataclass
import sympy as sp
import numpy as np
import random as rd

# import libraries
from common.inputParameters import InputParameters
from common.printer import Printer

# class food web data (used for read input files)
class FoodWebData:

    # Initializing, receive filename and fill all food web data
    def __init__(self, inputParameters: InputParameters, printer: Printer, fileName: str, customInitialBiomass: bool):
        # read data
        with open(inputParameters.dataFolder + "/" + fileName, 'r') as file:
            # read file, remove all \n and split using ;
            data = file.read().split(';')
        # get food web filename
        self.food_web_filename = self.parseString(data[0])
        # get CRC checker
        self.crc = self.parseString(data[1])
        # get matrix size)
        self.n = self.parseInt(data[2])
        # get lived species
        self.liveSpecies = self.parseInt(data[3])
        # get biomass stock for every species vector
        self.initialBiomass = self.parseColumnMatrix(data[4], self.n)
        # use intial biomass as current biomass
        self.biomass = self.parseColumnMatrix(data[4], self.n)
        # get imports vector
        self.imports = self.parseColumnMatrix(data[5], self.n)
        # get exports vector
        self.exports = self.parseColumnMatrix(data[6], self.n)
        # get respiration vector
        self.respiration= self.parseColumnMatrix(data[7], self.n)
        # get matrix flows of biomass
        self.flowMatrix = self.parseMatrix(data[8], self.n)
        # check if load customInitialBiomass (always in file customInitialBiomass.m)
        if (customInitialBiomass):
            # clear data
            data.clear()
            # read data
            with open(folder + "/customInitialBiomass.m", 'r') as file:
                # read file, remove all \n and split using ;
                data = file.read().split(';')
            # get custom initial biomass
            self.initialBiomass = self.parseColumnMatrix(data[0], self.n)
        # print info
        if (inputParameters.verbose or inputParameters.verboseInputFile):
            printer.printInfo("Parsed data from '" + self.food_web_filename + "'")
            printer.printInfo("-CRC '" + self.crc + "'")
            printer.printInfo("-Matrix size (n) '" + str(self.n) + "'")
            printer.printInfo("-Nodes / compartiments (l) '" + str(self.liveSpecies) + "'")
            printer.printMatrix("-Initial biomass (bo):", self.initialBiomass)
            printer.printMatrix("-Biomass (b):", self.biomass)
            printer.printMatrix("-Imports (p):", self.imports)
            printer.printMatrix("-Exports (q):", self.exports)
            printer.printMatrix("-Respiration (r):", self.respiration)
            printer.printMatrix("-Flow matrix (F):", self.flowMatrix)

    # parse string
    def parseString(self, dataStr: str) -> str:
        # check if print more info
        return dataStr.split("'")[1]

    # parse int
    def parseInt(self, dataStr: str) -> int:
        # remove all \n and spaces
        dataStr = dataStr.replace('\n', '').replace(' ', '');
        # remove first part
        dataStr = dataStr[dataStr.find('=') + 1:]
        # transform to string
        return int(dataStr);

    # parse column Matrix
    def parseColumnMatrix(self, dataStr: str, n: int) -> sp.Matrix:
        # replace all end of lines by spaces
        dataStr = dataStr.replace('\n', ' ')
        # take all elements between []
        dataStr = dataStr[dataStr.find('[') + 1:dataStr.find(']')]
        # split vector
        vectorStr = dataStr.split(" ")
        # convert vector in floats
        vector = []
        for elementStr in vectorStr:
            # avoid empty elementStr
            if (len(elementStr) > 0):
                # simpify element
                vector.append(sp.sympify(elementStr))
        # check size before returning
        if (len(vector) != n):
            raise Exception("Error parsing " + self.food_web_filename + ". Vector size is different of expected size " + str(n))
        # return column vector Matrix
        return sp.diag(vector);

    # parse n*n matrix
    def parseMatrix(self, dataStr: str, n: int) -> sp.Matrix:
        # first parse row matrix
        rowMatrix = self.parseColumnMatrix(dataStr, n * n)
        # return matrix
        return sp.Matrix(n, n, rowMatrix);

    # get initial biomass in list format
    def getinitialBiomass(self) -> list[float]:
        solution: list[float] = []
        for i in range (0, self.biomass.rows):
            solution.append(self.biomass[i, 0])
        return solution

    # calculate perturbated initial biomass
    def calculatePerturbatedInitialBiomass(self, inputParameters: InputParameters) -> None:
        # declare zero matrix
        self.perturbatedInitialBiomass = sp.Matrix(sp.ZeroMatrix(self.n, 1))
        # iterate over initial biomass
        for i in range (0, self.initialBiomass.rows):
            # get random number
            randomNumber: float = float(rd.randint(0, 1000))
            mu: float = np.log(float(self.initialBiomass[i, 0]) / np.sqrt(1 + (randomNumber * randomNumber)))
            sigma: float = np.sqrt(np.log(1 + (randomNumber * randomNumber)))
            # calculate perturbation using lognormal
            self.perturbatedInitialBiomass[i, 0] = self.initialBiomass[i, 0] * np.random.lognormal(mu, sigma)

    # food web filename
    food_web_filename = ""

    # CRC checker
    crc = ""

    # matrix size (represents species and detritus)
    n: int = 0

    # live species represented in matrix (normally n-1)
    liveSpecies: int = 0

    # initial biomass stock for every species matrix (size n*1)
    initialBiomass: sp.Matrix

    # perturbated initial biomass stock for every species matrix (list of matrix of size n*1)
    perturbatedInitialBiomass: sp.Matrix

    # biomass stock for every species matrix (size n*1)
    biomass: sp.Matrix

    # imports matrix (size n*1)
    imports: sp.Matrix

    # exports matrix (size n*1)
    exports: sp.Matrix

    # respiration matrix (special export, size n*1)
    respiration: sp.Matrix

    # flows of biomass matrix (size n*n)
    flowMatrix: sp.Matrix