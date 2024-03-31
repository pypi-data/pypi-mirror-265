# import common libraries
import sympy as sp

# import libraries
from common.inputParameters import InputParameters
from common.printer import Printer
from ecosystems.data.foodWebData import FoodWebData
from ecosystems.data.symbolicData import SymbolicData

# class stability (used for study the stability with combinations of proportions)
class Stability:

    # Initializing, receive io parameters and symbolic data
    def __init__(self, jacobian: sp.Matrix, symbolicData: SymbolicData, foodWebData: FoodWebData) -> None:
        # evaluate jacobian for foodWebData
        self.jacobianEvaluated = jacobian.subs(symbolicData.getFoodWebDataSubsValues(foodWebData))
        # also for initialBiomass
        self.jacobianEvaluated = self.jacobianEvaluated.subs(symbolicData.getBiomassSubsValues(foodWebData.initialBiomass))

    # check stability for the given combination of sd, sr and sl
    def checkStability(self, precission: int, sd: int, sr: int, sl: int)-> float:
        # first check if combination is valid (the sum of the three values must be the same of the precission)
        if ((sd + sr + sl) == precission):
            # combination is stable if maximum eigenValue is negative
            if (self.getMaximumEigenValue(sd / float(precission), sr / float(precission), sl / float(precission)) < 0):
                return 1.0
            else:
                return 0.0
        else:
            # invalid combination, raise exception
            raise Exception("invalid stability proportion: " + str(sd) + " " + str(sr) + " " + str(sl))

    # get maximum eigen value for the given proportion
    def getMaximumEigenValue(self, sd: float, sr: float, sl: float):
        # adjust jacobian with the given proportions
        jacobianProportions: sp.Matrix = self.jacobianEvaluated.subs({"s_d" : sd, "s_r" : sr, "s_l" : sl})
        # calculate eigen values
        eigenValues = jacobianProportions.eigenvals()
        # find the biggest real part of the eigenValues
        maxRe: float = None
        for eigenValue in eigenValues:
            # get real part of the eigen value
            re = sp.re(eigenValue)
            # continue depending of maxRe
            if (maxRe == None):
                maxRe = re
            elif (re > maxRe):
                maxRe = re
        # return the max eigen value
        return maxRe

    # jacobian (evaluated for foodWebData and initial biomass but NOT for proportions)
    jacobianEvaluated: sp.Matrix
