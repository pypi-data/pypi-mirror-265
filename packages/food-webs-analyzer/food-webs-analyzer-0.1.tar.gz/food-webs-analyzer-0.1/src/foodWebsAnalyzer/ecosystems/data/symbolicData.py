# import common libraries
import sympy as sp

# import libraries
from ecosystems.data.foodWebData import FoodWebData
from common.inputParameters import InputParameters

# symbolic elements used in foodWebData
class SymbolicData:

    # Initializing, receive n
    def __init__(self, inputParameters: InputParameters, foodWebData: FoodWebData):
        # declare n
        n: int = foodWebData.n
        # use matrix symbol for F
        self.flowMatrix = sp.Matrix(sp.MatrixSymbol('F', n, n))
        # use vectors for the rest of elements
        self.initialBiomass = sp.Matrix(sp.ZeroMatrix(n, 1))
        self.imports = sp.Matrix(sp.ZeroMatrix(n, 1))
        self.exports = sp.Matrix(sp.ZeroMatrix(n, 1))
        self.respiration = sp.Matrix(sp.ZeroMatrix(n, 1))
        self.biomass = sp.Matrix(sp.ZeroMatrix(n, 1))
        # iterate over n values
        for i in range (0, n):
            # check if use numerical values instead symbols
            if (inputParameters.numerical):
                self.initialBiomass[i] = foodWebData.initialBiomass[i,0]
                self.imports[i] = foodWebData.imports[i,0]
                self.exports[i] = foodWebData.exports[i,0]
                self.respiration[i] = foodWebData.respiration[i,0]
                for j in range(0, n):
                    self.flowMatrix[i, j] = foodWebData.flowMatrix[i, j]
            else:
                self.initialBiomass[i] = sp.Symbol("b^*_" + str(i))
                self.imports[i] = sp.Symbol("p" + str(i))
                self.exports[i] = sp.Symbol("q_" + str(i))
                self.respiration[i] = sp.Symbol("r_" + str(i))
            # biomass uses always symbols
            self.biomass[i] = sp.Symbol("b_" + str(i))

    # get dictionary with all equivalences of symbols for the given foodWebData and initial biomass
    def getFoodWebDataSubsValues(self, foodWebData: FoodWebData) -> dict:
        solution = {}
        for i in range(0, foodWebData.n):
            solution[self.initialBiomass[i]] = foodWebData.initialBiomass[i, 0]
            solution[self.imports[i]] = foodWebData.imports[i, 0]
            solution[self.exports[i]] = foodWebData.exports[i, 0]
            solution[self.respiration[i]] = foodWebData.respiration[i, 0]
            for j in range(0, foodWebData.n):
                solution[self.flowMatrix[i, j]] = foodWebData.flowMatrix[i, j]
        return solution

    # get dictionary with all equivalences of symbols for the given foodWebData but with perturbated initialbiomass
    def getPerturbatedFoodWebDataSubsValues(self, foodWebData: FoodWebData, sampleIndex: int) -> dict:
        solution = {}
        for i in range(0, foodWebData.n):
            solution[self.initialBiomass[i]] = foodWebData.perturbatedInitialBiomass[sampleIndex][i, 0]
            solution[self.imports[i]] = foodWebData.imports[i, 0]
            solution[self.exports[i]] = foodWebData.exports[i, 0]
            solution[self.respiration[i]] = foodWebData.respiration[i, 0]
            for j in range(0, foodWebData.n):
                solution[self.flowMatrix[i, j]] = foodWebData.flowMatrix[i, j]
        return solution

    # get dictionary with all equivalences of symbols for the given biomass
    def getBiomassSubsValues(self, biomassVector: list[float]) -> dict:
        solution = {}
        for i in range(0, len(biomassVector)):
            solution[self.biomass[i]] = biomassVector[i]
        return solution

    # get biomass variables in list format
    def getBiomassVariables(self) -> list[sp.Symbol]:
        solution: list[sp.Symbol] = []
        for i in range (0, self.biomass.rows):
            solution.append(self.biomass[i, 0])
        return solution

    # flows of biomass matrix (given)
    flowMatrix: sp.Matrix

    # initial biomass stock vector for every species matrix (given)
    initialBiomass: sp.Matrix

    # perturbated initial biomass stock vector for every species matrix (calculated based on initialBiomass)
    perturbatedInitialBiomass: sp.Matrix

    # imports vector (given)
    imports: sp.Matrix

    # exports vector (given)
    exports: sp.Matrix

    # respiration vector (given)
    respiration: sp.Matrix

    # biomass stock vector for every species matrix (unknowns)
    biomass: sp.Matrix