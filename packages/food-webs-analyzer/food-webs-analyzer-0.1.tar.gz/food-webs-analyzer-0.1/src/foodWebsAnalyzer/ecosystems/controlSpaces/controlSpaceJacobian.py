# import numpy as np
import numpy as np

# import libraries
from ecosystems.analysis.stability import Stability
from ecosystems.data.foodWebData import FoodWebData
from common.printer import Printer

# class control space jacobian (used for calculate the control space based on jacobian)
class ControlSpaceJacobian:

    # Initializing, receive foodwebdata and stability module
    def __init__(self, printer: Printer, stability: Stability, foodWebData: FoodWebData):
        precission: int = 10
        # create range space between [0, precission]
        proportionRange = range(0, precission + 1)
        # declare cellIndex
        cellIndex = 0
        # iterate over all posible values of sd
        for sd in proportionRange:
            # iterate over all posible values of sr
            for sr in proportionRange:
                # derive sl from sd and sr
                sl = (precission - sd - sr)
                # check if combination is valid
                if ((sd + sr + sl) == precission):
                    # add values in vectors
                    self.sdValues.append(sd / float(precission))
                    self.srValues.append(sr / float(precission))
                    self.slValues.append(sl / float(precission))
                    # check stability for the given combination of sd, sr and sl
                    self.stabilityValues.append(stability.checkStability(precission, sd, sr, sl))          
            # update cellIndex
            cellIndex += 1
        # print proportion ternary
        printer.printProportionTernary("localStability-" + foodWebData.food_web_filename, foodWebData.food_web_filename, self.sdValues, self.srValues, self.slValues, self.stabilityValues)

    # sd values
    sdValues: list[float] = []

    # sr values
    srValues: list[float] = []

    # sl values
    slValues: list[float] = []    

    # stability values
    stabilityValues: list[float] = []      

    



