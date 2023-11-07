
# Basic libraries to import for completing the whole work.
import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import csv
import pandas as pd

from selenium import webdriver 
from selenium.webdriver.chrome.service import Service 
from bs4 import BeautifulSoup
import pandas as pd
import threading

# import allAlgorithms 
import time





class Mainwindow(QMainWindow):
    def __init__(self):
        super(Mainwindow,self).__init__()
        self.printData = []
        self.isStop = False
        self.isPause = False
        loadUi("Scrap.ui",self) # Here we imported the QT Designer file which we made as Python GUI FIle.
        self.ProgressBar.setValue(0)
        self.BackButton.clicked.connect(lambda: self.close())

        # Command to remove the default Windows Frame Design.
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        # Command to make the backgroud of Window transparent.
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        #These 2 lines are used to put funnctions on close and minimize buttons.
        # self.BackButton.clicked.connect(lambda: self.close())
        
        
        #Button Functions
        # self.SortButton.clicked.connect(self.SortTable)
        self.StartButton.clicked.connect(self.startScrapping)
        self.PauseButton.clicked.connect(self.PauseFun)
        self.StopButton.clicked.connect(self.StopFun)


    def PauseFun(self):
        if not self.isPause:
            self.isPause = True
        else:
            self.isPause = False
            self.PauseButton.setText("PAUSE")

    def StopFun(self):
        if not self.isStop:
            self.isStop = True
        else:
            self.isStop = False


    def fillData(self):
            data = self.printData
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
            data = None


    def startScrapping(self):
        service = Service(executable_path = r'D:\chromedriver-win64\chromedriver.exe')
        options  = webdriver.ChromeOptions()
        options.add_argument('--blink-settings=imagesEnabled=false')
        driver = webdriver.Chrome(service = service, options = options)

        endPoint = int(self.RangeBox.text())
        th1 = threading.Thread(target= self.ScrapData, args = (1, endPoint, driver))
        self.ProgressBar.setValue(0)
        self.isStop = False
        self.isPause = False
        th1.start()

        # data = self.ScrapData(1, endPoint, driver)
        # data = data.values
        # print(data)
        # self.fillData(data)


    def ScrapData(self, start, end, driver):
        
        Title = []
        Author = []
        Publisher = []
        Year = []
        Language = []
        ISBN = []
        Page = []
        Series = []
        ID = []
        Size = []
        Format = []

        
        for pgNr in range(start,end + 1):
            isStopped = False
            while True:
                try:
                    while (self.isPause):
                        if self.isStop:
                            isStopped = True
                            break
                        self.PauseButton.setText("CONTINUE")
                        time.sleep(1)
                    self.PauseButton.setText("PAUSE")
                except:
                    pass
                else:
                    break

            while True:
                try:
                    if self.isStop:
                        isStopped = True
                except:
                    pass
                else:
                    break
            if isStopped:
                break


            driver.get("https://libgen.is/search.php?mode=last&view=detailed&phrase=1&res=100&timefirst=&timelast=&sort=def&sortmode=ASC&page=" + str(pgNr)) 

            content = driver.page_source 
            soup = BeautifulSoup(content)


            for a in soup.findAll('table',attrs={'border':"0", 'rules':"cols", 'width':"100%"}):
                rows = a.findAll('tr',attrs={'valign':"top"})
                if len(rows) > 10:
                    Title.append(giveText(rows, 1, 2))
                    Author.append(giveText(rows, 2, 1))

                    Series.append(modifySeries(giveText(rows, 3, 1)))

                    Publisher.append(giveText(rows, 4, 1))
                    Year.append(giveText(rows, 5, 1))
                    Language.append(giveText(rows, 6, 1))

                    page = giveText(rows, 6, 3)
                    Page.append(modifyPage(page))

                    ISBN.append(giveText(rows, 7, 1))
                    ID.append(giveText(rows, 7, 3))

                    size = giveText(rows, 9, 1)
                    Size.append(modifySize(size))

                    Format.append(giveText(rows, 9, 3))
            self.ProgressBar.setValue((pgNr * 100) // end )

        self.PauseButton.setText("PAUSE")
        df = pd.DataFrame({'Title':Title,'Author':Author,'Publisher':Publisher, 'Year':Year, 'Language':Language, 
                        'ISBN':ISBN, 'Page':Page,'Series':Series,'ID':ID,  'Size':Size, "Format":Format  }) 
        # df.to_csv(rf'D:\book{end}.csv', index=False, encoding='utf_8_sig')
        self.printData = df.values
        self.fillData()
        # return df

   
def giveText(rowDF, row, col):
    cols = rowDF[row].findAll('td',attrs={})
    res = cols[col].text
    
    if not res or res == "":
        return "NA"
    return res

def modifyPage(page):
    if "[" in page:
        return page[page.index('[') + 1: page.index(']')]
        
    return page

def modifySize(size):
    if size == "NA":
        return size
    size = size.split('(')[0].split(" ")
    if size[1] == "Kb":
        size[0] = round(float(size[0]) / 1024, 2)
        
    return size[0]

def modifySeries(series):
    if series == "NA":
        series = "StandAlone"
    return series
        
  
   


    
    # def SortTable(self):
    #     algoName, attributeName, startPoint, endPoint = self.getDataFromBox()
    #     attributeIdx = self.getAttributeIndex(attributeName)

    #     if algoName.lower() in ["pigeonhole sort", "radix sort", "count sort"] and attributeIdx != 6:
    #         self.TimeBox.setText(f"{algoName} only works on integers, Try Pages Column")
    #         return
        
    #     data = self.getDataFromCsv(startPoint=startPoint, endPoint=endPoint)
    #     if data == None:
    #         print("not available")
    #         return
    #     # print(len(data))

    #     sTime = time.time()

    #     try:
    #         if algoName.lower() == "merge sort":
    #             allAlgorithms.merge_sort(data, attributeIdx)
    #         elif algoName.lower() == "bubble sort":
    #             allAlgorithms.bubble_sort(data, attributeIdx)
    #         elif algoName.lower() == "selection sort":
    #             allAlgorithms.selection_sort(data, attributeIdx)
    #         elif algoName.lower() == "insertion sort":
    #             allAlgorithms.insertion_sort(data, attributeIdx)
    #         elif algoName.lower() == "quick sort":
    #             allAlgorithms.quick_sort(data, 0, len(data)-1, attributeIdx)
    #         elif algoName.lower() == "bucket sort":
    #             data = allAlgorithms.bucket_sort(data, attributeIdx)
    #         elif algoName.lower() == "count sort" and attributeIdx == 6:  # works only on pages
    #             data = allAlgorithms.count_sort(data, attributeIdx)
    #         elif algoName.lower() == "radix sort" and attributeIdx == 6:  # works only on pages
    #             data = allAlgorithms.radix_sort(data, attributeIdx)
    #         elif algoName.lower() == "pigeonhole sort" and attributeIdx == 6:  # works only on pages
    #             data = allAlgorithms.pigeonhole_sort(data, attributeIdx)
    #         elif algoName.lower() == "heap sort" : 
    #             data = allAlgorithms.heap_sort(data, attributeIdx)
    #         elif algoName.lower() == "oddeven sort" : 
    #             data = allAlgorithms.oddEven_sort(data, attributeIdx)
    #         eTime = time.time()
    #         # str(eTime - sTime)
    #         self.TimeBox.setText(f"It took {eTime - sTime} seconds to sort {endPoint-startPoint+1} data using {algoName} sort")
    #         self.fillData(data=data)
    #     except:
    #         eTime = time.time()
    #         self.TimeBox.setText(f"Error; time took is {eTime - sTime}")



# main

# app = QApplication(sys.argv)
# window = Mainwindow()
# window.show()
# sys.exit(app.exec_())






