import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QLabel, QWidget, QMessageBox,
    QComboBox, QCheckBox, QHBoxLayout
)
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("8º BATALHÃO DE POLÍCIA DO EXÉRCITO - Cadastro")
        self.setGeometry(100, 100, 1000, 600)
        
        self.conn = sqlite3.connect("BraçalPE2024.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        self.layout = QVBoxLayout()

        self.title_label = QLabel("8º BATALHÃO DE POLÍCIA DO EXÉRCITO")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: green;")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.name_label = QLabel("Nome:")
        self.name_input = QLineEdit()
        self.idt_label = QLabel("IDT:")
        self.idt_input = QLineEdit()
        self.birth_label = QLabel("Data de Nascimento (AAAA-MM-DD):")
        self.birth_input = QLineEdit()
        self.cpf_label = QLabel("CPF:")
        self.cpf_input = QLineEdit()
        self.blood_label = QLabel("Tipo Sanguíneo:")
        self.blood_input = QLineEdit()

        self.cargo_label = QLabel("Cargo:")
        self.cargo_combo = QComboBox()
        self.cargo_combo.addItems(["SD", "SGT", "TEN"])

        self.ativa_checkbox = QCheckBox("Ativa")
        self.baixa_checkbox = QCheckBox("Baixa")

        self.armamento_label = QLabel("Armamento:")
        self.armamento_combo = QComboBox()
        self.armamento_combo.addItems([
            "Pistola 9mm", "Pistola .40", "Pistola .45", "Pistola PT 1911", "Pistola Glock 17", 
            "Pistola CZ 75", "Pistola Taurus PT 92", "Pistola Beretta 92", "Pistola SIG P226", 
            "PC"
        ])

        self.add_button = QPushButton("Adicionar Registro")
        self.add_button.clicked.connect(self.add_record)

        self.load_button = QPushButton("Carregar Registros")
        self.load_button.clicked.connect(self.load_records)

        self.filter_layout = QHBoxLayout()
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Filtrar por nome ou CPF")
        self.filter_button = QPushButton("Filtrar")
        self.filter_button.clicked.connect(self.filter_records)
        self.filter_layout.addWidget(self.filter_input)
        self.filter_layout.addWidget(self.filter_button)

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "Nome", "IDT", "Nascimento", "CPF", 
            "Tipo Sanguíneo", "Cargo", "Ativa", "Baixa", "Armamento"
        ])

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.idt_label)
        self.layout.addWidget(self.idt_input)
        self.layout.addWidget(self.birth_label)
        self.layout.addWidget(self.birth_input)
        self.layout.addWidget(self.cpf_label)
        self.layout.addWidget(self.cpf_input)
        self.layout.addWidget(self.blood_label)
        self.layout.addWidget(self.blood_input)
        self.layout.addWidget(self.cargo_label)
        self.layout.addWidget(self.cargo_combo)
        self.layout.addWidget(self.ativa_checkbox)
        self.layout.addWidget(self.baixa_checkbox)
        self.layout.addWidget(self.armamento_label)
        self.layout.addWidget(self.armamento_combo)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.load_button)
        self.layout.addLayout(self.filter_layout)
        self.layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.apply_theme()

    def create_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS pessoas")
        self.cursor.execute(
            """
            CREATE TABLE pessoas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                idt INTEGER NOT NULL,
                nascimento TEXT NOT NULL,
                cpf TEXT NOT NULL,
                tipo_sanguineo TEXT NOT NULL,
                cargo TEXT NOT NULL,
                ativa INTEGER NOT NULL,
                baixa INTEGER NOT NULL,
                armamento TEXT NOT NULL
            )
            """
        )
        self.conn.commit()

    def add_record(self):
        nome = self.name_input.text()
        idt = self.idt_input.text()
        nascimento = self.birth_input.text()
        cpf = self.cpf_input.text()
        tipo_sanguineo = self.blood_input.text()
        cargo = self.cargo_combo.currentText()
        ativa = 1 if self.ativa_checkbox.isChecked() else 0
        baixa = 1 if self.baixa_checkbox.isChecked() else 0
        armamento = self.armamento_combo.currentText()

        if nome and idt and nascimento and cpf and tipo_sanguineo and armamento:
            try:
                self.cursor.execute(
                    """
                    INSERT INTO pessoas (nome, idt, nascimento, cpf, tipo_sanguineo, cargo, ativa, baixa, armamento)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (nome, idt, nascimento, cpf, tipo_sanguineo, cargo, ativa, baixa, armamento)
                )
                self.conn.commit()
                QMessageBox.information(self, "Sucesso", "Registro adicionado com sucesso!")
                self.clear_inputs()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao adicionar: {e}")
        else:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos corretamente!")

    def load_records(self):
        self.cursor.execute("SELECT nome, idt, nascimento, cpf, tipo_sanguineo, cargo, ativa, baixa, armamento FROM pessoas")
        rows = self.cursor.fetchall()

        self.table.setRowCount(len(rows))
        for row_index, row_data in enumerate(rows):
            for col_index, col_data in enumerate(row_data):
                if col_index in (6, 7):
                    col_data = "Sim" if col_data == 1 else "Não"
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

    def filter_records(self):
        filter_text = self.filter_input.text()
        self.cursor.execute(
            """
            SELECT nome, idt, nascimento, cpf, tipo_sanguineo, cargo, ativa, baixa, armamento 
            FROM pessoas 
            WHERE nome LIKE ? OR cpf LIKE ?
            """,
            (f"%{filter_text}%", f"%{filter_text}%")
        )
        rows = self.cursor.fetchall()

        self.table.setRowCount(len(rows))
        for row_index, row_data in enumerate(rows):
            for col_index, col_data in enumerate(row_data):
                if col_index in (6, 7):
                    col_data = "Sim" if col_data == 1 else "Não"
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

    def clear_inputs(self):
        self.name_input.clear()
        self.idt_input.clear()
        self.birth_input.clear()
        self.cpf_input.clear()
        self.blood_input.clear()
        self.ativa_checkbox.setChecked(False)
        self.baixa_checkbox.setChecked(False)
        self.armamento_combo.setCurrentIndex(0)

    def apply_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: black;
                color: green;
                font-family: Consolas;
                font-size: 14px;
            }
            QLineEdit, QTableWidget {
                background-color: #222;
                color: green;
                border: 1px solid green;
            }
            QTableWidget::item {
                background-color: #111;
                color: green;
            }
            QPushButton {
                background-color: #333;
                color: green;
                border: 1px solid green;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #444;
            }
            QLabel {
                color: green;
            }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
