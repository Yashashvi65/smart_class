import tkinter as tk
from threading import *
import random
import time
import ctypes

from host import *

bgC = "#242424"
bgC2 = "#575a61"
fgC = "#f3f3f3"
b = "#09fa9a"

attendanceTime = 10

driverStartFlag = False

def fromRgb(rgb):
    return "#%02x%02x%02x" % rgb  

class ColorAnimation(Thread):
    def run(self):
        while(True):
            r = 9
            g = 250
            b = 153
            while (r < 255 or g < 255 or b < 255):
                global canvas
                global root
                global Title1Frame
                canvas.configure(bg=fromRgb((r,g,b)))
                canvas.configure(highlightbackground=fromRgb((r,g,b)))
                root.configure(background=fromRgb((r,g,b)))
                TitleCanvas.configure(bg=fromRgb((r,g,b)))
                TitleCanvas.configure(highlightbackground=fromRgb((r,g,b)))
                r = min(r + 1, 255)
                g = min(g + 1, 255)
                b = min(b + 1, 255)
                time.sleep(0.005)
            while (r > 9 or g > 250 or b > 153):
                canvas.configure(bg=fromRgb((r,g,b)))
                canvas.configure(highlightbackground=fromRgb((r,g,b)))
                root.configure(background=fromRgb((r,g,b)))
                TitleCanvas.configure(bg=fromRgb((r,g,b)))
                TitleCanvas.configure(highlightbackground=fromRgb((r,g,b)))
                r = max(r - 1, 9)
                g = max(g - 1, 250)
                b = max(b - 1, 153)
                time.sleep(0.005)
                

class Driver(Thread):
    def run(self):
        count = 0
        while(True):
            if (count >= attendanceTime):
                global maxa
                maxa += 1
                attendanceList = take_attendance(webdriver)
                totalStudents.set(str(len(attendanceList)))
                room.updateAttendance(attendanceList)
                updateTable()
                count = 0
            global maxp
            maxp +=1
            handsList = who_participates(webdriver)
            raisedHands.set(len(handsList))
            room.updateParticipation(handsList)
            time.sleep(1)
            count += 1
            

def updateTable():
    studentTable.delete(0, tk.END)
    for i in range(len(room.students)):
        global maxa
        global maxp
        if (maxa == 0 or maxp == 0):
            studentTable.insert(0, "")
            studentTable.insert(0, "")
            studentTable.insert(0, room.students[i].name)
            
        else:
            studentTable.insert(0, "")
            studentTable.insert(0, "Participation Score: " + str(int(100 * room.students[i].pscore/maxp)) + "%")
            studentTable.insert(0, "Attendance Percentage: " + str(int( 100 * room.students[i].ascore/maxa)) + "%")
            studentTable.insert(0, room.students[i].name)
            

def handleInsert():
    table.insert(0, inputVal.get() + " | hands: " + raisedHands.get())


class Student():
    def __init__(self, name):
        #Participation
        self.pscore = 0
        self.ascore = 0
        self.name = name

class Room():
    def __init__(self):
        self.students = []

    def updateParticipation(self, list):
        for i in range(len(list)):
            studentFound = False
            for j in range(len(self.students)):
                if (self.students[j].name == list[i]):
                    studentFound = True
                    self.students[j].pscore = self.students[j].pscore + 1
                    break
            if (studentFound == False):
                self.students.append(Student(list[i]))
    
    def updateAttendance(self, list):
        for i in range(len(list)):
            studentFound = False
            for j in range(len(self.students)):
                if (self.students[j].name == list[i]):
                    studentFound = True
                    self.students[j].ascore = self.students[j].ascore + 1
                    break
            if (studentFound == False):
                self.students.append(Student(list[i]))

room = Room()

def linkFunc():
    room_link = "https://us04web.zoom.us/wc/join/8343445317"
    headless = False
    global webdriver
    webdriver = launch(room_link, headless)
    driverStartFlag = True

def timeFunc():
    global attendanceTime
    attendanceTime = int(timeInputVal.get())
    print(attendanceTime)

def firstHandFunc():
    call_first(webdriver)
    print("message sent")

def setCCFunc():
    print("not implemented")

