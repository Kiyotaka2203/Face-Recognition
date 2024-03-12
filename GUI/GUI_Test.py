from tkinter import *
import pandas as pd
from tkinter import filedialog as fd
import datetime as dt
from PIL import Image, ImageTk
import face_recognition as fr

def processImage():
    global pr_df, abs_df
    global pfname, afname

    unknown_fp = fd.askopenfilename(filetypes=[("JPEG files", "*.jpg;*.jpeg")])
    if not unknown_fp:
        update_log("[Log 0] No input File: Code Terminated")
        return

    update_log(unknown_fp)

    df = pd.read_csv('Student.csv', delimiter=',')

    presentees = []
    absentees = []

    dateObj = dt.datetime.now()
    dateStr = str(dateObj.date())

    pfname = 'Presentees '+dateStr+'.csv'
    afname = 'Absentees '+dateStr+'.csv'

    update_log('[Log 0] Verifying')

    unknownImage = fr.load_image_file(unknown_fp)
    unknownEncoding = fr.face_encodings(unknownImage)

    peopleCount = range(0, len(unknownEncoding))
    peopleCount = list(peopleCount)

    for index, row in df.iterrows():
        if index == 4:
            update_log("[Log 1] Half Done Successfully")

        StudPath = row['File Path']

        knownImage = fr.load_image_file(StudPath)
        knownEncoding = fr.face_encodings(knownImage)[0]

        for i in peopleCount:
            results = fr.compare_faces([knownEncoding], unknownEncoding[i])

            if results[0]:
                peopleCount.remove(i)
                presentees.append([row['Reg No'], row['Name']])
                break

        mylist = [row['Reg No'], row['Name']]

        if mylist not in presentees:
            absentees.append(mylist)

    pr_df = pd.DataFrame(columns=['Reg No', 'Name'])
    abs_df = pd.DataFrame(columns=['Reg No', 'Name'])

    update_log('[Log 2] Created new data frames')

    for i in presentees:
        pr_df.loc[len(pr_df)] = i

    for j in absentees:
        abs_df.loc[len(abs_df)] = j

    update_log('[Log 3] Updated the data frames')
    update_log('Image processed successfully!')
    

def downloadFile():
    global pfname, afname
    if pfname and afname:   
        presentees_file = fd.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if presentees_file:
            pr_df.to_csv(presentees_file, sep=',', index=False, encoding='utf-8')

        absentees_file = fd.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if absentees_file:
            abs_df.to_csv(absentees_file, sep=',', index=False, encoding='utf-8')

        update_log('[Log 4] Files Saved Successfully')

def update_log(text):
    def update():
        log_label.config(text=log_label.cget("text") + "\n" + text)
        log_label.update_idletasks()  # Update the GUI immediately
    gui.after(500, update)  # Delay of 500 milliseconds (0.5 second) between each log update

gui = Tk()

icon = PhotoImage(file='GUI/logo.png')
background_image = PhotoImage(file='GUI/Back.png')

button_image = PhotoImage(file='GUI/click.png')
download_image = PhotoImage(file='GUI/download.png')

gui.geometry("900x900")
gui.title("Smart Attendance System")
gui.iconphoto(True, icon)
gui.config(background="#FFFFFF")  # Change background color to white

background_label = Label(gui, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

label = Label(gui,
              text="Smart Attendance System",
              font=('Elianto', 25, 'bold'),
              fg='white',
              bg='#121212')

label.place(x=250, y=50)  # Adjusted position

log_label = Label(gui,
                  text="",
                  font=('Elianto', 12),
                  fg='#32CD32',  # Lime color
                  justify=LEFT,
                  bg='#202020')  # Change background color to white

log_label.place(x=220, y=250, width=300, height=200)  # Adjusted position and reduced width and height

button = Button(gui,
                text='Choose Image!',
                font=('Comic Sans', 18, 'bold'),
                fg='#FFFFFF',  # Changed text color to white
                bg='#4CAF50',  # Green color
                activeforeground='#FFFFFF',  # Changed active text color to white
                activebackground='#008CBA',  # Dark blue color
                image=button_image,
                compound='right',
                command=processImage)

button.place(x=330, y=150)  # Adjusted position

download = Button(gui,
                  text='Download Presentees and Absentees file!',
                  font=('Comic Sans', 18, 'bold'),
                  fg='#FFFFFF',  # Changed text color to white
                  bg='#4CAF50',  # Green color
                  activeforeground='#FFFFFF',  # Changed active text color to white
                  activebackground='#008CBA',  # Dark blue color
                  image=download_image,
                  compound='right',
                  command=downloadFile)

download.place(x=150, y=600)  # Adjusted position

gui.mainloop()
