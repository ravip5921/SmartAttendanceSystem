from server import client_teacher

from numpy import spacing
from kivymd.app import MDApp

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivymd.uix.textfield import MDTextField
from kivymd.uix.datatables import MDDataTable

from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen


class LoginWindow(Screen):
    pass


class AttendanceWindow(Screen):
    pass


cardColor = [0.796875, 0.8984375, 0.99609375, 1]
textColor = [0, 0, 0, 1]
backgroundColor = [0.59765625, 0.8046875, 0.99609375, 1]

sm = ScreenManager()
sm.add_widget(LoginWindow(name="login"))
sm.add_widget(AttendanceWindow(name="attendance"))


class MainApp(MDApp):
    teacherId = ""

    classId = ""
    className = ""
    classList = []

    subjectId = ""
    subjectname = ""
    subjectList = []

    attendanceId = ""
    attendanceList = {}
    attendanceToBeDone = []
    attendanceListMini = []
    data_tables = None
    stop_btn = None
    present_btn = None

    def __init__(self, **kwargs):
        self.title = "Smart Attendance"
        super().__init__(**kwargs)

    def build(self):

        loginBg = MDBoxLayout()
        loginBg.md_bg_color = backgroundColor
        imageLayout = MDBoxLayout(size_hint=(0.15, 0.15),
                                  pos_hint={'center_x': .5, 'center_y': .9})
        imageObj = Image(source="./assets/icon.png")
        imageLayout.add_widget(imageObj)

        smallCard = MDBoxLayout()
        smallCard.md_bg_color = cardColor
        smallCard.size_hint = (0.5, 0.65)
        smallCard.radius = [40, 40, 40, 40]
        smallCard.orientation = "vertical"
        smallCard.pos_hint = {'center_x': .5, 'center_y': .5}

        teacherIDBox = MDBoxLayout()
        teacherIDBox.pos_hint = {'center_x': .5, 'center_y': .5}
        teacherIDBox.orientation = 'vertical'
        teacherIDBox.adaptive_height = True
        teacherIDBox.size_hint = (0.5, 1.0)

        self.teacherIDInp = MDTextField(hint_text="Teacher Id:")
        self.teacherIDInp.color_mode = "custom"
        self.teacherIDInp.line_color_normal = textColor
        self.teacherIDInp.line_color_focus = textColor
        self.teacherIDInp.hint_text_color = textColor
        self.teacherIDInp.pos_hint = {'center_x': .5, 'center_y': .2}

        self.classIDInp = MDTextField(hint_text="Class Id:")
        self.classIDInp.hint_text = "Class Id:"
        self.classIDInp.color_mode = "custom"
        self.classIDInp.line_color_normal = textColor
        self.classIDInp.line_color_focus = textColor
        self.classIDInp.hint_text_color = textColor
        self.classIDInp.pos_hint = {'center_x': .5, 'center_y': .2}

        teacherIDLabel = MDLabel(text="Teacher Id:")
        teacherIDLabel.size_hint = (1, 0.2)

        classIDLabel = MDLabel(text="Class Id:")
        classIDLabel.size_hint = (1, 0.2)

        teacherIDBox.add_widget(teacherIDLabel)
        teacherIDBox.add_widget(self.teacherIDInp)
        teacherIDBox.add_widget(classIDLabel)
        teacherIDBox.add_widget(self.classIDInp)

        connectButton = MDRaisedButton(text="Connect")
        connectButton.pos_hint = {'center_x': .5, 'center_y': .5}
        connectButton.bind(on_press=self.connectCallback)
        subjectNameLayout = MDBoxLayout(orientation="vertical")
        subjectNameLayout.pos_hint = {'center_x': .5, 'center_y': .5}
        subjectNameLayout.size_hint = (0.65, 0.5)
        subjectNameLayout.adaptive_height = True

        self.teacherName = MDLabel(pos_hint={'center_x': .5, 'center_y': .5})
        self.teacherName.text = ""

        self.subjectName = MDLabel(pos_hint={'center_x': .5, 'center_y': .5})
        self.subjectName.text = "No Connection"

        subjectNameLayout.add_widget(self.teacherName)
        subjectNameLayout.add_widget(self.subjectName)

        startButton = MDRaisedButton(text="Start")
        startButton.pos_hint = {'center_x': .5, 'center_y': .5}
        startButton.bind(on_release=self.startCallback)
        smallCard.add_widget(teacherIDBox)
        smallCard.add_widget(connectButton)
        smallCard.add_widget(subjectNameLayout)
        smallCard.add_widget(startButton)
        smallCard.add_widget(MDLabel(size_hint=(1, 0.2)))

        loginScreen = sm.get_screen("login")
        loginScreen.add_widget(loginBg)
        loginScreen.add_widget(imageLayout)
        loginScreen.add_widget(smallCard)
        ###########################################################################
        attendanceBg = MDBoxLayout()
        attendanceBg.md_bg_color = backgroundColor

        attendanceBox = MDBoxLayout(orientation="vertical")
        attendanceBox.pos_hint = {"center_x": .5, "center_y": .9}
        attendanceBox.size_hint = (0.9, 0.2)
        # attendanceBox.adaptive_height = True
        # attendanceBox = MDBoxLayout(spacing="40dp")
        # attendanceBox.md_bg_color = [1, 0, 0, 1]

        attendanceInnerBox1 = MDBoxLayout(orientation="horizontal")
        attendanceInnerBox1.size_hint = (1, 0.5)

        self.attendanceTextLabel = MDLabel(
            text="Attendance will time out in 10 minutes")

        backButton = MDRaisedButton(text="Back")
        backButton.bind(on_press=self.backCallback)

        attendanceInnerBox2 = MDBoxLayout(orientation="horizontal")
        attendanceInnerBox2.size_hint = (1, 0.5)

        self.attendanceCodeLabel = MDLabel(text="Attendance Code :")

        refreshButton = MDRaisedButton(text="Refresh")
        refreshButton.bind(on_press=self.refreshCallback)

        attendanceInnerBox1.add_widget(self.attendanceTextLabel)
        attendanceInnerBox1.add_widget(backButton)

        attendanceInnerBox2.add_widget(self.attendanceCodeLabel)
        attendanceInnerBox2.add_widget(refreshButton)

        attendanceBox.add_widget(attendanceInnerBox1)
        attendanceBox.add_widget(attendanceInnerBox2)

        # stopAttendanceButton = MDRaisedButton(text="Stop Attendance")
        # stopAttendanceButton.bind(on_press=self.stopAttendanceCallback)
                
        attendanceScreen = sm.get_screen("attendance")
        attendanceScreen.add_widget(attendanceBg)
        attendanceScreen.add_widget(attendanceBox)
        
        # attendanceScreen.add_widget(stopAttendanceButton)
        return sm

    def getSubject(self):
        try:
            subjectListFromServer = client_teacher.updateClassAndSubjects(
                self.teacherId)

            # # get subject list of each class teached by teacher
            # for i in subjectListFromServer["subject"]:
            #     self.subjectList.append(i)

            # print(subjectList)
            if "error" not in subjectListFromServer:
                # print(subjectListFromServer["teacher_name"])
                self.subjectId = subjectListFromServer["subject"][0][0]
                self.subjectname = subjectListFromServer["subject"][0][1]
                self.teacherName.text = str(
                    "Welcome, ") + str(subjectListFromServer["teacher_name"])
            # print(self.subjectId)
        except Exception as e:
            print("Subject retrival error", e)
        pass

    def startAttendanceSheet(self):
        try:
            AttendanceListFromServer = client_teacher.startAttendance(
                self.teacherId, self.classId, self.subjectId)

            print(self.teacherId, self.classId, self.subjectId)
            if "error" in AttendanceListFromServer:
                print(AttendanceListFromServer["error"])
                self.attendanceTextLabel.text = AttendanceListFromServer["error"]
            else:
                # save attendance code
                self.attendanceId = AttendanceListFromServer["acode"]
                for list in AttendanceListFromServer["student_list"]:
                    #print(list[0], list[1])
                    presence = "Absent"
                    presenceList = [list[1], presence]
                    self.attendanceList[list[0]] = presenceList
                print(AttendanceListFromServer["timeout"])
                self.attendanceTextLabel.text = AttendanceListFromServer["timeout"]

        except Exception as e:
            print("error :", e)

    def updateAttendanceSheet(self):
        try:
            AttendanceListFromServer = client_teacher.getAttendance(
                self.teacherId, self.classId)
            if "error" in AttendanceListFromServer:
                print(AttendanceListFromServer["error"])
            else:
                # update presence in list
                keys = AttendanceListFromServer["student_list"]
                # print(keys)
                for key in keys:
                    self.attendanceList[key][1] = "Present"
                self.widgetRemover()  # removes old instance of datatable,stop and present button
                attendanceScreen = sm.get_screen("attendance")
                # adds data table , stop and present button
                self.load_table(attendanceScreen)
        except Exception as e:
            print(e)

    def finalAttendanceSheet(self, *args):
        try:
            AttendanceListFromServer = client_teacher.stopAttendance(
                self.teacherId, self.classId)
            if "error" in AttendanceListFromServer:
                print(AttendanceListFromServer["error"])
                self.attendanceTextLabel.text = AttendanceListFromServer["error"]
            else:
                print(AttendanceListFromServer["success"])
                self.attendanceTextLabel.text = AttendanceListFromServer["success"]
        except Exception as e:
            print(e)

    def manualPresent(self, *args):

        try:
            for text in self.attendanceToBeDone:
                print("Done presence", text)
                client_teacher.markAttendance(
                    self.teacherId, self.classId, text)
        except:
            print("some error occured during manual attendance")

        # empty selected check for presence
        while len(self.attendanceToBeDone) > 0:
            self.attendanceToBeDone.pop()
        # print("After",self.attendanceToBeDone)
        self.updateAttendanceSheet()

    def startCallback(self, *args):
        self.startAttendanceSheet()
        self.attendanceCodeLabel.text = "Attendance Code: " + \
            str(self.attendanceId)
        sm.current = "attendance"
        attendanceScreen = sm.get_screen("attendance")
        self.load_table(attendanceScreen)

    def connectCallback(self, *args):
        self.classIDInp.text = self.classIDInp.text.upper()
        self.teacherId = self.teacherIDInp.text
        self.classId = self.classIDInp.text

        self.getSubject()
        # print("searching subject for", self.teacherID, self.classID)
        self.subjectName.text = str(self.subjectname)

    def stopAttendanceCallback(self, *args):
        self.finalAttendanceSheet()
        self.attendanceCodeLabel.text = "Attendance Code: "
        pass

    def backCallback(self, *args):
        sm.current = "login"

    def refreshCallback(self, *args):
        self.updateAttendanceSheet()
        self.widgetRemover()
        aScreen = sm.get_screen("attendance")
        self.load_table(aScreen)

    def stopCallback(self, *args):
        self.finalAttendanceSheet()
        pass

    def presentCallback(self, *args):
        self.manualPresent()
        attendanceScreen = sm.get_screen("attendance")
        self.widgetRemover()
        self.load_table(attendanceScreen)
        pass

    def load_table(self, aScreen):
        # list to make attendance list a list for initial insert in data table
        AttendListMini = []
        for key in self.attendanceList:
            AttendListMini.append(key)
            AttendListMini.append(self.attendanceList[key][0])
            AttendListMini.append(self.attendanceList[key][1])

        self.data_tables = MDDataTable(
            pos_hint={'center_y': 0.5, 'center_x': 0.5},
            size_hint=(0.7, 0.6),
            rows_num=48,
            check=True,
            # use_pagination=True,
            column_data=[
                ("Roll Number", dp(40)),
                ("Student", dp(30)),
                ("Presence", dp(30)), ],
            row_data=[
                (AttendListMini[i*3], AttendListMini[(i*3)+1],
                 AttendListMini[(i*3)+2])
                for i in range(int(len(AttendListMini)/3))
                # (f"{i + 1}", "2.23", "3.65")
                # for i in range(50)
            ],
        )

        self.data_tables.bind(on_check_press=self.check_press)

        self.stop_btn = MDRaisedButton(
            text="Stop",
            pos_hint={'center_y': 0.1, 'center_x': 0.6}
        )
        self.stop_btn.bind(on_press=self.stopCallback)

        self.present_btn = MDRaisedButton(
            text="Mark Present",
            pos_hint={'center_y': 0.1, 'center_x': 0.3}
        )
        self.present_btn.bind(on_press=self.presentCallback)

        aScreen.add_widget(self.data_tables)
        aScreen.add_widget(self.stop_btn)
        aScreen.add_widget(self.present_btn)

        # return layout

    def check_press(self, instance_table, current_row):
        print(current_row)
        self.attendanceToBeDone.append(current_row[0])

    def widgetRemover(self):
        attendanceScreen = sm.get_screen("attendance")
        attendanceScreen.remove_widget(self.data_tables)
        attendanceScreen.remove_widget(self.stop_btn)
        attendanceScreen.remove_widget(self.present_btn)
        # attendanceScreen.clear_widgets()
        # attendanceScreen.add_widget(MDLabel(text="hi ravi"))


if __name__ == "__main__":
    MainApp().run()
