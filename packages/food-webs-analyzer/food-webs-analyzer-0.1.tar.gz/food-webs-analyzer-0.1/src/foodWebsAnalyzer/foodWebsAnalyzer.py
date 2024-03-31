# import common libraries
import os
import sys

# import libraries
from common.inputParameters import InputParameters
from common.printer import Printer
from ecosystems.ecosystem import Ecosystem
from ecosystems.analysis.generalModel import GeneralModel
from ecosystems.analysis.stability import Stability

# class food webs analyzer
class FoodWebsAnalyzer:

    # Initializing, receive io parameters and symbolic data
    def __init__(self, arguments: str) -> None:
        # first init input parameters
        self.inputParameters = InputParameters(arguments)
        # init self.printer
        self.printer = Printer(self.inputParameters)
        # read food web datas
        self.readFoodWebDatas()
        # generate output ternaries
        self.generateOutputTernaries()        

    # read ecosystem datas from directoryinputParameters
    def readFoodWebDatas(self) -> None:
        # first check if data folder exist
        if os.path.isdir(self.inputParameters.dataFolder):
            # continue depending if we're loading a list of specific foodWebDatas or all self.ecosystems
            if (self.inputParameters.customFiles == ""):
                # print info
                print("Reading all ecosystem data from '" + self.inputParameters.dataFolder + "'")
                # get all food web data from files
                for foodWebFile in os.listdir(self.inputParameters.dataFolder):
                    # filter by extension
                    if ".m" in foodWebFile or ".mat" in foodWebFile:
                        print("Reading file " + foodWebFile + "...")
                        self.ecosystems.append(Ecosystem(self.inputParameters, self.printer, foodWebFile, False))
                        print("Finished.")
            else:
                # print info
                print("Reading single ecosystem data '" + self.inputParameters.customFiles + "' from '" + self.inputParameters.dataFolder + "'")
                # obtain files
                files = self.inputParameters.customFiles.split(',')
                # process every file
                for file in files:
                    self.ecosystems.append(Ecosystem(self.inputParameters, self.printer, file, False))
        else:
            # print info
            print("Folder '" + self.inputParameters.dataFolder + "' doesn't exist")

    # generate output ternaries
    def generateOutputTernaries(self) -> None:
        # first check that we have multiple files and we're checking the local stability
        if ((self.inputParameters.customFiles == "") and 
            self.inputParameters.checkLocalStability and
            (len(self.ecosystems) > 0)):
            # iterate over all processed ecosystem and calculate the average of the stabilityValues
            stabilityValuesAverage = self.ecosystems[0].generalModel.controlSpaceJacobian.stabilityValues
            for i in range (0, len(stabilityValuesAverage)):
                # declare average value
                averageValue: float = 0
                # sum all stability values of ecosystems
                for ecosystem in self.ecosystems:
                    averageValue = averageValue + ecosystem.generalModel.controlSpaceJacobian.stabilityValues[i]
                stabilityValuesAverage[i] = averageValue / float(len(self.ecosystems))
            # print proportion ternary
            self.printer.printProportionTernary("localStability", ".",
                self.ecosystems[0].generalModel.controlSpaceJacobian.sdValues,
                self.ecosystems[0].generalModel.controlSpaceJacobian.srValues,
                self.ecosystems[0].generalModel.controlSpaceJacobian.slValues,
                stabilityValuesAverage)

    # input parameters
    inputParameters: InputParameters

    # printer
    printer: Printer

    # list of food web datas
    ecosystems: list[Ecosystem] = []
   
# main function
if __name__ == '__main__':
    # simply create a instance of foodweb dynamics    
    FoodWebsAnalyzer(sys.argv)