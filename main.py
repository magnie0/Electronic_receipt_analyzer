import sys
from image_to_text.imageToText import ImagetoText
from auchan.analyseReceiptAuchan import Analyse_Receipt_Auchan
#TODO help if no argument passed
#ex. usage python3 imageToText.py <filename>
filename = sys.argv[1]
#Auchan
str = ImagetoText(filename)
Analyse_Receipt_Auchan(str)
