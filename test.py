from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Assuming you have 10 sliders
        self.sliders = [QSlider(Qt.Horizontal) for _ in range(10)]

        # Create a layout
        layout = QVBoxLayout()

        # Add sliders to the layout
        for slider in self.sliders:
            layout.addWidget(slider)
            # Connect each slider's valueChanged signal to a common function
            slider.valueChanged.connect(self.handle_slider_change)

        # Create a central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)

        # Set the central widget
        self.setCentralWidget(central_widget)

    def handle_slider_change(self, value):
        # Identify which slider triggered the change
        sender_slider = self.sender()

        # Find the index of the sender slider in the sliders list
        slider_index = self.sliders.index(sender_slider)

        # Perform actions based on the slider index or value
        print(f"Slider {slider_index + 1} value changed to {value}")
        # Your custom actions here...

if __name__ == "__main__":
    app = QApplication([])
    window = MyMainWindow()
    window.show()
    app.exec_()
