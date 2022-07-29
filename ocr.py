import cv2
import numpy as np
import pytesseract
import re
import uuid
from tkinter import filedialog 
from datetime import datetime


import shutil
# from fastapi import FastAPI, File, UploadFile
from typing import List

# from requests import Response


# app = FastAPI()

# @app.post("/upload-img")
# async def upload_image(images: List[UploadFile] = File(...)):
#     # destination_file_path = "upload_images/"+files.filename # location to store files
#     images[0].filename = f"{uuid.uuid4()}.jpg"
#     contents = await images[0].read() # <-- Important!
#     # return {"Result": "Success"}
#     return Response(user)


# pytesseract.pytesseract.tesseract_cmd = r"C:\Users\mahad\AppData\Local\Tesseract-OCR\tesseract.exe"
# TESSDATA_PREFIX = r'C:\\Users\\mahad\\AppData\\Local\\Tesseract-OCR\\tessdata'
# Storing image path 
print("please select NID font image")
font_image_path = filedialog.askopenfilename()

print("please select NID back image")
back_image_path = filedialog.askopenfilename()
######..................***Start of font data functions***....................


# Reading image file using cv2.imread function..............
def read_font_image(img_path):
    img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)

#..................*************....................
    copy_img = img.copy()
    lower = np.array([60,60,60])
    higher = np.array([250,250,250])
    mask = cv2.inRange(img, lower,higher)     
    
    cont, _= cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)       # Finding Bounding Box
    # cont_img = cv2.drawContours(img, cont, -1,255,3)

    c = max(cont, key=cv2.contourArea)      # Finding Max Contor.........
    x,y,w,h = cv2.boundingRect(c)
    # cv2.rectangle(img,(x,y), (x+w, y+h), (0,255,0),3)

    cropped_img = copy_img[y:y+h, x:x+w]        # Cropping image..........
    
#..................*************....................

    cropped_img = cv2.resize(cropped_img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    # cropped_img = cv2.resize(cropped_img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)


#..................*************....................

    gray_image = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)     #Converting image to BGR2GRAY color..................

#..................*************....................

    adaptiv_threshold = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 109,26)       #Appling Adapting Threshold for better result............
    return adaptiv_threshold

#..................*************....................







# Reading image file using cv2.imread function..............
def read_font_image_ns(img_path):
    img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)

#..................*************....................
    copy_img = img.copy()
    lower = np.array([60,60,60])
    higher = np.array([250,250,250])
    mask = cv2.inRange(img, lower,higher)     
    
    cont, _= cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)       # Finding Bounding Box
    # cont_img = cv2.drawContours(img, cont, -1,255,3)

    c = max(cont, key=cv2.contourArea)      # Finding Max Contor.........
    x,y,w,h = cv2.boundingRect(c)
    # cv2.rectangle(img,(x,y), (x+w, y+h), (0,255,0),3)

    cropped_img = copy_img[y:y+h, x:x+w]        # Cropping image..........
    
#..................*************....................

    # cropped_img = cv2.resize(cropped_img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    cropped_img = cv2.resize(cropped_img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)


#..................*************....................

    gray_image = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)     #Converting image to BGR2GRAY color..................

#..................*************....................

    adaptiv_threshold = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 89,15)       #Appling Adapting Threshold for better result............
    return adaptiv_threshold

#..................*************....................

def thin_font(image):
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2), np.uint8)
    image = cv2.erode(image, kernel, iterations= 1)
    image = cv2.bitwise_not(image)
    return (image)


#..................*************....................



# Converting image to string.....................


def image_to_text(threshold_image):
    result = pytesseract.image_to_string(threshold_image, lang = "eng")
    return result

#Display the image...................
def display(title, image):
    return cv2.imshow(title, image)


#..................*************....................


def name_extraction(text):
    name_condition = r"\bName.*"
    capital_name_condition = r"\b[A-Z][A-Z].*[A-Z][A-Z][A-Z]\b"
    name = re.findall(name_condition, text, re.M)
    capital_name = re.findall(capital_name_condition, text, re.M) 
    # print("Name 0:::"+name[0])
    # print(len(capital_name))
    # print(capital_name)
    if len(name) >0:
        if len(name[0])>6:
            name = str(name[0]).replace(',','.')
            # name = re.split(':', name)[1]
            name = name[6:]               
        elif len(capital_name)>0:
            for n in capital_name:
                if len(n)>6:
                    # print(n)
                    name = n  
                         
    elif len(capital_name)>0:
        for n in capital_name:
            if len(n)>3 & len(n)<20:
                if "." in n:
                    # print("line124",n)
                    name = n
                    break
                else:
                    name = n

    else:
        name = 'None'
    return name


#..................*************....................




def dob_extraction(text):
    dob_condition = r"[0-3][0-9] [A-Z][a-z]{2} [1-3][0-9]{3}"
    dob = re.findall(dob_condition, text, re.M)
    if dob:
        sdob = str(dob[0])
        dob = datetime.strptime(sdob, "%d %b %Y").strftime('%d %m %Y')
        # print(dob)

    return dob

#..................*************....................


