from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox,
    QRadioButton, QButtonGroup, QTextEdit, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt, QUrl

try:
    from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
    MULTIMEDIA_AVAILABLE = True
except Exception:
    MULTIMEDIA_AVAILABLE = False

import os
from logic.quiz_bank import get_random_question
from core.state import APP_STATE


class QuizPage(QWidget):
    def __init__(self, navigate):
        super().__init__()
        self.navigate = navigate
        self.player = None
        self.music_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'quiz_music.mp3')
        self.music_path = os.path.normpath(self.music_path)
        self._init_ui()
        self._init_player()
        self.reset()

    def _init_player(self):
        if MULTIMEDIA_AVAILABLE and os.path.exists(self.music_path):
            try:
                self.player = QMediaPlayer()
                self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.music_path)))
            except Exception:
                self.player = None
        else:
            self.player = None

    def _init_ui(self):
        root = QVBoxLayout(self)

        # Header
        header = QHBoxLayout()
        title = QLabel("Kuis Interaktif Aljabar Linear")
        title.setStyleSheet("font-size:30px; font-weight:700;")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        header.addStretch()
        header.addWidget(title, alignment=Qt.AlignCenter)
        header.addStretch()
        btn_back = QPushButton("Kembali")
        btn_back.clicked.connect(self._back)
        header.addWidget(btn_back)
        root.addLayout(header)

        sep = QFrame(); sep.setFrameShape(QFrame.HLine); sep.setFrameShadow(QFrame.Sunken)
        root.addWidget(sep)

        # Controls row
        ctrl = QHBoxLayout()
        ctrl.addWidget(QLabel("Level:"))
        self.cb_level = QComboBox(); self.cb_level.addItems(["Easy", "Medium", "Hard"])
        self.cb_level.setEnabled(False)  # level is pre-chosen in setup
        self.cb_level.setToolTip("Level dipilih di halaman setup kuis")
        ctrl.addWidget(self.cb_level)
        self.btn_music = QPushButton("Matikan Musik")
        self.btn_music.clicked.connect(self._toggle_music)
        ctrl.addWidget(self.btn_music)
        ctrl.addStretch()
        self.lbl_progress = QLabel("Soal: 0/0")
        self.lbl_progress.setStyleSheet("font-weight:700;")
        ctrl.addWidget(self.lbl_progress)
        self.lbl_score = QLabel("Skor: 0")
        self.lbl_score.setStyleSheet("font-weight:700;")
        ctrl.addWidget(self.lbl_score)
        root.addLayout(ctrl)

        # Question area
        self.prompt = QTextEdit(); self.prompt.setReadOnly(True)
        self.prompt.setStyleSheet("font-family: Consolas, monospace; font-size:14px;")
        root.addWidget(self.prompt)

        self.options_group = QButtonGroup(self)
        self.opt_buttons = []
        opts_layout = QVBoxLayout()
        for i in range(3):
            rb = QRadioButton(f"Pilihan {i+1}")
            self.options_group.addButton(rb, i)
            self.opt_buttons.append(rb)
            opts_layout.addWidget(rb)
        root.addLayout(opts_layout)

        # Feedback area
        self.feedback = QTextEdit(); self.feedback.setReadOnly(True)
        self.feedback.setStyleSheet("font-family: Consolas, monospace; font-size:14px;")
        root.addWidget(self.feedback)

        # Action row
        actions = QHBoxLayout()
        self.btn_next = QPushButton("Mulai Kuis")
        self.btn_next.clicked.connect(self._next_question)
        actions.addWidget(self.btn_next)
        self.btn_submit = QPushButton("Kirim Jawaban")
        self.btn_submit.clicked.connect(self._submit)
        actions.addWidget(self.btn_submit)
        actions.addStretch()
        root.addLayout(actions)

    def _back(self):
        self.stop_music()
        self.navigate("welcome")

    def _toggle_music(self):
        if not self.player:
            QMessageBox.information(self, "Info", "Musik tidak tersedia. Pastikan file assets/quiz_music.mp3 ada.")
            return
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.btn_music.setText("Hidupkan Musik")
        else:
            self.player.play()
            self.btn_music.setText("Matikan Musik")

    def play_music(self):
        if self.player:
            self.player.play()
            self.btn_music.setText("Matikan Musik")

    def stop_music(self):
        if self.player:
            self.player.stop()
            self.btn_music.setText("Hidupkan Musik")

    def reset(self):
        self.level = APP_STATE.quiz_level
        # set combobox 
        try:
            idx = ["Easy", "Medium", "Hard"].index(self.level)
            self.cb_level.setCurrentIndex(idx)
        except Exception:
            self.cb_level.setCurrentIndex(0)
            self.level = "Easy"
        self.total_questions = int(APP_STATE.quiz_count)
        if self.total_questions < 5:
            self.total_questions = 5
        if self.total_questions > 15:
            self.total_questions = 15

        self.score = 0
        self.current_question = None
        self.current_index = 0
        self.answered = False
        self.lbl_score.setText("Skor: 0")
        self.lbl_progress.setText(f"Soal: {self.current_index}/{self.total_questions}")
        self.prompt.clear()
        self.feedback.clear()
        for rb in self.opt_buttons:
            rb.setChecked(False)
        self.btn_next.setText("Mulai Kuis")
        self._set_feedback_neutral()

    def _set_feedback_success(self):
        self.feedback.setStyleSheet("font-family: Consolas, monospace; font-size:14px; background:#E8F5E9; color:#1B5E20; border:2px solid #8FB996;")

    def _set_feedback_error(self):
        self.feedback.setStyleSheet("font-family: Consolas, monospace; font-size:14px; background:#FCEAEA; color:#B71C1C; border:2px solid #E57373;")

    def _set_feedback_neutral(self):
        self.feedback.setStyleSheet("font-family: Consolas, monospace; font-size:14px;")

    def _next_question(self):
        if self.btn_next.text() == "Selesai":
            self.reset()
            return
        if self.btn_next.text() == "Mulai Kuis":
            self.play_music()
        if self.current_index >= getattr(self, 'total_questions', 0):
            self.feedback.setText("Kuis selesai! Jawaban telah direset. Kamu bisa mulai lagi.")
            self._set_feedback_success()
            self.btn_next.setText("Selesai")
            return
        # Load a new random question using pre-selected level
        self.current_question = get_random_question(self.level)
        self.answered = False
        self.current_index += 1
        self.lbl_progress.setText(f"Soal: {self.current_index}/{self.total_questions}")
        self.prompt.setText(self.current_question['prompt'])
        for i, rb in enumerate(self.opt_buttons):
            rb.setText(self.current_question['options'][i])
            rb.setChecked(False)
        self.feedback.clear()
        self._set_feedback_neutral()
        self.btn_next.setText("Soal Berikutnya")

    def _submit(self):
        if not self.current_question:
            QMessageBox.information(self, "Info", "Tekan 'Mulai Kuis' terlebih dahulu.")
            return
        if self.answered:
            QMessageBox.information(self, "Info", "Sudah dinilai. Tekan 'Soal Berikutnya'.")
            return
        checked_id = self.options_group.checkedId()
        if checked_id < 0:
            QMessageBox.warning(self, "Peringatan", "Silakan pilih salah satu jawaban dulu.")
            return
        correct_idx = self.current_question['correct_index']
        if checked_id == correct_idx:
            self.score += self.current_question.get('score', 10)
            self.lbl_score.setText(f"Skor: {self.score}")
            self.feedback.setText("Benar! Kerja bagus! Teruskan, kamu hebat!\n\n" + self.current_question.get('explanation', ''))
            self._set_feedback_success()
        else:
            self.feedback.setText("Kurang tepat. Jangan menyerah, coba pelajari langkahnya berikut ini:\n\n" + self.current_question.get('explanation', ''))
            self._set_feedback_error()
        self.answered = True
        # show finish dialog
        if self.current_index >= self.total_questions:
            self.btn_next.setText("Selesai")
            m = QMessageBox(self)
            m.setWindowTitle("Selamat!")
            m.setText(f"Kuis selesai! Skor akhir: {self.score}")
            m.setInformativeText("Ingin coba lagi atau kembali ke Halaman Utama?")
            try_btn = m.addButton("Coba Lagi", QMessageBox.AcceptRole)
            home_btn = m.addButton("Ke Halaman Utama", QMessageBox.RejectRole)
            m.exec_()
            if m.clickedButton() == try_btn:
                # Reset 
                self.reset()
                self.stop_music()
                self.navigate("quiz_setup")
            else:
                # Back to welcome
                self.stop_music()
                self.navigate("welcome")
