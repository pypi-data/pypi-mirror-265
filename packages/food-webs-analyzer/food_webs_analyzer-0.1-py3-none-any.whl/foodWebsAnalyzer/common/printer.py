# import common libraries
import os
import shutil
import sympy as sp
import numpy as np
import mpltern as mtn
import matplotlib.pyplot as plt
from matplotlib.patches import ArrowStyle
from matplotlib.patches import FancyArrowPatch
import pylatex as pl # type: ignore
import scipy as sc # type: ignore


# import libraries
from common.inputParameters import InputParameters
import utils.transform as tr


# class printer (used for print outputs in console and files)
class Printer:

    # Initializing
    def __init__(self, inputParameters: InputParameters):
        # save reference to input parameters
        self.inputParameters = inputParameters
        # init image counter
        self.imageCounter = 0
    
    # init latex document
    def initFolderAndLatexDocument(self, foodWebFilename: str) -> None:
        # remove extensions
        foodWebFolder = foodWebFilename.replace(".m", "")
        # clear and init directory
        if os.path.isdir(self.inputParameters.outputFolder + "/" + foodWebFolder):
            shutil.rmtree(self.inputParameters.outputFolder + "/" + foodWebFolder)
        os.mkdir(self.inputParameters.outputFolder + "/" + foodWebFolder)
        # check if we defined a latex file
        if (len(self.inputParameters.outputLatexFile) > 0):
            # create basic document
            self.latexDoc = pl.Document(self.inputParameters.outputFolder + "/" + foodWebFolder + "/" + self.inputParameters.outputLatexFile)
            # add math package
            self.latexDoc.packages.append(pl.Package('amsmath'))

    # Print files
    def writeOutputFiles(self, foodWebFolder: str) -> None:
        # check if we have to write a output file
        if (len(self.inputParameters.outputPlainFile) > 0):
            # print info
            self.printInfo("Writting output file '" + self.inputParameters.outputPlainFile + "'")
            # open file and write output
            with open(self.inputParameters.outputFolder + "/" + foodWebFolder + "/" + self.inputParameters.outputPlainFile, mode='w', encoding="utf-8") as f:
                f.write(self.outputPlainBuffer)
        # check if generate Latex files
        if (len(self.inputParameters.outputLatexFile) > 0):
            # generate text file
            self.latexDoc.generate_tex()
            # generate pdf file
            self.latexDoc.generate_pdf(clean_tex=False)

    # write matrix in file usingMatLab format
    def writeMatrixColumnMatLab(self, foodWebFolder: str, file: str, valueName: str, matrix: sp.Matrix) -> None:
        # convert matrix in list of strings separated by commas
        valuesList: str = ", ".join(tr.matrixFloatToListStr(matrix))
        # print info
        self.printInfo("Writting file '" + file + "'")
        # open file and write output
        with open(self.inputParameters.outputFolder + "/" + foodWebFolder + "/" + file, mode='w', encoding="utf-8") as f:
            f.write(valueName + " = [" + valuesList + "].';")

    # print string info
    def printInfo(self, value: str | sp.Matrix | sp.MatrixSymbol) -> None:
        # get pretty format
        output = sp.pretty(value, wrap_line = self.inputParameters.wrapLine)
        # print in console
        print(output)
        # check if add to buffer
        if (len(self.inputParameters.outputPlainFile) > 0):
            self.outputPlainBuffer += output + "\n"
        # continue depending if we're going to writting in latex
        if (len(self.inputParameters.outputLatexFile) > 0):
            # get latex format code and append to latex buffer
            self.latexDoc.append(pl.NoEscape(sp.latex(value, mode = self.inputParameters.latexMode, order = self.inputParameters.latexOrder)))

    # print the given matrix, and optionally their evaluated matrix
    def printMatrix(self, info:str, matrix: sp.Matrix | sp.MatrixSymbol) -> None:
        # print info
        self.printInfo(info)
        # print matrix
        self.printInfo(matrix)

    # print the given matrix, and their evaluated matrix if we're not in numerical mode)
    def printMatrixEvaluated(self, info:str, matrix: sp.Matrix | sp.MatrixSymbol, dic: dict) -> None:
        # print matrix
        self.printMatrix(info, matrix)
        # print evaluated matrix (only if numerical option isn't enabled
        if (not self.inputParameters.numerical):
            self.printMatrix("Evaluated", matrix.subs(dic))

    # print the given ode graph
    def printODEGraph(self, foodWebFolder: str, odeValues: sc.integrate._ivp.ivp.OdeResult) -> None:
        # create figure
        plt.figure()
        # plot lines
        for i in range(0, len(odeValues.y)):
            plt.plot(odeValues.t, odeValues.y[i], label = str(i))
        # put legendlegend
        plt.legend()
        # save image
        imageName = self.savePlotInFile(foodWebFolder, plt)
        # clear figure
        plt.clf()
        # continue depending if we're going to writting in latex
        if (len(self.inputParameters.outputLatexFile) > 0):
            # put figure in latex doc
            with self.latexDoc.create(pl.Figure(position='h!')) as figure:
                figure.add_image(imageName, width='300px')

    # print the given graph
    def printGraphMatrix(self, foodWebFolder: str, matrix: sp.Matrix) -> None:
        # create figure
        plt.figure()
        # plot lines
        plt.plot(tr.matrixFloatToList(matrix))
        # save image
        imageName = self.savePlotInFile(foodWebFolder, plt)
        # clear figure
        plt.clf()
        # continue depending if we're going to writting in latex
        if (len(self.inputParameters.outputLatexFile) > 0):
            # put figure in latex doc
            with self.latexDoc.create(pl.Figure(position='h!')) as figure:
                figure.add_image(imageName, width='300px')

    # print a proportion ternary using the given data
    def printProportionTernary(self, filename: str, foodWebFolder: str, sdValues: list[float], srValues: list[float], slValues: list[float], stabilityValues: list[float]) -> None:
        # create figure
        fig = plt.figure(figsize=(10, 7.5))
        ax = fig.add_subplot(111, projection='ternary')
        # create as tripcolor
        # rasterized=True
        cs = ax.tricontourf(sdValues, slValues, srValues, stabilityValues, vmin=0.0, vmax=1.0)
        ax.set_title("Proportion values Heatmap")
        # configure colorbar
        cax = ax.inset_axes([1.05, 0.1, 0.05, 0.9], transform=ax.transAxes)
        colorbar = fig.colorbar(cs, cax=cax)
        colorbar.set_label('Stability', rotation=270, va='baseline')
        # enable grid
        ax.grid(linewidth=0.5)        
        # set ticks
        ticks = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        ax.taxis.set_ticks(ticks)
        ax.laxis.set_ticks(ticks)
        ax.raxis.set_ticks(ticks)
        # set labels
        ax.set_tlabel("Pure Donor Control")
        ax.set_llabel("Pure Lotka Volterra")
        ax.set_rlabel("Pure Recipient")
        # create arrow
        arrowstyle = ArrowStyle('simple', head_length=10, head_width=5)
        kwargs_arrow = {
            'transform': ax.transAxes,  # Used with ``ax.transAxesProjection``
            'arrowstyle': arrowstyle,
            'linewidth': 1,
            'clip_on': False,  # To plot arrows outside triangle
            'zorder': -10,  # Very low value not to hide e.g. tick labels.
        }
        # Start of arrows in barycentric coordinates.
        ta = np.array([ 0.1, -0.1,  1.1])
        la = np.array([ 1.1,  0.1, -0.1])
        ra = np.array([-0.1,  1.1,  0.1])
        # End of arrows in barycentric coordinates.
        tb = np.array([ 1.0, -0.1,  0.1])
        lb = np.array([ 0.1,  1.0, -0.1])
        rb = np.array([-0.1,  0.1,  1.0])
        # This transforms the above barycentric coordinates to the original Axes
        # coordinates. In combination with ``ax.transAxes``, we can plot arrows fixed
        # to the Axes coordinates.
        f = ax.transAxesProjection.transform
        # create arrows
        ax.add_patch(FancyArrowPatch(f(ta), f(tb), ec='C0', fc='C0', **kwargs_arrow))
        ax.add_patch(FancyArrowPatch(f(la), f(lb), ec='C1', fc='C1', **kwargs_arrow))
        ax.add_patch(FancyArrowPatch(f(ra), f(rb), ec='C2', fc='C2', **kwargs_arrow))
        # To put the axis-labels at the positions consistent with the arrows above, it
        # may be better to put the axis-label-text directly as follows rather than
        # using e.g.  ax.set_tlabel.
        kwargs_label = {
            'transform': ax.transTernaryAxes,
            'backgroundcolor': 'w',
            'ha': 'center',
            'va': 'center',
            'rotation_mode': 'anchor',
            'zorder': -9,  # A bit higher on arrows, but still lower than others.
        }
        # Put axis-labels on the midpoints of arrows.
        tpos = (ta + tb) * 0.5
        lpos = (la + lb) * 0.5
        rpos = (ra + rb) * 0.5
        # set texts
        ax.text(*tpos, 'sd fraction', color='C0', rotation=-60, **kwargs_label)
        ax.text(*lpos, 'sl fraction', color='C1', rotation= 60, **kwargs_label)
        ax.text(*rpos, 'sr fraction', color='C2', rotation=  0, **kwargs_label)
        # save image
        imageName = ""
        # check saving format
        if(self.inputParameters.saveSVG):
            imageName = self.inputParameters.outputFolder + "/" + foodWebFolder + "/" + filename + ".svg"
            plt.savefig(self.inputParameters.outputFolder + "/" + foodWebFolder + "/" + filename + ".svg", format="svg", dpi = self.inputParameters.dpi)
        else:
            imageName = self.inputParameters.outputFolder + "/" + foodWebFolder + "/" +  filename + ".png"
            plt.savefig(self.inputParameters.outputFolder + "/" + foodWebFolder + "/" +  filename + ".png", format="png", dpi = self.inputParameters.dpi)
        # clear figure
        fig.clf()
        # continue depending if we're going to writting in latex
        if (len(self.inputParameters.outputLatexFile) > 0):
            # put figure in latex doc
            with self.latexDoc.create(pl.Figure(position='h!')) as figure:
                figure.add_image(imageName, width='300px')

    # print ode result in a table
    def printODETable(self, odeResult: sc.integrate._ivp.ivp.OdeResult) -> None:
        # print info
        self.printInfo("printing ODE result")
        # get number of variables
        numVar = len(odeResult.y)
        numRows = len(odeResult.t)
        # open file and write output
        with open("solverResult.txt", mode='w', encoding="utf-8") as f:
            # write header
            f.write("time,")
            for i in range(0, numVar):
                if (i == (numVar - 1)):
                    f.write("biomass_" + str(i + 1) + "\n")
                else:
                    f.write("biomass_" + str(i + 1) + ",")
            # write data
            for row in range(0, numRows):
                f.write(str(odeResult.t[row]) + ",")
                for i in range(0, numVar):
                    if (i == (numVar - 1)):
                        f.write(str(odeResult.y[i][row]) + "\n")
                    else:
                        f.write(str(odeResult.y[i][row]) + ",")

    # save given plot in file
    def savePlotInFile(self, foodWebFolder: str, plot) -> str:
        # create image name
        imageName = "image" + str(self.imageCounter)
        # update counter
        self.imageCounter += 1
        # check saving format
        if(self.inputParameters.saveSVG):
            plot.savefig(self.inputParameters.outputFolder + "/" + foodWebFolder + "/" + imageName + ".svg", format="svg", dpi = self.inputParameters.dpi)
            return imageName + ".svg"
        else:
            plot.savefig(self.inputParameters.outputFolder + "/" + foodWebFolder + "/" +  imageName + ".png", format="png", dpi = self.inputParameters.dpi)
            return imageName + ".png"

    # reference to input parameters
    inputParameters: InputParameters

    # output buffer for plain format
    outputPlainBuffer: str = ""

    # latex document
    latexDoc: pl.Document

    # image counter
    imageCounter: int

