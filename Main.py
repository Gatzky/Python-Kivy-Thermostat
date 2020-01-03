from firebase import firebase
from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from time import sleep
from threading import Thread

FBConn = firebase.FirebaseApplication('https://thermostatgacagh.firebaseio.com/')
sliderTempValue = 0
sliderFinalValue = 0


class startButton(Button):
    def __init__(self, **kwargs):
        super(startButton, self).__init__(**kwargs)

    def on_press(self):
        Thread(target=startLogger).start()


class expTempSlider(Slider):
    def __init__(self, **kwargs):
        super(expTempSlider, self).__init__(**kwargs)

    def on_release(self):
        pass

    def on_touch_up(self, touch):
        super(expTempSlider, self).on_touch_up(touch)
        if touch.grab_current == self:
            global sliderFinalValue
            global sliderTempValue
            sliderFinalValue = sliderTempValue
            fbPath = "/Temperature/Kivy"
            FBConn.put(fbPath, 'Expected temperature', str(sliderFinalValue))
            expectedTempLabel.text = "Expected temperature: " + "%.2f" % sliderFinalValue + " C"
            return True


def callback_value(instance, value):
    global sliderTempValue
    sliderTempValue = value
    sliderLabel.text = str(sliderTempValue) + " C"


actualTempLabel = Label(text="Actual temperature: Unknown")
expectedTempLabel = Label(text="Expected temperature: Unknown")
heaterStateLabel = Label(text="Heater: Unknown")

startButtonInstance = startButton(text="Start")

expTempSliderInstance = expTempSlider(min=0, max=100, value=0, step=0.25)
expTempSliderInstance.bind(value=callback_value)
sliderLabel = Label(text="0.0 C")


class MainApp(App):
    def build(self):
        boxMain = BoxLayout(orientation='vertical')

        boxTempLabel = BoxLayout(orientation='vertical')

        boxTempLabel.add_widget(actualTempLabel)
        boxTempLabel.add_widget(expectedTempLabel)
        boxTempLabel.add_widget(heaterStateLabel)

        boxSlider = BoxLayout(orientation='vertical')

        boxSlider.add_widget(expTempSliderInstance)
        boxSlider.add_widget(sliderLabel)

        boxDevice = BoxLayout(orientation='vertical')

        boxDevice.add_widget(startButtonInstance)

        boxMain.add_widget(boxTempLabel)
        boxMain.add_widget(boxSlider)
        boxMain.add_widget(boxDevice)

        return boxMain


def startLogger():
    while True:
        function()
        sleep(1)


def function():
    fbPath = "/Temperature/Particle"
    actualTemp = FBConn.get(fbPath, 'Actual temperature')
    actualTempLabel.text = "Actual temperature: " + str(actualTemp) + " C"
    heaterFlag = FBConn.get(fbPath, 'Is heater active')
    if heaterFlag == "0":
        heaterStateLabel.text = "Heater: Off"
    else:
        heaterStateLabel.text = "Heater: On"


if __name__ == '__main__':
    MainApp().run()
