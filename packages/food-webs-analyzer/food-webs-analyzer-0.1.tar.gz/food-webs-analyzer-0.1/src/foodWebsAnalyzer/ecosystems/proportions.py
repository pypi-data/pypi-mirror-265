# import common libraries
import sympy as sp

# class proportions (used for store all proportion parameters)
class Proportions:

    # Initializing
    def __init__(self) -> None:
        # init symbols
        self.s_d = sp.Symbol("s_d")
        self.s_r = sp.Symbol("s_r")
        self.s_l = sp.Symbol("s_l")

    # get dictionary with all equivalences of symbols for the given proportions
    def getProportionSubsValues(self, s_d: float, s_r: float) -> dict:
        return {"s_d" : s_d, "s_r" : s_r, "s_l" : float(1.0 - s_d - s_r)}

    # donor-control parameter
    s_d: sp.Symbol

    # recipient controlled parameter
    s_r: sp.Symbol

    # lotka_volterra parameter
    s_l: sp.Symbol