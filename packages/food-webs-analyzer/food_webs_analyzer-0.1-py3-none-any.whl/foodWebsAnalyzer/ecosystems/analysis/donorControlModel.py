# import common libraries
import sympy as sp

# import libraries
from common.inputParameters import InputParameters
from common.printer import Printer
from common import matrixOperations as mo
from ecosystems.data.foodWebData import FoodWebData
from ecosystems.data.symbolicData import SymbolicData
from ecosystems.analysis.steadyStates import SteadyStates

# class donor control model (used for calculate all donor control parameters)
class DonorControlModel:

    # initializing, receive io parameters and symbolic data
    def __init__(self, inputParameters: InputParameters, printer: Printer, symbolicData: SymbolicData, foodWebData: FoodWebData) -> None:
        # calculate derivative
        self.calculateDerivative(inputParameters, printer, symbolicData, foodWebData)
        # calculate fixed points
        self.calculateFixedPoints(inputParameters, printer, symbolicData, foodWebData)
        # calculate jacobian
        self.calculateJacobian(inputParameters, printer, symbolicData, foodWebData)
        # calculate steady states
        self.steadyStates = SteadyStates(inputParameters, printer, "DonorControl", self.jacobian, symbolicData, foodWebData)

    # calculate donor control model derivative
    def calculateDerivative(self, inputParameters: InputParameters, printer: Printer, symbolicData: SymbolicData, foodWebData: FoodWebData) -> None:
        # initial consumption intensity matrix: F (/) b0
        self.initialConsumptionIntensity = mo.hadamard_division_vector(symbolicData.flowMatrix, symbolicData.initialBiomass);
        # consumption intensity vector: sum(.x)(initialConsumptionIntensity)
        self.consumptionIntensity = mo.sumatorial_dotx(self.initialConsumptionIntensity)
        # system inflows vector: initialConsumptionIntensity * b
        self.systemInflows = mo.product(self.initialConsumptionIntensity, symbolicData.biomass)
        # system outflows vector: consumptionIntensity (*) b
        self.systemOutflows = mo.hadamard_product(self.consumptionIntensity, symbolicData.biomass)
        # total system flows: systemInflows - systemOutflows
        self.totalSystemFlows = mo.substract(self.systemInflows, self.systemOutflows)
        # units export: q (/) b0
        self.unitsExport = mo.hadamard_division(symbolicData.exports, symbolicData.initialBiomass)
        # units respiration: r (/) b0
        self.unitsRespiration = mo.hadamard_division(symbolicData.respiration, symbolicData.initialBiomass)
        # outflows: (unitsExport + unitsRespiration) * b
        self.outflows = mo.hadamard_product(mo.add(self.unitsExport, self.unitsRespiration), symbolicData.biomass)
        # calculate d(b)/d(t): totalSystemFlows - outflows + imports
        self.db_dt = mo.add(mo.substract(self.totalSystemFlows, self.outflows), symbolicData.imports)
        # print info
        if (inputParameters.verbose or inputParameters.verboseDonorControlDerivative):
            printer.printInfo("Calculating donor control model derivative for foodWebData '" + foodWebData.food_web_filename + "'")
            # get dictionary with food web data subs values
            foodWebDataSubsValues = symbolicData.getFoodWebDataSubsValues(foodWebData)
            printer.printMatrixEvaluated(
                "Initial consumption intensity matrix: F (/) b0",
                self.initialConsumptionIntensity, foodWebDataSubsValues)
            printer.printMatrixEvaluated(
                "Consumption intensity vector: sum(.x)(initialConsumptionIntensity)",
                self.consumptionIntensity, foodWebDataSubsValues)
            printer.printMatrixEvaluated(
                "System inflows vector: initialConsumptionIntensity * b",
                self.systemInflows, foodWebDataSubsValues)
            printer.printMatrixEvaluated(
                "System outflows vector: consumptionIntensity (*) b",
                self.systemOutflows, foodWebDataSubsValues)
            printer.printMatrixEvaluated(
                "Total system flows: systemInflows - systemOutflows",
                self.totalSystemFlows, foodWebDataSubsValues)
            printer.printMatrixEvaluated(
                "Units export: q (/) b0",
                self.unitsExport, foodWebDataSubsValues)
            printer.printMatrixEvaluated(
                "Units respiration: r (/) b0",
                self.unitsRespiration, foodWebDataSubsValues)
            printer.printMatrixEvaluated(
                "Outflows: (unitsExport + unitsRespiration) * b",
                self.outflows, foodWebDataSubsValues)
            printer.printMatrixEvaluated(
                "d(b)/d(t): totalSystemFlows - outflows + imports",
                self.db_dt, foodWebDataSubsValues)

    # calculate donor control fixed points
    def calculateFixedPoints(self, inputParameters: InputParameters, printer: Printer, symbolicData: SymbolicData, foodWebData: FoodWebData) -> None:
        # evaluate parameters in db_dt
        db_dt_evaluated: sp.Matrix = self.db_dt.subs(symbolicData.getFoodWebDataSubsValues(foodWebData))
        # calculate donor control fixed points: evaluate initial biomass in db_dt_evaluated (b = b0)
        self.fixedPoints = db_dt_evaluated.subs(symbolicData.getBiomassSubsValues(foodWebData.getinitialBiomass()))
        # print info
        if (inputParameters.verbose or inputParameters.verboseDonorControlFixedPoints):
            printer.printInfo("Calculating donor control model fixed points for '" + foodWebData.food_web_filename + "'")
            printer.printMatrix("Fixed points(b = b0):", self.fixedPoints)

    # calculate donor control Jacobian
    def calculateJacobian(self, inputParameters: InputParameters, printer: Printer, symbolicData: SymbolicData, foodWebData: FoodWebData) -> None:
        # first check if use sympy jacobian method or calculate manually
        if inputParameters.useSympyJacobian:
            # calculate use sympy jacobian
            self.jacobian = self.db_dt.jacobian(symbolicData.biomass)
            # print info
            if (inputParameters.verbose or inputParameters.verboseDonorControlJacobian):
                printer.printInfo("Calculating donor control model jacobian matrix for foodWebData '" + foodWebData.food_web_filename + "'")
                printer.printMatrixEvaluated(
                    "Jacobian (Sympy)",
                    self.jacobian,
                    symbolicData.getFoodWebDataSubsValues(foodWebData))
        else:
            # get the sume of units exports and respirations
            exportUnits : sp.Matrix = mo.add(self.unitsExport, self.unitsRespiration)
            # calculate diagonal matrix of the sumo of consumption intensity and outflows
            diagonal: sp.Matrix = mo.diagonal(mo.add(self.consumptionIntensity, exportUnits));
            # calculate jacobian substracting the calculated diagonal to the consumptionIntensity matrix
            self.jacobian = mo.substract(self.initialConsumptionIntensity, diagonal)
            # print info
            if (inputParameters.verbose or inputParameters.verboseDonorControlJacobian):
                printer.printInfo("Calculating donor control model jacobian matrix for foodWebData '" + foodWebData.food_web_filename + "'")
                # get dictionary with food web data subs values
                foodWebDataSubsValues = symbolicData.getFoodWebDataSubsValues(foodWebData)
                printer.printMatrixEvaluated(
                    "Diagonal: consumptionIntensity + outflows",
                    diagonal, foodWebDataSubsValues)
                printer.printMatrixEvaluated(
                    "Jacobian: initialConsumptionIntensity - diagonal",
                    self.jacobian, foodWebDataSubsValues)

    # initial consumption intensity matrix: F (/) b0
    initialConsumptionIntensity: sp.Matrix

    # consumption intensity vector: sum(.x)(initialConsumptionIntensity)
    consumptionIntensity: sp.Matrix

    # system inflows vector: initialConsumptionIntensity * b
    systemInflows: sp.Matrix

    # system outflows vector: consumptionIntensity (*) b
    systemOutflows: sp.Matrix

    # total system flows: systemInflows - systemOutflows
    totalSystemFlows: sp.Matrix

    # units exports: q (/) b0
    unitsExport: sp.Matrix

    # units respiration: r (/) b0
    unitsRespiration: sp.Matrix

    # outflows: (unitsExport + unitsRespiration) * b
    outflows: sp.Matrix

    # derivative of b / derivative of t
    db_dt: sp.Matrix

    # fixed points
    fixedPoints: sp.Matrix

    # jacobian matrix
    jacobian: sp.Matrix

    # steady States
    steadyStates: SteadyStates