def main():
    global maxa
    maxa= 0
    global maxp
    maxp = 0
    
    linkFunc()
    

    global root
    root = tk.Tk()
    root.title("Smart Class")
    x = root.winfo_screenwidth()
    y = root.winfo_screenwidth()
    root.geometry('%dx%d' % (x, y))
    root.configure(background=b)
    global canvas
    canvas = tk.Canvas(root, highlightbackground=b, height=1000, width=300, bg=b)
    canvas.pack()
    

    #Title1Frame
    global TitleCanvas
    Title1Frame = tk.Frame(root, bg=b)
    Title1Frame.place(width=300, height=100, x=x/2-170, y=0)
    TitleCanvas = tk.Canvas(Title1Frame, highlightbackground=b, bg=b, width = 300, height = 100)
    #tk.Label(Title1Frame, text="Smart Class",fg="black", font=("Helvetica", 40)).pack(fill=tk.X)
    TitleCanvas.pack()      
    
    

    #LinkFrame
    LFrame = tk.Frame(root, bg=bgC)
    LFrame.place(width=300, height=200, x=2, y=110)
    MCLabel = tk.Label(LFrame, text="Enter Meeting Code", fg=fgC, bg=bgC, font=("Helvetica", 13)).pack(pady=5)
    global linkInputVal
    linkInputVal = tk.StringVar()
    LinkInputBox = tk.Entry(LFrame, bg=bgC, width = 18, textvariable = linkInputVal, fg=fgC, font=("Helvetica", 16))
    LinkInputBox.pack(pady=5)
    MPCLabel = tk.Label(LFrame, text="Enter Meeting PassCode", fg=fgC, bg=bgC, font=("Helvetica", 13)).pack(pady=5)
    global passcodeInputVal
    passcodeInputVal = tk.StringVar()
    passcodeInputBox = tk.Entry(LFrame, bg=bgC, width = 18, textvariable = passcodeInputVal, fg=fgC, font=("Helvetica", 16))
    passcodeInputBox.pack(pady=5)
    sethPhoto = tk.PhotoImage(file = "assets/set.png") 
    setButton = tk.Button(LFrame, highlightbackground='black', height=30, width=30, image=sethPhoto, command = linkFunc).pack(pady=5)

    
    #HandRaisedFrame
    global raisedHands
    raisedHands = tk.StringVar()
    HRFrame = tk.Frame(root, bg=bgC)
    HRFrame.place(width=300, height=100, x=2, y=330)
    raisedHands.set(0)
    HRLabel = tk.Label(HRFrame, text="Number of Raised Hands", fg=fgC, bg=bgC, font=("Helvetica", 13)).pack(fill=tk.X, pady=10)
    HRLabelVal = tk.Label(HRFrame, textvariable=raisedHands, fg=fgC, bg=bgC, font=("Helvetica", 30)).pack(fill=tk.X)
    

    #StudentsFrame
    global totalStudents
    totalStudents = tk.StringVar()
    totalStudents.set(0) 
    SFrame = tk.Frame(root, bg=bgC)
    SFrame.place(width=300, height=575, x=x-302, y=110)
    SLabel = tk.Label(SFrame, text="Students Present", fg=fgC, bg=bgC, font=("Helvetica", 15)).pack(fill=tk.X, pady=10)
    SLabelVal = tk.Label(SFrame, textvariable=totalStudents, fg=fgC, bg=bgC, font=("Helvetica", 30)).pack(fill=tk.X)
    SALabel = tk.Label(SFrame, text="Take Attendance", fg=fgC, bg=bgC, font=("Helvetica", 10)).pack(fill=tk.X, pady=5)
    global attendanceTime
    attendanceTime = 10
    setPhoto = tk.PhotoImage(file = "assets/set.png") 
    setButton = tk.Button(SFrame, highlightbackground='black', height=30, width=30, image=setPhoto).pack()
    global studentTable
    studentTable = tk.Listbox(SFrame, borderwidth=0, fg=fgC, bg=bgC2, font=("Helvetica", 10), height=y-600)
    studentTable.pack(fill=tk.X, padx=10, pady=10)

    #CCFrame
    CCFrame = tk.Frame(root, bg=bgC)
    CCFrame.place(width=300, height=100, x=2, y=460)
    CCLabel = tk.Label(CCFrame, text="Closed Captioning", fg=fgC, bg=bgC, font=("Helvetica", 15)).pack(fill=tk.X, pady=2)
    set2Photo = tk.PhotoImage(file = "assets/set.png") 
    setButton = tk.Button(CCFrame, highlightbackground='black', height=30, width=30, image=set2Photo).pack(pady=5)

    FFrame = tk.Frame(root, bg=bgC)
    FFrame.place(width=300, height=100, x=2, y=585)
    FLabel = tk.Label(FFrame, text="Get FeedBack", fg=fgC, bg=bgC, font=("Helvetica", 15)).pack(fill=tk.X, pady=2)
    set1Photo = tk.PhotoImage(file = "assets/set.png") 
    setButton = tk.Button(FFrame, highlightbackground='black', height=30, width=30, image=set1Photo).pack(pady=5)
    

    #Thread
    t1 = Driver()
    t1.start()
    print("driver room started")

    t2 = ColorAnimation()
    t2.start()

    root.mainloop()

if __name__ == '__main__':
    main()
