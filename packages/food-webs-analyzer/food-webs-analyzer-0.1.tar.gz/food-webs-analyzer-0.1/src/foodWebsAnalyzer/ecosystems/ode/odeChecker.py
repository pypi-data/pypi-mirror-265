# import common libraries
import sympy as sp

# import libraries
from common.inputParameters import InputParameters
from common.printer import Printer
from ecosystems.data.foodWebData import FoodWebData
from ecosystems.analysis.steadyStates import SteadyStates
from ecosystems.analysis.generalModel import GeneralModel


# class ODEChecker (used for check ODE results)
class ODEChecker:

    # Initializing, receive input parameters, printer, ode solver and steadyStates
    def __init__(self, inputParameters: InputParameters, printer: Printer, foodWebData: FoodWebData,
                 biomassFinal: sp.Matrix, generalModel: GeneralModel) -> None:
        # first check if steady states was calculated
        if (generalModel.steadyStates != None):
            # declare matrix with the differences between steadyStates and solver results
            differenceMatrix = sp.Matrix(sp.ZeroMatrix(foodWebData.n, 1))
            for i in range(0, len(generalModel.steadyStates.values)):
                if (generalModel.steadyStates.values[i,0] > biomassFinal[i,0]):
                    differenceMatrix[i,0] = (generalModel.steadyStates.values[i,0] - biomassFinal[i,0])
                else:
                    differenceMatrix[i,0] = (biomassFinal[i,0] - generalModel.steadyStates.values[i,0])
            # print info
            if (inputParameters.verbose or inputParameters.verboseGeneralModelODEChecker):
                printer.printInfo("Checking ODE Results for foodWebData '" + foodWebData.food_web_filename + "'")
                printer.printMatrix("Differences between steadyStates and ODE results", differenceMatrix)
                printer.printGraphMatrix(differenceMatrix)
