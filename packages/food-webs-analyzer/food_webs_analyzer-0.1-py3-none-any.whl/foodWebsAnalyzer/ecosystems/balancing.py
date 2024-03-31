# import common libraries
import sympy as sp

# import libraries
from common.inputParameters import InputParameters
from common.printer import Printer
from ecosystems.data.foodWebData import FoodWebData


# class balancing (using for check if the given biomass is balanced)
class Balancing:

    # Initializing
    def __init__(self, inputParameters: InputParameters, printer: Printer, foodWebData: FoodWebData) -> None:
        print("test")