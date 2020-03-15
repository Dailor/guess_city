import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel, QMessageBox, QPushButton, QTextEdit
from PyQt5.Qt import QFont, QPixmap
from search_op import get_map

MAX_SCORE = 2
IMAGE_SIZE = 580, 520

CITIES_DICT = dict()

CITIES_DICT["Алматы"] = list()
CITIES_DICT["Алматы"].append("Парк первого президента, Алматы")
CITIES_DICT["Алматы"].append("Театр, Алматы")
CITIES_DICT["Алматы"].append("Мега, Алматы")

CITIES_DICT["Нур-Султан"] = list()
CITIES_DICT["Нур-Султан"].append("Байтерек, Нур-Султан")
CITIES_DICT["Нур-Султан"].append("Хан Шатыр, Нур-Султан")
CITIES_DICT["Нур-Султан"].append("Этно-мемориальный комплекс Карта Казахстана Атамекен, Нур-Султан")

CITIES_DICT["Лондон"] = list()
CITIES_DICT["Лондон"].append("Вестминстер Бридж роуд, Лондон")
CITIES_DICT["Лондон"].append("парк Риджентс, Лондон")
CITIES_DICT["Лондон"].append("парк Виктория, Лондон")


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.default_font = QFont()
        self.default_font.setPointSize(15)

        self.scores_1 = 0
        self.scores_2 = 0

        self.now_move = 1

        self.city_now = None
        self.city_obj = None
        self.city_obj_now = None

        self.loader_UI()

    def loader_UI(self):
        self.setGeometry(300, 300, 600, 600)

        self.move_label = QLabel(self)
        self.move_label.setGeometry(250, 70, 120, 30)
        self.move_label.setFont(self.default_font)
        self.move_label.setText(f"Now guess {self.now_move}")

        self.label_scores = QLabel(self)
        self.label_scores.setFont(self.default_font)
        self.label_scores.setText("0:0")
        self.label_scores.move(280, 0)

        self.cities_list = QComboBox(self)
        self.cities_list.currentTextChanged.connect(self.select_city)
        self.cities_list.setFont(self.default_font)
        self.cities_list.resize(150, 30)
        self.cities_list.move(230, 30)

        self.cities_list.addItem("")
        self.cities_list.addItems(CITIES_DICT.keys())

        self.city_obj_pic = QLabel(self)
        self.city_obj_pic.move(10, 30)
        self.city_obj_pic.resize(*IMAGE_SIZE)
        self.city_obj_pic.hide()

        self.btn_prev = QPushButton(self, text='<=')
        self.btn_prev.clicked.connect(self.switch_img)
        self.btn_prev.setGeometry(30, 560, 50, 30)
        self.btn_prev.id_btn = 1
        self.btn_prev.hide()

        self.btn_next = QPushButton(self, text='=>')
        self.btn_next.clicked.connect(self.switch_img)
        self.btn_next.setGeometry(520, 560, 50, 30)
        self.btn_next.id_btn = 2
        self.btn_next.hide()

        self.edit_answer = QTextEdit(self)
        self.edit_answer.setGeometry(245 - 30, 560, 150, 30)
        self.edit_answer.hide()

        self.btn_check = QPushButton(self, text='Check')
        self.btn_check.setGeometry(410 - 30, 560, 50, 30)
        self.btn_check.clicked.connect(self.check_ans)
        self.btn_check.hide()

    def switch_img(self):
        id_btn = self.sender().id_btn
        if id_btn == 1:
            self.city_obj_now -= 1
        else:
            self.city_obj_now += 1

        if self.city_obj_now < 0:
            self.city_obj_now = len(self.city_obj) - 1
        elif self.city_obj_now == len(self.city_obj):
            self.city_obj_now = 0

        self.set_obj_picture()

    def set_label_scores(self):
        self.label_scores.setText(f"{self.scores_1}:{self.scores_2}")

    def check_ans(self):
        ans = self.edit_answer.toPlainText()
        msg = QMessageBox(self)
        if ans == self.city_now:
            self.add_scores(True)
            msg.setText("Correct")
        else:
            self.add_scores(False)
            msg.setText('WRONG')
        msg.show()
        self.edit_answer.clear()

    def add_scores(self, add):
        if add is True:
            if self.now_move == 1:
                self.scores_1 += 1
            else:
                self.scores_2 += 1

        self.now_move = 1 if self.now_move == 2 else 2

        self.check_win()
        self.set_label_scores()

        self.move_label.setGeometry(250, 70, 120, 30)
        self.move_label.setText(f"Now guess {self.now_move}")
        self.label_scores.show()
        self.cities_list.show()

        self.city_obj_pic.hide()
        self.btn_next.hide()
        self.btn_prev.hide()
        self.edit_answer.hide()
        self.btn_check.hide()

    def check_win(self):
        if self.scores_1 > MAX_SCORE:
            text = 'FIRST'
        elif self.scores_2 > MAX_SCORE:
            text = 'SECOND'
        else:
            return False

        msg = QMessageBox(self)
        msg.setText(text)
        msg.setFont(self.default_font)
        msg.show()
        self.close()

    def select_city(self, city):
        self.cities_list.setCurrentIndex(0)
        if len(city) == 0:
            return

        self.city_now = city
        self.city_obj = CITIES_DICT[city]
        random.shuffle(self.city_obj)
        self.city_obj_now = 0

        self.move_label.setGeometry(250, 0, 120, 30)
        self.move_label.setText(f"Now guess {self.now_move}")

        self.label_scores.hide()
        self.cities_list.hide()

        self.city_obj_pic.show()
        self.btn_next.show()
        self.btn_prev.show()
        self.edit_answer.show()
        self.btn_check.show()

        self.set_obj_picture()

    def set_obj_picture(self):
        pic = get_map(self.city_obj[self.city_obj_now])
        qpix = QPixmap()
        qpix.loadFromData(pic)
        qpix = qpix.scaled(*IMAGE_SIZE)
        self.city_obj_pic.setPixmap(qpix)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec())
