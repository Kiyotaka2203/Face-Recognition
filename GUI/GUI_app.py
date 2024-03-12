import tkinter as tk
from tkinter import filedialog as fd
from PIL import Image, ImageTk
import pandas as pd
import datetime as dt
import face_recognition as fr

class SmartAttendanceApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Smart Attendance System")
        self.master.geometry("900x900")
        self.master.config(background="#121212")
        self.master.iconphoto(True, tk.PhotoImage(file='GUI/logo.png'))

        self.label = tk.Label(master, text="Smart Attendance System", font=('Elianto', 25, 'bold'), fg='white', bg='#121212')
        self.label.place(x=250, y=100)

        self.log_label = tk.Label(master, text="", font=('Elianto', 12), fg='#32CD32', justify=tk.LEFT, bg='#121212')
        self.log_label.place(x=50, y=250, width=800, height=400)

        self.button_image = tk.PhotoImage(file='GUI/click.png')
        self.download_image = tk.PhotoImage(file='GUI/download.png')

        self.button = tk.Button(master, text='Choose Image!', font=('Comic Sans', 18, 'bold'), fg='#00FF00', bg='black',
                                activeforeground='black', activebackground='white', image=self.button_image, compound='right',
                                command=self.process_image)
        self.button.place(x=330, y=200)

        self.download = tk.Button(master, text='Download Presentees and Absentees file!', font=('Comic Sans', 18, 'bold'),
                                  fg='#00FF00', bg='black', activeforeground='black', activebackground='white',
                                  image=self.download_image, compound='right', command=self.download_file)
        self.download.place(x=200, y=600)

    def update_log(self, text):
        self.log_label.config(text=self.log_label.cget("text") + "\n" + text)

    def process_image(self):
        unknown_fp = fd.askopenfilename(filetypes=[("JPEG files", "*.jpg;*.jpeg")])
        if not unknown_fp:
            self.update_log("[Log 0] No input File: Code Terminated")
            return

        self.update_log(unknown_fp)

        df = pd.read_csv('Student.csv', delimiter=',')
        presentees = []
        absentees = []

        dateObj = dt.datetime.now()
        dateStr = str(dateObj.date())

        pfname = 'Presentees '+dateStr+'.csv'
        afname = 'Absentees '+dateStr+'.csv'

        self.update_log('[Log 0] Verifying')

        unknownImage = fr.load_image_file(unknown_fp)
        unknownEncoding = fr.face_encodings(unknownImage)

        peopleCount = range(0, len(unknownEncoding))
        peopleCount = list(peopleCount)

        for index, row in df.iterrows():
            if index == 4:
                self.update_log("[Log 1] Half Done Successfully")

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

        self.update_log('[Log 2] Created new data frames')

        for i in presentees:
            pr_df.loc[len(pr_df)] = i

        for j in absentees:
            abs_df.loc[len(abs_df)] = j

        self.update_log('[Log 3] Updated the data frames')

    def download_file(self):
        presentees_file = fd.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if presentees_file:
            pr_df.to_csv(presentees_file, sep=',', index=False, encoding='utf-8')

        absentees_file = fd.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if absentees_file:
            abs_df.to_csv(absentees_file, sep=',', index=False, encoding='utf-8')

        self.update_log('[Log 4] Files Saved Successfully')

def main():
    root = tk.Tk()
    app = SmartAttendanceApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
