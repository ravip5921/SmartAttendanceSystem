import server.client_student


import cv2
import face_recognition
import os

from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButton, MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
# from kivymd.uix.behaviors.backgroundcolor_behavior import BackgroundColorBehavior

textColor = [0, 0, 0, 1]
dialogTextColor = [0, 0, 0, 1]
textInpBgColor = [0.796875, 0.8984375, 0.99609375, 1]
appBgColor = [0.30078125, 0.76171875, 0.99609375, 1]
textLineColorFocus = [0.01171875, 0.515625, 0.984375, 1]
textLineColorNormal = [0.984375, 0.53125, 0.0117, 1]

Window.top = 50
#Window.size = (540, 960)
Window.size = (400,700)
filePresent = True
pictureRemoved = False
try:
    fileP = open("./userData.txt", "r")
except:
    filePresent = False
    pass


class StudentApp(MDApp):
    rollNoSaved = ""
    pictureRemoved = False

    def build(self):
        # app LOGO
        self.theme_cls.theme_style = "Light"
        imageObj = Image(source="./assets/icon.png")
        # layout for image of logo
        imageLayout = MDBoxLayout(size_hint=(0.35, 0.35),
                                  pos_hint={'x': 0.325, 'y': 0.2})
        imageLayout.add_widget(imageObj)
        # widgets for input
        rollNoL = MDLabel(text="  Roll No:", theme_text_color="Custom")
        rollNoL.text_color = textColor
        AttendanceCodeL = MDLabel(
            text="  Attendance Code:", theme_text_color="Custom")
        AttendanceCodeL.text_color = textColor

        self.rollNoT = MDTextField(hint_text="Enter Roll no :")
        self.rollNoT.color_mode = "custom"
        # self.rollNoT.fill_color = [0.0117, 0.96875, 0.984375, 1]
        self.rollNoT.line_color_focus = textLineColorFocus
        self.rollNoT.line_color_normal = textLineColorNormal
        # self.rollNoT.mode = "fill"

        self.AttendanceCodeT = MDTextField(
            hint_text="Enter Attendance Code : ")
        self.AttendanceCodeT.color_mode = "custom"
        self.AttendanceCodeT.line_color_focus = textLineColorFocus
        self.AttendanceCodeT.line_color_normal = textLineColorNormal

        inputLayout = MDBoxLayout(orientation="vertical",

                                  pos_hint={'x': 0.1, 'y': 0.1}
                                  )
        inputLayout2 = MDBoxLayout(orientation="vertical",

                                   pos_hint={'x': 0.1, 'y': 0.1}
                                   )

        # setting text of roll no from saved file
        if filePresent:
            self.rollNoT.text = fileP.readline()
            fileP.close()

        inputLayout.size_hint = (0.8, 0.25)
        inputLayout.radius = [20, 7, 20, 7]
        # inputLayout.md_bg_color = [0.328125, 0.31640625, 0.8359375, 1]
        inputLayout.md_bg_color = textInpBgColor

        spacer = MDBoxLayout(size_hint=(1, 0.1))
        inputLayout2.size_hint = (0.8, 0.25)
        inputLayout2.radius = [20, 7, 20, 7]
        # inputLayout2.md_bg_color = [0.328125, 0.31640625, 0.8359375, 1]
        inputLayout2.md_bg_color = textInpBgColor
        # Adding widgets for input to input layout
        inputLayout.add_widget(MDLabel())
        inputLayout.add_widget(rollNoL)
        inputLayout.add_widget(self.rollNoT)
        inputLayout2.add_widget(MDLabel())

        # inputLayout.add_widget(MDLabel())
        inputLayout2.add_widget(MDLabel())
        inputLayout2.add_widget(AttendanceCodeL)
        inputLayout2.add_widget(self.AttendanceCodeT)
        inputLayout2.add_widget(MDLabel())

        # Message label
        self.messageL = MDLabel(
            text="Error", theme_text_color="Custom")
        self.messageL.text_color = dialogTextColor
        # Layout for Message

        # self.dismissButton = MDRaisedButton(text="Okay",
        #                                     pos_hint={'x': 0.7})
        self.messageDialog = MDDialog(text="Dialog",
                                      size_hint=(0.8, 0.2),
                                      radius=[20, 7, 20, 7])
        #   size_hint=(0.8, 0.9),
        #   pos_hint={'x': 0.1, 'y': 0.5},
        #   Buttons=[self.dismissButton])
        # self.dismissButton.bind(on_press=self.messageDialog.dismiss)

        # messageDialogBox = MDBoxLayout(orientation="vertical",
        #                                size_hint=(0.8, 1),
        #                                pos_hint={'y': 0.8})

        # messageDialogBox.add_widget(self.messageL)
        # messageDialogBox.add_widget(self.dismissButton)
        # self.messageDialog.buttons.append(self.dismissButton)
        # self.messageDialog.add_widget(messageDialogBox)

        messageLayout = MDBoxLayout(orientation="vertical",
                                    size_hint=(0.8, 0.4),
                                    pos_hint={'x': 0.1, 'y': 0.1}
                                    )
        self.authenticateL = MDLabel(
            text="Authenticate your face:", theme_text_color="Custom")

        self.authenticateL.text_color = textColor
        messageLayout.add_widget(self.authenticateL)
        # messageLayout.add_widget(self.messageDialog)

        # Camera object
        self.cameraObj = Camera()
        self.cameraObj.resolution = (640, 480)
        self.cameraObj.play = True
        cameraLayout = MDBoxLayout(size_hint=(0.8, 1),
                                   pos_hint={'x': 0.1})
        cameraLayout.add_widget(self.cameraObj)
        # Capture Button
        self.buttonObj = MDFloatingActionButton(icon='camera')
        # self.buttonObj.size_hint = (.2, .2)
        self.buttonObj.pos_hint = {'x': .45, 'bottom': 0.1}
        self.buttonObj.bind(on_press=self.takeImage)
        self.buttonObj.md_bg_color = [0.796875, 0.8984375, 0.99609375, 1]
        # layout for camera and capture button
        myBoxLayout = MDBoxLayout(
            orientation="vertical",
            md_bg_color=appBgColor
            # md_bg_color=[0.796875, 1, 1, 1]
        )

        myBoxLayout.add_widget(imageLayout)
        myBoxLayout.add_widget(MDLabel(text=" ", size_hint=(1, 0.2)))
        myBoxLayout.add_widget(inputLayout)
        myBoxLayout.add_widget(spacer)
        myBoxLayout.add_widget(inputLayout2)
        myBoxLayout.add_widget(messageLayout)
        myBoxLayout.add_widget(cameraLayout)
        myBoxLayout.add_widget(self.buttonObj)
        myBoxLayout.add_widget(MDLabel(text=" ", size_hint=(1, 0.1)))

        return myBoxLayout

    def takeImage(self, *args):
        if self.AttendanceCodeT.text == "" or self.rollNoT == "":
            # self.messageL.text = "Enter all values"
            self.messageDialog.text = "Enter all values"
            self.messageDialog.open()
        else:
            self.filename = str(self.rollNoT.text + "+" +
                                self.AttendanceCodeT.text+".png")
            self.rollNo = str(self.rollNoT.text)
            self.acode = self.AttendanceCodeT.text
            print(self.filename)

            try:
                self.cameraObj.export_to_png(self.filename)
                imag = face_recognition.load_image_file(self.filename)
                imag = cv2.cvtColor(imag, cv2.COLOR_BGR2RGB)
                self.encodingsData = face_recognition.face_encodings(imag)
                if len(self.encodingsData) > 0:
                    self.encodingsData = self.encodingsData[0]
                    self.encodingsData = self.encodingsData.tolist()
                    # print(self.encodingsData)
                    #  Send embeddings to server
                    print(self.rollNo)
                    dataFromServer = server.client_student.markAttendance(
                        self.rollNo, int(self.acode), self.encodingsData)
                    # print(dataFromServer)
                    if "error" in dataFromServer:
                        print(dataFromServer["error"])
                        # self.authenticateL.text = str(dataFromServer["error"])
                        self.messageDialog.text = str(dataFromServer["error"])
                        self.messageDialog.open()

                    else:
                        print(dataFromServer["success"])
                        self.authenticateL.text = str(
                            dataFromServer["success"])
                        # self.messageDialog.text = str(dataFromServer["error"])
                        # self.messageDialog.open()

                    try:
                        os.remove(self.filename)
                        self.pictureRemoved = True
                    except Exception as e:
                        print("Image file remove error: ", e)

                    if filePresent:
                        try:
                            os.remove("./userData.txt")

                        except Exception as e:
                            print("Text file remove error: ", e)

                    try:
                        fileP = open("./userData.txt", "w")
                        fileP.write(self.rollNo)

                    except Exception as e:
                        print("File error: ", e)
                else:
                    self.authenticateL.text = "No face detected. Try Again"
                    os.remove(self.filename)
            except Exception as e:
                # print("No face detected.")
                print("Error :", e)
                if not self.pictureRemoved:
                    os.remove(self.filename)
                self.encodingsData = None


if __name__ == "__main__":
    StudentApp().run()
