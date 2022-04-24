import inspect
import textwrap
import cv2
from pyparsing import str_type
import pytesseract
import re
from tkinter import filedialog 
import string

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Storing image path 
file_path = filedialog.askopenfilename()

# Reading image file using cv2.imread function..............
img = cv2.imread(file_path)



# img = cv2.resize(img, None, fx= 0.5, fy=0.5)

#Converting image to BGR2GRAY color..................
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#Tuning image with some filter for better result............
adaptiv_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 89,28)

#Display the image...................
# cv2.imshow("gray", gray)
# cv2.imshow("image", img)
cv2.imshow(file_path, adaptiv_threshold)

#Converting image to string.....................
text = pytesseract.image_to_string(adaptiv_threshold, lang= 'eng')
ben_text = pytesseract.image_to_string(adaptiv_threshold, lang= 'ben')
fornt_text = text + ben_text
print (fornt_text)

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
name = re.findall(name_condition, fornt_text, re.M)
birthday = re.findall(birthday_condition, fornt_text, re.M)
id_no = re.findall(id_no_condition, fornt_text, re.M)

#Bengali data veriable......................
ben_name = re.findall(bengali_name_condition, fornt_text, re.MULTILINE)
ben_father_name = re.findall(father_name_condition, fornt_text, re.MULTILINE)
ben_mother_name = re.findall(mother_name_condition, fornt_text, re.MULTILINE)

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






# Holding the displayed image visible..................
cv2.waitKey(0)
cv2.destroyAllWindows()
