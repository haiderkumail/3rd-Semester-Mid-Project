
# Basic libraries to import for completing the whole work.
import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import csv
import pandas as pd

import allAlgorithms 
import time

class Sort_Mainwindow(QMainWindow):
    def __init__(self):
        super(Sort_Mainwindow,self).__init__()
        loadUi("SortMenu.ui",self) # Here we imported the QT Designer file which we made as Python GUI FIle.
        
        # Command to remove the default Windows Frame Design.
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        # Command to make the backgroud of Window transparent.
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        #These 2 lines are used to put funnctions on close and minimize buttons.
        self.BackButton.clicked.connect(lambda: self.close())
        
        # Function to load the previous data of student at the start of program.
        self.load_table()
        
        #Button Functions
        self.SortButton.clicked.connect(self.SortTable)
        
    def getDataFromBox(self):
        algoName = self.SortCB.currentText()
        attributeName = self.AttributeBox.currentText()
        startPoint = self.StartPoint.text()
        endPoint = self.EndPoint.text()

        return algoName, attributeName, int(startPoint), int(endPoint)

    def getDataFromCsv(self, startPoint, endPoint):
        with open('combined_file.csv', "r",encoding="utf_8_sig") as fileInput:
            data = list(csv.reader(fileInput))
            if endPoint >= len(data):
                return
            if startPoint == 0:
                startPoint += 1
                endPoint += 1
            data = data[startPoint:endPoint+1]
            
            temp = [6,8,9]
            for i in data:
                if i[6]:
                    try:
                        i[6] = int(i[6])
                    except:
                        i[6] = 0
                else:
                    i[6] = 0

                if i[8]:
                    try:
                        i[8] = int(i[8])
                    except:
                        i[8] = 0
                else:
                    i[8] = 0

                if i[9]:
                    try:
                        i[9] = float(i[9])
                    except:
                        i[9] = 0
                else:
                    i[9] = 0
                
            return data
        
    def getAttributeIndex(self, attribute):
        dict1 = {"TITLE":0, "AUTHOR":1, "PUBLISHER":2, "YEAR":3, "ISBN":5, "PAGE":6, "SERIES":7, "ID":8, "SIZE":9, "FORMAT":10}
        return dict1[attribute.upper()]



    
    def SortTable(self):
        algoName, attributeName, startPoint, endPoint = self.getDataFromBox()
        attributeIdx = self.getAttributeIndex(attributeName)

        if algoName.lower() in ["pigeonhole sort", "radix sort", "count sort"] and attributeIdx != 6:
            self.TimeBox.setText(f"{algoName} only works on integers, Try Pages Column")
            return
        
        data = self.getDataFromCsv(startPoint=startPoint, endPoint=endPoint)
        if data == None:
            print("not available")
            return
        # print(len(data))

        sTime = time.time()

        try:
            if algoName.lower() == "merge sort":
                allAlgorithms.merge_sort(data, attributeIdx)
            elif algoName.lower() == "bubble sort":
                allAlgorithms.bubble_sort(data, attributeIdx)
            elif algoName.lower() == "selection sort":
                allAlgorithms.selection_sort(data, attributeIdx)
            elif algoName.lower() == "insertion sort":
                allAlgorithms.insertion_sort(data, attributeIdx)
            elif algoName.lower() == "quick sort":
                allAlgorithms.quick_sort(data, 0, len(data)-1, attributeIdx)
            elif algoName.lower() == "bucket sort":
                data = allAlgorithms.bucket_sort(data, attributeIdx)
            elif algoName.lower() == "count sort" and attributeIdx == 6:  # works only on pages
                data = allAlgorithms.count_sort(data, attributeIdx)
            elif algoName.lower() == "radix sort" and attributeIdx == 6:  # works only on pages
                data = allAlgorithms.radix_sort(data, attributeIdx)
            elif algoName.lower() == "pigeonhole sort" and attributeIdx == 6:  # works only on pages
                data = allAlgorithms.pigeonhole_sort(data, attributeIdx)
            elif algoName.lower() == "heap sort" : 
                data = allAlgorithms.heap_sort(data, attributeIdx)
            elif algoName.lower() == "oddeven sort" : 
                data = allAlgorithms.oddEven_sort(data, attributeIdx)
            eTime = time.time()
            # str(eTime - sTime)
            self.TimeBox.setText(f"It took {eTime - sTime} seconds to sort {endPoint-startPoint+1} data using {algoName} sort")
            self.fillData(data=data)
        except:
            eTime = time.time()
            self.TimeBox.setText(f"Error; time took is {eTime - sTime}")

        
        
    # This is a helping Function to load the content of the table after every event.
    def load_table(self, startPoint = 1, endPoint = 100):
        data = self.getDataFromCsv(startPoint, endPoint)
        self.fillData(data=data)
            
    def fillData(self, data):
            self.DataTable.clear()

            self.DataTable.setHorizontalHeaderLabels(("TITLE","AUTHOR","PUBLISHER","YEAR","ISBN","PAGE","SERIES","ID","Size","Format"))
            roww = 0
            self.DataTable.setRowCount(len(data))
            for row in data:
                self.DataTable.setItem(roww, 0 , QtWidgets.QTableWidgetItem((row[0])))
                self.DataTable.setItem(roww, 1 , QtWidgets.QTableWidgetItem((row[1])))
                self.DataTable.setItem(roww, 2 , QtWidgets.QTableWidgetItem((row[2])))
                self.DataTable.setItem(roww, 3 , QtWidgets.QTableWidgetItem((row[3])))
                self.DataTable.setItem(roww, 4 , QtWidgets.QTableWidgetItem((row[5])))
                self.DataTable.setItem(roww, 5 , QtWidgets.QTableWidgetItem((str(row[6]))))
                self.DataTable.setItem(roww, 6 , QtWidgets.QTableWidgetItem((row[7])))
                self.DataTable.setItem(roww, 7 , QtWidgets.QTableWidgetItem((str(row[8]))))
                self.DataTable.setItem(roww, 8 , QtWidgets.QTableWidgetItem((str(row[9]))))
                self.DataTable.setItem(roww, 9 , QtWidgets.QTableWidgetItem((row[10])))
                roww += 1

# main

# app = QApplication(sys.argv)
# window = Mainwindow()
# window.show()
# sys.exit(app.exec_())



