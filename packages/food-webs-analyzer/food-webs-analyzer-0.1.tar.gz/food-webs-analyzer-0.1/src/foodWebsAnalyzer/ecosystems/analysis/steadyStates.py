# import common libraries
import sympy as sp

# import libraries
from common.inputParameters import InputParameters
from common.printer import Printer
from common import matrixOperations as mo
from ecosystems.data.foodWebData import FoodWebData
from ecosystems.data.symbolicData import SymbolicData


# class Steady states (used for calculate steady states for donor control or general model)
class SteadyStates:

    # Initializing, receive io parameters and symbolic data
    def __init__(self, inputParameters: InputParameters, printer: Printer, steadyStateTypes: str, jacobian: sp.Matrix,
                 symbolicData: SymbolicData, foodWebData: FoodWebData) -> None:
        # first adjust proportions (all for donor)
        jacobianProportions: sp.Matrix = jacobian.subs({"s_d" : 1, "s_r" : 0, "s_l" : 0})
        # evaluate to obtain values
        evaluatedJacobian: sp.Matrix = jacobianProportions.subs(symbolicData.getFoodWebDataSubsValues(foodWebData))
        # use initial biomass
        evaluatedJacobian = evaluatedJacobian.subs(symbolicData.getBiomassSubsValues(foodWebData.getinitialBiomass()))
        # invert jacobian
        invertedJacobian: sp.Matrix = -1 * evaluatedJacobian.inv()
        # multiply by imports
        self.values: sp.Matrix = mo.product(invertedJacobian, foodWebData.imports)
        # save values in file
        printer.writeMatrixColumnMatLab(foodWebData.food_web_filename, "steadyStates" + steadyStateTypes + ".m", "b", self.values)
        # print info
        if (inputParameters.verbose or inputParameters.verboseSteadyStates):
            printer.printInfo(steadyStateTypes + " steady states for foodWebData '" + foodWebData.food_web_filename + "'")
            printer.printMatrix(steadyStateTypes + " jacobian", jacobian)
            printer.printMatrix(steadyStateTypes + " jacobian proportions", jacobianProportions)
            printer.printMatrix(steadyStateTypes + " jacobian evaluated", evaluatedJacobian)
            printer.printMatrix(steadyStateTypes + " jacobian inverted", invertedJacobian)
            printer.printMatrix(steadyStateTypes + " steady state values", self.values)

    # steady states (evaluated)
    values: sp.Matrix
