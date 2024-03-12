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
        print("[Log 0] No input File: Code Terminated")
        return

    df = pd.read_csv('Student.csv', delimiter=',')

    presentees = []
    absentees = []

    dateObj = dt.datetime.now()
    dateStr = str(dateObj.date())

    pfname = 'Presentees '+dateStr+'.csv'
    afname = 'Absentees '+dateStr+'.csv'

    print('[Log 0] Verifying')

    unknownImage = fr.load_image_file(unknown_fp)
    unknownEncoding = fr.face_encodings(unknownImage)

    peopleCount = range(0, len(unknownEncoding))
    peopleCount = list(peopleCount)

    for index, row in df.iterrows():
        if index == 4:
            print("[Log 1] Half Done Successfully")

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

    print('[Log 2] Created new data frames')

    for i in presentees:
        pr_df.loc[len(pr_df)] = i

    for j in absentees:
        abs_df.loc[len(abs_df)] = j

    print('[Log 3] Updated the data frames')

    successLabel = Label(gui,
            text="Image Processed - Click to download",
            font=('Elianto', 20, 'bold'),
            fg='white',
            bg='#121212')
    
    successLabel.place(x=200, y=300)
    

def downloadFile():
    pr_df.to_csv(pfname, sep=',', index=False, encoding='utf-8')
    abs_df.to_csv(afname, sep=',', index=False, encoding='utf-8')

    print('[Log 4] Flushed the data to CSV files')

    print('[Log 5] Attendance Success')
    print('Presentees File: ' + pfname)
    print('Absentees File: ' + afname)

    prLabel = Label(gui,
            text='Presentees File: ' + pfname,
            font=('Elianto', 20, 'bold'),
            fg='white',
            bg='#121212')
    
    absLabel = Label(gui,
            text='Absentees File: ' + afname,
            font=('Elianto', 20, 'bold'),
            fg='white',
            bg='#121212')
    
    prLabel.place(x=180, y=500)
    absLabel.place(x=180, y=550)

gui = Tk()

icon = PhotoImage(file='GUI/logo.png')
button_image = PhotoImage(file='GUI/click.png')
download_image = PhotoImage(file='GUI/download.png')

gui.geometry("900x700")
gui.title("Smart Attendance System")
gui.iconphoto(True, icon)
gui.config(background="#121212")

canvas = Canvas(gui, bg="#121212", highlightthickness=0)
canvas.pack(fill="both", expand=True)

background_image = Image.open('GUI/background.png')
background_photo = ImageTk.PhotoImage(background_image)

label = Label(gui,
              text="Smart Attendance System",
              font=('Elianto', 25, 'bold'),
              fg='white',
              bg='#121212')

label.place(x=250, y=100)

log_label = Label(gui,
                  text="",
                  font=('Elianto', 12),
                  fg='white',
                  bg='#121212',
                  justify=LEFT)

log_label.place(x=50, y=250)

button = Button(gui,
                text='Choose Image!',
                font=('Comic Sans', 18, 'bold'),
                fg='#00FF00',
                bg='black',
                activeforeground='black',
                activebackground='white',
                image=button_image,
                compound='right',
                command=processImage)

button.place(x=330, y=200)

download = Button(gui,
                  text='Download Presentees and Absentees file!',
                  font=('Comic Sans', 18, 'bold'),
                  fg='#00FF00',
                  bg='black',
                  activeforeground='black',
                  activebackground='white',
                  image=download_image,
                  compound='right',
                  command=downloadFile)

download.place(x=200, y=400)

gui.mainloop()