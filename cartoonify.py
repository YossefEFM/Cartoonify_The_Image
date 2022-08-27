# importing libraries
import tkinter
from tkinter import Button

import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
import easygui
import os


# Upload Function
def upload():
    Path=easygui.fileopenbox()
    car(Path)

# Save function
def save(cartoon, ImagePath):
    #saving an image using imwrite()
    newName="cartoonified_Image"
    path1 = os.path.dirname(ImagePath)
    extension=os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(cartoon, cv2.COLOR_RGB2BGR))
    I = "Image saved by name (( " + newName +" )) at  (( "+ path +" ))"
    tkinter.messagebox.showinfo(title=None, message="SAVED \n"+I)

# Figures titles
Name= ["Natural image", "Gray image","SmoothGray image","Edges","Colored image", "Cartoon image"]

top=Tk()
top.geometry('500x500')
top.title(' !! Cartoonify Your Image !!')

Icon = PhotoImage(file ="Icon.png")
top.iconphoto(False,Icon)

CoderData = Label(text = " Made BY  \n\n **  YOSSEF  ESSAM  FOUAD  **" ,  font=('Georgia', 20, 'bold'), foreground = "blue")
CoderData.pack(side =TOP , pady = 30)

upload=Button(top,text="Cartoonify an Image",command=upload,padx=10,pady=5)
upload.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
upload.pack(side=TOP,pady=30)


def car(Image):
    # Local variables in the function which use to change the image
    line_Size, bluer, k , W, H= 7, 7, 50, 300,300

    # reading image
    img = cv2.imread(Image)
    # Resize Image
    img = cv2.resize(img, (W, H))

    # Edges
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Resize gray Image
    gray = cv2.resize(gray, (W, H))

    smoothGray = cv2.medianBlur(gray, bluer)
        # Resize SmoothGray Image
    smoothGray = cv2.resize(smoothGray, (W, H))

    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_Size, bluer)
        # Resize edges Image
    edges = cv2.resize(edges, (W, H))


    # Color contization
    data = np.float32(img).reshape((-1, 3))
    cre = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)

    ret, label, center = cv2.kmeans(data, k, None, cre, 10, cv2.KMEANS_RANDOM_CENTERS)

    center = np.uint8(center)

    result = center[label.flatten()]
    result = result.reshape(img.shape)
    # plt.imshow(result)


    # Cartoonization
    color = cv2.bilateralFilter(img, 7, 200, 200)
        # Resize Colored  Image
    color = cv2.resize(color, (W, H))

    cartoon = cv2.bitwise_and(color, color, mask=edges)
        # Resize Cartoon Image
    cartoon =cv2.resize(cartoon, (W, H))


    # Plotting Image Transition
    images = [img, gray, smoothGray, edges, color, cartoon]
    fig, axes = plt.subplots(3, 2, figsize=(8, 8), subplot_kw={'xticks': [], 'yticks': []},
                             gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.set_title(Name[i])
        ax.imshow(images[i], cmap='gray')

    # Save Button
    Save = Button(top, text="Save an Image", command=lambda: save(cartoon, Image), padx=10, pady=5)
    Save.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
    Save.pack(side=TOP, pady=100)
    plt.show()





top.mainloop()
