# import common libraries
import sympy as sp
from sympy.strategies.rl import subs

# import libraries
from common.inputParameters import InputParameters
from common.printer import Printer
from common import matrixOperations as mo
from ecosystems.analysis.donorControlModel import DonorControlModel
from ecosystems.data.foodWebData import FoodWebData
from ecosystems.data.symbolicData import SymbolicData
from ecosystems.proportions import Proportions
from ecosystems.analysis.steadyStates import SteadyStates
from ecosystems.analysis.stability import Stability
from ecosystems.controlSpaces.controlSpaceJacobian import ControlSpaceJacobian

# class general model (used for calculate all donor control parameters)
class GeneralModel:

    # initializing, receive io parameters and symbolic data
    def __init__(self, inputParameters: InputParameters, printer: Printer, symbolicData: SymbolicData, foodWebData: FoodWebData,
                 proportions: Proportions, donorControlModel: DonorControlModel) -> None:
        # calculate derivative
        self.calculateDerivative(inputParameters, printer, symbolicData, foodWebData, proportions, donorControlModel)
        # calculate jacobian
        self.calculateJacobian(inputParameters, printer, symbolicData, foodWebData, proportions, donorControlModel)
        # check if calculate steady states
        if (inputParameters.checkCalculateSteadyStates()):
            self.steadyStates = SteadyStates(inputParameters, printer, "GeneralModel", self.jacobian, symbolicData, foodWebData)
        else:
            self.steadyStates = None
        # check if analyze fixed points
        if (inputParameters.checkLocalStability):
            # calculate stability
            self.stability = Stability(self.jacobian, symbolicData, foodWebData)
            self.controlSpaceJacobian = ControlSpaceJacobian(printer, self.stability, foodWebData)
        else:
            self.stability = None
            self.controlSpaceJacobian = None

    # calculate general model derivative
    def calculateDerivative(self, inputParameters: InputParameters, printer: Printer, symbolicData: SymbolicData, foodWebData: FoodWebData,
                            proportions: Proportions, donorControlModel: DonorControlModel) -> None:
        # get common size n
        n: int = foodWebData.n
        # declare consumption matrix
        self.donorControlInitialConsumptionIntensity = sp.Matrix(sp.ZeroMatrix(n, n))
        self.recipientInitialConsumptionIntensity = sp.Matrix(sp.ZeroMatrix(n, n))
        self.mixedInitialConsumptionIntensity = sp.Matrix(sp.ZeroMatrix(n, n))
        # calculate consumptions
        for i in range(0, n):
            for j in range(0, n):
                self.donorControlInitialConsumptionIntensity[i,j] = (symbolicData.flowMatrix[i,j] / symbolicData.initialBiomass[j, 0])
                self.recipientInitialConsumptionIntensity[i,j] = (symbolicData.flowMatrix[i,j] / symbolicData.initialBiomass[i, 0])
                self.mixedInitialConsumptionIntensity[i,j] = (symbolicData.flowMatrix[i,j] / (symbolicData.initialBiomass[i, 0] * symbolicData.initialBiomass[j, 0]))
        # init total system flows
        self.donorControlTotalSystemFlows = sp.Matrix(sp.ZeroMatrix(n, 1))
        self.recipientTotalSystemFlows = sp.Matrix(sp.ZeroMatrix(n, 1))
        self.mixedTotalSystemFlows = sp.Matrix(sp.ZeroMatrix(n, 1))
        # calculate total system flows
        for i in range(0, n):
            # declare partial sums
            sumDonorControl = 0
            sumRecipient = 0
            sumMixed = 0
            for j in range(0, n):
                sumDonorControl += ((self.donorControlInitialConsumptionIntensity[i,j] * symbolicData.biomass[j, 0]) -
                                    (self.donorControlInitialConsumptionIntensity[j,i] * symbolicData.biomass[i, 0]))
                sumRecipient += ((self.recipientInitialConsumptionIntensity[i,j] * symbolicData.biomass[i, 0]) -
                                 (self.recipientInitialConsumptionIntensity[j,i] * symbolicData.biomass[j, 0]))
                sumMixed += ((self.mixedInitialConsumptionIntensity[i,j] * symbolicData.biomass[i, 0] * symbolicData.biomass[j, 0]) -
                             (self.mixedInitialConsumptionIntensity[j,i] * symbolicData.biomass[i, 0] * symbolicData.biomass[j, 0]))
            # add sums into total system flows
            self.donorControlTotalSystemFlows[i, 0] = sumDonorControl
            self.recipientTotalSystemFlows[i, 0] = sumRecipient
            self.mixedTotalSystemFlows[i, 0] = sumMixed
        # init total system flows
        self.totalSystemFlows = sp.Matrix(sp.ZeroMatrix(n, 1))
        # calculate total system flows
        for i in range(0, n):
            self.totalSystemFlows[i, 0] = ((proportions.s_d * self.donorControlTotalSystemFlows[i, 0]) +
                                           (proportions.s_r * self.recipientTotalSystemFlows[i, 0]) +
                                           (proportions.s_l * self.mixedTotalSystemFlows[i, 0]))
        # init derivative
        self.db_dt = sp.Matrix(sp.ZeroMatrix(n, 1))
        # calculate derivative
        for i in range(0, n):
            self.db_dt[i, 0] = self.totalSystemFlows[i, 0] - donorControlModel.outflows[i, 0] + symbolicData.imports[i, 0]
        # print info
        if (inputParameters.verbose or inputParameters.verboseGeneralModelDerivative):
            printer.printInfo("Calculating general model derivative for foodWebData '" + foodWebData.food_web_filename + "'")
            # donor control
            printer.printMatrixEvaluated(
                "Donor control initial consumption intensity",
                self.donorControlInitialConsumptionIntensity, symbolicData.getFoodWebDataSubsValues(foodWebData))
            printer.printMatrixEvaluated(
                "Donor control total system flows",
                self.donorControlTotalSystemFlows, symbolicData.getFoodWebDataSubsValues(foodWebData))
            # recipient
            printer.printMatrixEvaluated(
                "Recipient initial consumption intensity",
                self.recipientInitialConsumptionIntensity, symbolicData.getFoodWebDataSubsValues(foodWebData))
            printer.printMatrixEvaluated(
                "Recipient total system flows",
                self.recipientTotalSystemFlows, symbolicData.getFoodWebDataSubsValues(foodWebData))
            # mixed
            printer.printMatrixEvaluated(
                "Mixed initial consumption intensity",
                self.mixedInitialConsumptionIntensity, symbolicData.getFoodWebDataSubsValues(foodWebData))
            printer.printMatrixEvaluated(
                "Mixed total system flows",
                self.mixedTotalSystemFlows, symbolicData.getFoodWebDataSubsValues(foodWebData))
            # result
            printer.printMatrixEvaluated(
                "Total system flows",
                self.totalSystemFlows, symbolicData.getFoodWebDataSubsValues(foodWebData))
            printer.printMatrixEvaluated(
                "Derivative",
                self.db_dt, symbolicData.getFoodWebDataSubsValues(foodWebData))

    # calculate general model derivative
    def calculateJacobian(self, inputParameters: InputParameters, printer: Printer, symbolicData: SymbolicData, foodWebData: FoodWebData,
                          proportions: Proportions, donorControlModel: DonorControlModel) -> None:
        # check if use sympy jacobian method or calculate manually
        if inputParameters.useSympyJacobian:
            # calculate use sympy jacobian
            self.jacobian = self.db_dt.jacobian(symbolicData.biomass)
            # print info
            if (inputParameters.verbose or inputParameters.verboseGeneralModelJacobian):
                printer.printInfo("Calculating general model jacobian matrix for foodWebData '" + foodWebData.food_web_filename + "'")
                printer.printMatrixEvaluated(
                    "Jacobian (Sympy)",
                    self.jacobian, symbolicData.getFoodWebDataSubsValues(foodWebData))
        else:
            # get common size n
            n: int = foodWebData.n
            # init jacobian matrix
            self.jacobian = sp.Matrix(sp.ZeroMatrix(n, n))
            # calculate consumptions
            for i in range(0, n):
                for j in range(0, n):
                    if (i != j):
                        self.jacobian[i, j] = ((proportions.s_d * self.donorControlInitialConsumptionIntensity[i,j]) -
                                               (proportions.s_r * self.recipientInitialConsumptionIntensity[j,i]) +
                                               (proportions.s_l * (self.mixedInitialConsumptionIntensity[i, j] - self.mixedInitialConsumptionIntensity[j,i]) * symbolicData.biomass[i, 0]))
                    else:
                        # calculate sumatorial values
                        sumDonorControlInitialConsumptionIntensity = 0
                        sumRecipientControlInitialConsumptionIntensity = 0
                        sumMixed = 0
                        for k in range(0, n):
                            sumDonorControlInitialConsumptionIntensity += self.donorControlInitialConsumptionIntensity[k,i]
                            sumRecipientControlInitialConsumptionIntensity += self.recipientInitialConsumptionIntensity[i,k]
                            sumMixed += ((self.mixedInitialConsumptionIntensity[i, k] * symbolicData.biomass[k, 0]) -
                                         (self.mixedInitialConsumptionIntensity[k, i] * symbolicData.biomass[k, 0]))
                        # calculate jacobian value
                        self.jacobian[i, j] = ((proportions.s_d * (self.donorControlInitialConsumptionIntensity[i,i] - sumDonorControlInitialConsumptionIntensity)) +
                                               (proportions.s_r * (sumRecipientControlInitialConsumptionIntensity - self.recipientInitialConsumptionIntensity[i,i])) +
                                               (proportions.s_l * sumMixed) -
                                               (donorControlModel.unitsExport[i] + donorControlModel.unitsRespiration[i]))
            # print info
            if (inputParameters.verbose or inputParameters.verboseGeneralModelJacobian):
                printer.printInfo("Calculating general jacobian matrix for foodWebData '" + foodWebData.food_web_filename + "'")
                printer.printMatrixEvaluated(
                    "Jacobian",
                    self.jacobian, symbolicData.getFoodWebDataSubsValues(foodWebData))

    # donor control consumption intensity: F (/) bi
    donorControlInitialConsumptionIntensity: sp.Matrix

    # recipient consumption intensity: F (/) bj
    recipientInitialConsumptionIntensity: sp.Matrix

    # mixed consumption intesity: F (/) bi*bj
    mixedInitialConsumptionIntensity: sp.Matrix

    # donor control total system flows
    donorControlTotalSystemFlows: sp.Matrix

    # recipient total system flows
    recipientTotalSystemFlows: sp.Matrix

    # mixed total system flows
    mixedTotalSystemFlows: sp.Matrix

    # total system flow
    totalSystemFlows: sp.Matrix

    # derivative of b / derivative of t
    db_dt: sp.Matrix

    # jacobian matrix
    jacobian: sp.Matrix

    # steady States
    steadyStates: SteadyStates

    # domeig components
    stability: Stability

    # control space jacobian
    controlSpaceJacobian: ControlSpaceJacobian

    