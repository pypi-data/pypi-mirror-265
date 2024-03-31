import sympy as sp
import scipy as sc
import numpy as np
import pylatex as pl
import matplotlib.pyplot as plt

# print the given values in a figure
def PlotInFile(imageName, doc, odeValues):
    # plot lines
    for i in range(0, len(odeValues.y)):
        plt.plot(odeValues.t, odeValues.y[i], label = str(i))
    # put legendlegend
    plt.legend()
    # save as figure
    plt.savefig(imageName + ".png")
    plt.clf()
    # put figure in latex doc
    with doc.create(pl.Figure(position='h!')) as figure:
        figure.add_image(imageName + ".png", width='300px')

# evaluate the given two functions _(t) 10 times and plot image (only for symbolics)
def EvaluateAndPlot(imageName, doc, functionA, functionB, t):
    # evaluate for 10 times
    valuesX = []
    valuesY = []
    # draw 10 times
    for i in range (0, 10):
        # evaluate both functions
        functionAEvaluated = functionA.rhs.subs({t : i})
        functionBEvaluated = functionB.rhs.subs({t : i})
        # evaluate integral
        valuesX.append(functionAEvaluated.doit().evalf(10))
        valuesY.append(functionBEvaluated.doit().evalf(10))
    # print values
    doc.append(pl.NoEscape(sp.latex([sp.Matrix(valuesX), sp.Matrix(valuesY)], mode="equation*")))
    # plot lines
    plt.plot(valuesX, valuesY, label = "X")
    plt.plot(valuesY, valuesX, label = "Y")
    plt.legend()
    # save as figure
    plt.savefig(imageName + ".png")
    plt.clf()
    # put figure in latex doc
    with doc.create(pl.Figure(position='h!')) as figure:
        figure.add_image(imageName + ".png", width='300px')    