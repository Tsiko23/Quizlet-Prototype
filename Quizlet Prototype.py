import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QWidget,
    QTableWidget, QTableWidgetItem, QMessageBox
)

class VocabularyTrainer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("სიტყვების დამხმარე აპლიკაცია")
        self.setGeometry(100, 100, 600, 500)

        self.words = []
        self.current_word = None

        self.load_words()

        self.english_input = QLineEdit()
        self.english_input.setPlaceholderText("ინგლისური სიტყვა")

        self.georgian_input = QLineEdit()
        self.georgian_input.setPlaceholderText("ქართული თარგმანი")

        self.add_button = QPushButton("დამატება")
        self.add_button.clicked.connect(self.add_word)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["English", "Georgian", "ქმედება"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.exercise_label = QLabel("დაიწყე ვარჯიში!")
        self.exercise_word = QLabel("")
        self.exercise_word.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("შეიყვანე თარგმანი...")

        self.check_button = QPushButton("შეამოწმე")
        self.check_button.clicked.connect(self.check_answer)

        self.next_button = QPushButton("შემდეგი სიტყვა")
        self.next_button.clicked.connect(self.next_exercise_word)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.english_input)
        input_layout.addWidget(self.georgian_input)
        input_layout.addWidget(self.add_button)

        exercise_layout = QVBoxLayout()
        exercise_layout.addWidget(self.exercise_label)
        exercise_layout.addWidget(self.exercise_word)
        exercise_layout.addWidget(self.answer_input)
        exercise_layout.addWidget(self.check_button)
        exercise_layout.addWidget(self.next_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.table)
        main_layout.addSpacing(20)
        main_layout.addLayout(exercise_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.update_table()

    def add_word(self):
        eng = self.english_input.text().strip()
        geo = self.georgian_input.text().strip()

        if not eng or not geo:
            QMessageBox.warning(self, "შეცდომა", "შეავსე ორივე ველი")
            return

        self.words.append({"eng": eng, "geo": geo})
        self.save_words()
        self.update_table()

        self.english_input.clear()
        self.georgian_input.clear()

    def delete_word(self, row):
        del self.words[row]
        self.save_words()
        self.update_table()

    def update_table(self):
        self.table.setRowCount(len(self.words))
        for i, word in enumerate(self.words):
            self.table.setItem(i, 0, QTableWidgetItem(word["eng"]))
            self.table.setItem(i, 1, QTableWidgetItem(word["geo"]))

            delete_btn = QPushButton("წაშლა")
            delete_btn.clicked.connect(lambda _, row=i: self.delete_word(row))
            self.table.setCellWidget(i, 2, delete_btn)

    def next_exercise_word(self):
        if not self.words:
            QMessageBox.information(self, "შეტყობინება", "ჯერ დაამატე სიტყვები")
            return

        self.current_word = random.choice(self.words)
        self.exercise_word.setText(self.current_word["geo"])
        self.answer_input.clear()
        self.exercise_label.setText("მოიფიქრე ინგლისურად:")

    def check_answer(self):
        if not self.current_word:
            QMessageBox.warning(self, "ყურადღება", "ჯერ დააჭირე 'შემდეგი სიტყვა'")
            return

        user_answer = self.answer_input.text().strip().lower()
        correct_answer = self.current_word["eng"].lower()

        if user_answer == correct_answer:
            QMessageBox.information(self, "შედეგი", "✅ სწორი პასუხია!")
        else:
            QMessageBox.warning(self, "შედეგი", f"❌ არასწორია. სწორი იყო: {self.current_word['eng']}")

        self.answer_input.clear()

    def save_words(self):
        with open("words.txt", "w", encoding="utf-8") as f:
            for word in self.words:
                f.write(f"{word['eng']},{word['geo']}\n")

    def load_words(self):
        try:
            with open("words.txt", "r", encoding="utf-8") as f:
                for line in f:
                    if "," in line:
                        eng, geo = line.strip().split(",", 1)
                        self.words.append({"eng": eng, "geo": geo})
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VocabularyTrainer()
    window.show()
    sys.exit(app.exec_())