def nid_extraction(text):
    # id_no_condition = r"\d{17}|\d{13}|\d{10}|\d{3}\s\d{3}\s\d{4}"
    id_no_condition = r"[0-9]{17}|[0-9]{13}|[0-9]{10}|[0-9]{3}\s[0-9]{3}\s[0-9]{4}|[0-9]{6}\s[0-9]{4}"
    id_no = re.findall(id_no_condition, text, re.M) 
    
    if id_no:
        if len(id_no[0])==17:
            id_no = str(id_no[0])
            id_no = id_no.replace(" ", "")
        elif len(id_no[0])==13:
            id_no = str(id_no[0])
            id_no = id_no.replace(" ", "")
        elif len(id_no[0])==10:
            id_no = str(id_no[0])
            id_no = id_no.replace(" ", "")
        elif len(id_no[0])==11:
            id_no = str(id_no[0])
            id_no = id_no.replace(" ", "")
        elif len(id_no[0]) ==12:
            id_no = str(id_no[0])
            id_no = id_no.replace(" ", "")   
    else:
        id_no ="None"    
    return id_no



# def fontData(img)
img = read_font_image(font_image_path)
img = thin_font(img)
# cv2.imshow("fornt1", img) 
text = image_to_text(img)
# print (text)

#Removing All single charecter from text...............
text = re.sub(r'\b[a-zA-Z]\b','', text)
print (text)


# Removing All the special carecters from the text...................

# text = text.translate(str.maketrans('','', string.punctuation))
# print (ben_text)


    

######..................***End of font data functions***....................




######..................***Start of back data functions***....................


input_image = cv2.resize(cv2.imread(back_image_path), None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
# input_image = cv2.resize(cv2.imread(image_path), None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)


def match_and_alignImage(imgPath , img):
    per = 30
    imgQuery = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
    
    h,w = imgQuery.shape
    orb = cv2.ORB_create(1000)
    kp1 , des1 = orb.detectAndCompute(imgQuery, None)
    kp2, des2 = orb.detectAndCompute(img, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING2, True)
    matches = bf.match(des2, des1)
    matches = sorted(matches, key=lambda x:x.distance)
    good = matches[:int(len(matches)*(per/100))]

    srcPoints = np.float32([kp2[m.queryIdx].pt for m in good]).reshape(-1,1,2)
    dstPoints = np.float32([kp1[m.trainIdx].pt for m in good]).reshape(-1,1,2)

    M, _ = cv2.findHomography(srcPoints, dstPoints, cv2.RANSAC, 5.0)
    imgScan = cv2.warpPerspective(img, M, (w,h))
    
    imgScan = cv2.cvtColor(imgScan, cv2.COLOR_BGR2GRAY)
    imgScan = cv2.adaptiveThreshold(imgScan, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 111,29)
    
    
    return imgScan



def get_data(alignImage, roi):

    for x,r in enumerate(roi):

        imgCrop = alignImage[r[0][1]:r[1][1], r[0][0]:r[1][0]]
        # cv2.imshow(str(x), imgCrop)  

    imgCrop = cv2.resize(imgCrop, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    imgCrop = thin_font(imgCrop)
    # cv2.imshow("output2",imgCrop)
    output = pytesseract.image_to_string(imgCrop, lang="ben",config="--psm 6")

    return output


def get_address():
    roi_smart_back = [[(38, 350), (1294, 642), 'bText', 'Address']]
    # roi_normal_back = [[(4, 128), (1196, 302), 'btext', 'AddNS']]
    roi_normal_back = [[(0, 252), (2042, 540), 'bText', 'AddNS']]

    path_normal_back_img = 'query_img\\nsBack.jpg'
    path_smart_back_img = 'query_img\\hback.png'
    align_image = match_and_alignImage(path_normal_back_img, input_image)
    add = get_data(align_image, roi_normal_back)
    print(len(add))
    if len(add) < 10:
        align_image = match_and_alignImage(path_smart_back_img, input_image)
        add = get_data(align_image, roi_smart_back)
        # print(add)
        return add
    else:
        # print(add)
        return add
######..................***End of back data functions***......................




#..................*************....................

#Creating a User dictionary to hold all the data in once......................

user = {
    "Name" : None,
    "Date of Birth" : None,
    "NID No" : None,
    "Address" : None,
}

name = name_extraction(text)
dob = dob_extraction(text)
nid = nid_extraction(text)
add = get_address()


if len(name) ==0 or len(dob) == 0 or len(nid)==0:
    #call non smart thereshold
    
    # def fontData(img)
    img = read_font_image_ns(font_image_path)
    img = thin_font(img)
    cv2.imshow("fornt2", img) 
    text = image_to_text(img)
    print ("last------------------------\n"+text)

    #Removing All single charecter from text...............
    text = re.sub(r'\b[a-zA-Z]\b','', text)

    name = name_extraction(text)
    dob = dob_extraction(text)
    nid = nid_extraction(text)

    if name:
        user["Name"] = name

    if dob:
        user["Date of Birth"] = dob   

    if nid:
        user["NID No"] = nid
    
else:
    if name:
        user["Name"] = name

    if dob:
        user["Date of Birth"] = dob   

    if nid:
        user["NID No"] = nid
    # user["Name"] = name
    # user["Date of Birth"] = dob
    # user["NID No"] = nid




    # if name:
    #     user["Name"] = name

    # if dob:
    #     user["Date of Birth"] = dob   

    # if nid:
    #     user["NID No"] = nid
    if add:
        add = str(add).replace('\n','')
        user["Address"] = add



# Printing Output................

print(user)

#..................*************....................


# display(image_path, img)

# Holding the displayed image visible..................
cv2.waitKey(0)
cv2.destroyAllWindows()
