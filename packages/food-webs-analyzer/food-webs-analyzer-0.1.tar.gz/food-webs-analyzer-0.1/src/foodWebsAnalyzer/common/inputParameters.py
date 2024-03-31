# import common libraries
import random as rd
import shutil
import os

# class input parameters (used for read and store console input parameters)
class InputParameters:

    # Initializing
    def __init__(self, arguments: list[str]):
        # iterate over arguments and set potions
        for i in range(0, len(arguments)):
            # general parameters
            if (arguments[i] == "--dataFolder"):
                self.dataFolder = arguments[i + 1]
            elif (arguments[i] == "--customFiles"):
                self.customFiles = arguments[i + 1]
            elif (arguments[i] == "--outputFolder"):
                self.outputFolder = arguments[i + 1]
            elif ((arguments[i] == "--tn") or (arguments[i] == "--timeEnd")):
                self.timeEnd = float(arguments[i + 1])
            elif (arguments[i] == "--randomSeed"):
                self.randomSeed = float(arguments[i + 1])
            # processing parameters
            elif (arguments[i] == "--symbolic"):
                self.numerical = False
            elif (arguments[i] == "--numerical"):
                self.numerical = True
            elif (arguments[i] == "--useManualJacobian"):
                self.useSympyJacobian = False
            elif (arguments[i] == "--useSympyJacobian"):
                self.useSympyJacobian = True
            # tasks
            elif (arguments[i] == "--checkBalancing"):
                self.checkBalancing = True
            elif (arguments[i] == "--calculateDonorControlModel"):
                self.calculateDonorControlModel = True
            elif (arguments[i] == "--calculateGeneralModel"):
                self.calculateGeneralModel = True
                self.calculateDonorControlModel = True  # needed for general model
            elif (arguments[i] == "--checkLocalStability"):
                self.checkLocalStability = True
                self.calculateGeneralModel = True       # needed for jacobian control space
                self.calculateDonorControlModel = True  # needed for general model
                self.numerical = True                   # in this mode, always use numerical
            elif (arguments[i] == "--calculateBiomassDynamic"): # change to local stability
                self.calculateBiomassDynamic = True
                self.calculateGeneralModel = True       # needed for jacobian control space
                self.calculateDonorControlModel = True  # needed for general model
                self.numerical = True                   # in this mode, always use numerical
            elif (arguments[i] == "--checkGlobalStability"):
                self.checkGlobalStability = True
            # proportions
            elif (arguments[i] == "--proportion-sd"):
                self.proportionSd = float(arguments[i + 1])
            elif (arguments[i] == "--proportion-sr"):
                self.proportionSr = float(arguments[i + 1])
            # ODE
            elif (arguments[i] == "--ODESolver"):
                self.ODESolver = arguments[i + 1] 
            elif (arguments[i] == "--exportODETable"):
                self.exportODETable = True
            # output plain
            elif (arguments[i] == "--verbose"):
                # enable verbose output for all elements
                self.verbose = True
            elif (arguments[i] == "--verbose-inputFile"):
                # enable verbose output about inputFile
                self.verboseInputFile = True
            elif (arguments[i] == "--verbose-donorControlDerivative"):
                # enable verbose output about donor control derivative
                self.verboseDonorControlDerivative = True
            elif (arguments[i] == "--verbose-donorControlFixedPoints"):
                # enable verbose output about donor control fixed points
                self.verboseDonorControlFixedPoints = True
            elif (arguments[i] == "--verbose-donorControlJacobian"):
                # enable verbose output about donor control jacobian
                self.verboseDonorControlJacobian = True
            elif (arguments[i] == "--verbose-generalModelDerivative"):
                # enable verbose output about general model derivative
                self.verboseGeneralModelDerivative = True
            elif (arguments[i] == "--verbose-generalModelJacobian"):
                # enable verbose output about general model jacobian
                self.verboseGeneralModelJacobian = True
            elif (arguments[i] == "--verbose-steadyStates"):
                # enable verbose output about steady states
                self.verboseSteadyStates = True
            elif (arguments[i] == "--verbose-generalModelODE"):
                # enable verbose output about general model ODE
                self.verboseGeneralModelODE = True
            elif (arguments[i] == "--verbose-generalModelODEChecker"):
                # enable verbose output about general model ODE checker
                self.verboseGeneralModelODEChecker = True
            # output plain file
            elif (arguments[i] == "--outputPlainFile"):
                self.outputPlainFile = arguments[i + 1]
            elif (arguments[i] == "--outputODEResults"):
                self.outputODEResults = arguments[i + 1]
            # output latex
            elif (arguments[i] == "--outputLatexFile"):
                self.outputLatexFile = arguments[i + 1]
            elif (arguments[i] == "--latexMode"):
                self.latexMode = arguments[i + 1]
            # output images
            elif (arguments[i] == "--saveSVG"):
                self.saveSVG = True
            elif (arguments[i] == "--dpi"):
                self.dpi = int(arguments[i + 1])
        # check proportions values
        if ((self.proportionSd < 0) + (self.proportionSd > 1)):
            raise Exception("invalid donor-control proportion")
        elif ((self.proportionSr < 0) + (self.proportionSr > 1)):
            raise Exception("invalid recipient proportion")
        elif ((1 - self.proportionSd - self.proportionSr) < 0):
            raise Exception("invalid lotka-volterra proportion")
        # clear and init output directory
        if os.path.isdir(self.outputFolder):
            shutil.rmtree(self.outputFolder)
        os.mkdir(self.outputFolder)
        # init random
        rd.seed(self.randomSeed)

    # check if steady states can be calculated
    def checkCalculateSteadyStates(self) -> bool:
        return (self.proportionSd == 1 and self.proportionSr == 0)

    # data folder
    dataFolder: str = os.getcwd() + "/../data";

    # check if process only a certain file (placed in dat folder)
    customFiles: str = ""

    # output folder (by default the same directory)
    outputFolder: str = "out"

    # time end (by default 100)
    timeEnd: float = 100

    # random seed (by default None)
    randomSeed: float = None

    # check if the input data is balanced
    checkBalancing: bool = False

    # calculate donor control model
    calculateDonorControlModel: bool = False

    # calculate general model
    calculateGeneralModel: bool = False

    # calculate jacobian control space
    checkLocalStability: bool = False

    # calculate biomass dynamic
    calculateBiomassDynamic: bool = False

    # global stability
    checkGlobalStability: bool = False

    # check if use numerical mode (more quickly in the calculation of general model)
    numerical: bool = False

    # check if use sympy jacobian
    useSympyJacobian: bool = True;

    # set proportion donor-control
    proportionSd: float = 0.7;

    # set proportion recipient
    proportionSr: float = 0.2;

    # ODE solver
    ODESolver: str = "RK45"

    # export ODE table
    exportODETable: bool = False

    # verbose output. Enable ALL output info
    verbose: bool = False;

    # verbose for input file
    verboseInputFile: bool = False;

    # verbose for specific donor control derivative
    verboseDonorControlDerivative: bool = False;

    # verbose for specific donor control fixed points
    verboseDonorControlFixedPoints: bool = False;

    # verbose for specific donor control jacobian
    verboseDonorControlJacobian: bool = False;

    # verbose for specific general model derivative
    verboseGeneralModelDerivative: bool = False;

    # verbose for specific general model jacobian
    verboseGeneralModelJacobian: bool = False;

    # verbose for specific steady states
    verboseSteadyStates: bool = False;

    # verbose for specific general model ODE
    verboseGeneralModelODE: bool = False;

    # verbose for specific general model ODE Checker
    verboseGeneralModelODEChecker: bool = False;

    # output file
    outputPlainFile: str = ""

    # output ODE results
    outputODEResults: str = ""

    # wrap line in output
    wrapLine: bool = False

    # output latex file
    outputLatexFile: str = ""

    # latex mode
    latexMode: str = "equation*";

    # save as svg
    saveSVG: bool = False

    # dpi resolution for images
    dpi: int = 1200

    # latex order
    latexOrder: str = "none";

    # variable used if the stock falls below a product of initial stock and Delta we treat it as extinct
    delta: float = 0

    # maximum time
    t_max: float = 1e4;
