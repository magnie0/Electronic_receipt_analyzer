import sys
from utils.imageToText import ImagetoText
from auchan.analyseReceipt import Analyse_Receipt_Auchan
#TODO help if no argument passed
#ex. usage python3 imageToText.py <filename>
filename = sys.argv[1]
#Auchan
str = ImagetoText(filename)
Analyse_Receipt_Auchan(str,'2024-09-13')