import sympy as sp
import typing as tp
import scipy as sc # type: ignore
import numpy as np # type: ignore

# solve ode using scipy function "solve_ivp"
def solveNonLinearOde(ODEMethod: str, equations: list[tp.Any], symbols: list[sp.Symbol], initialValues: list[float], tn: float, numPoints: int) -> sc.integrate._ivp.ivp.OdeResult:
    # declare time variable
    t: sp.Symbol = sp.symbols('t')
    # Convert the SymPy symbolic expression for ydot into a form that SciPy can evaluate numerically, f
    f: sp.Lambda = sp.lambdify((t, symbols), equations)
    # evaluate function between [t0, tn] for numPoints
    timeToEvaluate = np.linspace(0, tn, numPoints)
    # Call SciPy's ODE initial value problem solver solve_ivp
    return sc.integrate.solve_ivp(f,
                                  method = ODEMethod,
                                  t_span = (0, tn),
                                  y0 = initialValues,
                                  first_step = 0.001,
                                  rtol = 0.00000001,    # 1e-8
                                  atol = 0.00000001,    # 1e-8
                                  t_eval=timeToEvaluate)