import inspect
import textwrap
from unittest import result
import cv2
from pyparsing import str_type
import pytesseract
import re
from tkinter import filedialog 
import string

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TESSDATA_PREFIX = 'C:/Program Files/Tesseract-OCR'
# Storing image path 
image_path = filedialog.askopenfilename()

# Reading image file using cv2.imread function..............
def read_image(img_path):
    return cv2.imread(img_path)


# img = cv2.resize(img, None, fx= 0.5, fy=0.5)

#Converting image to BGR2GRAY color..................
def gray_image(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#Tuning image with some filter for better result............
def threshold(gray_image):
    adaptiv_threshold = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 89,28)
    return adaptiv_threshold

#Display the image...................
def display(title, image):
    return cv2.imshow(title, image)

#Converting image to string.....................
lang = "eng+ben"
def image_to_text(threshold_image):
    result = pytesseract.image_to_string(threshold_image, lang= lang)
    return result

img = read_image(image_path)
img = gray_image(img)
img = threshold(img)
text = image_to_text(img)
print (text)

#Removing All single charecter from text...............
text = re.sub(r'\b[a-zA-Z]\b','', text)
# print (text)


# Removing All the special carecters from the text...................

# text = text.translate(str.maketrans('','', string.punctuation))
# print (ben_text)





 #English text Conditions ...................  
name_condition = r"\bName.*"
birthday_condition = r"\bDate.*"
id_no_condition = r"\bID NO.*"

# Bengali Text Conditions....................
bengali_name_condition = r"\bনাম.*"
father_name_condition = r"\bপিতা:.*"
mother_name_condition = r"\bমাতা:.*"

#English data veriable...................
name = re.findall(name_condition, text, re.M)
birthday = re.findall(birthday_condition, text, re.M)
id_no = re.findall(id_no_condition, text, re.M)

#Bengali data veriable......................
ben_name = re.findall(bengali_name_condition, text, re.MULTILINE)
ben_father_name = re.findall(father_name_condition, text, re.MULTILINE)
ben_mother_name = re.findall(mother_name_condition, text, re.MULTILINE)

# Creating a list to holds all the data in once......................

if name:
    text_list = name

if birthday:
    text_list= text_list + birthday   

if id_no:
    text_list= text_list + id_no

if ben_name:
    text_list= text_list + ben_name    

if ben_father_name:
    text_list= text_list + ben_father_name    

if ben_mother_name:
    text_list= text_list + ben_mother_name    


print (text_list)



# Converting text_list values to text_dict...................
text_dict = {}
for t in text_list:
    d = dict(x.split(":") for x in t.split("\\n"))
    for k, v in d.items():
       text_dict[k] = v


# Printing Output................


print (text_dict)




display(image_path, img)

# Holding the displayed image visible..................
cv2.waitKey(0)
cv2.destroyAllWindows()
