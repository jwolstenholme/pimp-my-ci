from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.clock import mainthread
from pimp_my_ci import PimpMyCi
import threading
import time

SIZE  = 15

class CanvasApp(App):

    def on_stop(self):
        self.pimp_my_ci.stop()

    def build(self):
        threading.Thread(target=self.start).start()
        return self.create_screen()

    def start(self):
        self.pimp_my_ci = PimpMyCi(self)
        self.pimp_my_ci.start()

    def create_screen(self):
        self.root = BoxLayout(spacing=SIZE)

        for i in range(32):
            led = Led()
            led.create(i)
            self.root.add_widget(led)

        return self.root

    @mainthread
    def fillOff(self):
        self.fillRGB(0, 0, 0, 0, 32)

    @mainthread
    def fillRGB(self, r, g, b, start=0, end=0):
        for i in range(start, end):
            led = self.root.children[i]
            led.update(r, g, b)

class Led(Widget):

    def create(self, index):
        with self.canvas:
            self.color = Color(0, 0, 0, 1, mode='rgba')
            self.rect = Rectangle(pos=(SIZE * 2 * index, 10), size=(SIZE, SIZE))

    def update(self, r, g, b):
        self.color.rgb = [r/255, g/255, b/255, 1]


if __name__ == '__main__':
    CanvasApp().run()



