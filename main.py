import PIL
import kivy, sys, os.path
kivy.require('1.11.1')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.button import Button
import webbrowser
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from PIL import Image
from io import BytesIO


class MyScreenManager(ScreenManager):

    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)
        Window.bind(on_dropfile=self._on_file_drop)

    def resizeSmallAndRead(self):
        global RGBValues
        global userImage
        userImage = Image.open(fileLocation, 'r')
        originalWidth, originalHeight = userImage.size

        while originalWidth * originalHeight > 4000:
            originalWidth *= 0.9
            originalHeight *= 0.9

        resizedWidth = int(round(originalWidth))
        resizedHeight = int(round(originalHeight))
        smallImage = userImage.resize((resizedWidth, resizedHeight), PIL.Image.ANTIALIAS)
        RGBValues = list(smallImage.getdata())

    def deleteDups(self):
         if deleteDups == 'Yes':
            x = 1
            for vals in RGBValues:
                y = 0
                for nums in vals:
                    try:
                        if nums != RGBValues[x][y]:
                            break
                        elif y > 1:
                            RGBValues[x - 1] = None
                            break
                        else:
                            y += 1
                            continue
                    except:
                        break
                x += 1

            while None in RGBValues:
                RGBValues.remove(None)

    def createImage(self):
        global finalImage
        lengthOfImage = len(RGBValues)

        # changed the length of the image for vertical and horizontal lines
        if orientation == 'Horizontal':
            finalImage = Image.new(userImage.mode, (1, lengthOfImage))
        else:
            finalImage = Image.new(userImage.mode, (lengthOfImage, 1))

        finalImage.putdata(RGBValues)

        # finds the length of the new image to match desired ratio
        if orientation == 'Vertical':
            newLength = round((int(ratioList[0]) * lengthOfImage) / int(ratioList[1]))
            finalImage = finalImage.resize((newLength, lengthOfImage), PIL.Image.ANTIALIAS)
        else:
            newLength = round((int(ratioList[1]) * lengthOfImage) / int(ratioList[0]))
            finalImage = finalImage.resize((lengthOfImage, newLength), PIL.Image.ANTIALIAS)

    def saveImage(self):
        content =Button(text='Image Saved', background_normal='', background_color=(.15, .15, .15, .6), font_size=20)
        savedPopup = Popup(title='Image Saved', content=content, size_hint=(.6, .6))
        content.bind(on_press=savedPopup.dismiss)
        try:
            cutStringIndex = filePath.rfind('\\')
            saveLocation = filePath[:cutStringIndex + 1]
            finalImage.save(saveLocation + userImageText + '.png')
            savedPopup.open()
        except:
            pass

    def openWebsite(self):
        webbrowser.open('https://ryan-w-c.github.io/')

    def openGitHub(self):
        webbrowser.open('https://github.com/ryan-w-c')

    def _on_file_drop(self, window, file_path):
        global fileLocation
        global fileCheck
        global filePath
        fileCheck = True
        fileLocation = file_path
        filePath = file_path.decode("utf-8")
        self.ids.userImageDrop.source = filePath

    def on_state_orientation(self, state, text):
        global orientation
        global orientationCheck
        orientationCheck = True
        orientation = text

    def on_state_ratio(self, state, text):
        global fileRatio
        global ratioCheck
        global ratioList
        ratioCheck = True
        fileRatio = text
        ratioList = fileRatio.split(':')

    def on_state_delete(self, state, text):
        global deleteDups
        global deleteCheck
        deleteCheck = True
        deleteDups = text

    def process(self):
        try:
            if fileCheck and orientationCheck and ratioCheck and deleteCheck:
                self.resizeSmallAndRead()
                self.deleteDups()
                self.createImage()
                data = BytesIO()
                finalImage.save(data, format='png')
                data.seek(0)
                previewIm = CoreImage(BytesIO(data.read()), ext='png')
                self.ids.previewImage.texture = previewIm.texture
                self.ids.savePreview.texture = previewIm.texture
                self.ids.saveButton.disabled = False
        except:
            pass


class RGBColorImageApp(App):

    def build(self):
        return MyScreenManager()

    def processText(self):
        global userImageText
        userImageText = self.root.ids.saveText.text


RGBColorImageApp().run()