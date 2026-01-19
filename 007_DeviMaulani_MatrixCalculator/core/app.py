import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget
from PyQt5.QtCore import Qt

from views.welcome_view import WelcomePage
from views.matrix_view import MatrixCalculatorPage
from views.vector_view import VectorCalculatorPage
from views.spl_view import SPLCalculatorPage
from views.quiz_view import QuizPage
from views.quiz_setup_view import QuizSetupPage
from core.theme import app_stylesheet


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kalkulator Aljabar Linear")
        self.setGeometry(100, 100, 1000, 720)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Pages
        self.welcome = WelcomePage(self.navigate)
        self.matrix_page = MatrixCalculatorPage(self.navigate)
        self.vector_page = VectorCalculatorPage(self.navigate)
        self.spl_page = SPLCalculatorPage(self.navigate)
        self.quiz_page = QuizPage(self.navigate)
        self.quiz_setup_page = QuizSetupPage(self.navigate)

        # Add to stack
        self.stack.addWidget(self.welcome)       # index 0
        self.stack.addWidget(self.matrix_page)   # index 1
        self.stack.addWidget(self.vector_page)   # index 2
        self.stack.addWidget(self.spl_page)      # index 3
        self.stack.addWidget(self.quiz_page)     # index 4
        self.stack.addWidget(self.quiz_setup_page)  # index 5

        self.navigate("welcome")

    def navigate(self, target: str):
        targets = {
            "welcome": 0,
            "matrix": 1,
            "vector": 2,
            "spl": 3,
            "quiz": 4,
            "quiz_setup": 5,
        }
        if target in targets:
            # If going back to welcome, reset all pages
            if target == "welcome":
                try:
                    self.matrix_page.reset()
                except Exception:
                    pass
                try:
                    self.vector_page.reset()
                except Exception:
                    pass
                try:
                    self.spl_page.reset()
                except Exception:
                    pass
                try:
                    self.quiz_page.stop_music()
                    self.quiz_page.reset()
                except Exception:
                    pass
            if target == "quiz":
                try:
                    self.quiz_page.reset()
                    self.quiz_page.play_music()
                except Exception:
                    pass
            self.stack.setCurrentIndex(targets[target])


def run():
    app = QApplication(sys.argv)
    # Apply global theme
    app.setStyleSheet(app_stylesheet())
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
