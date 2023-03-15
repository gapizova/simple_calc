""" Это учебный проект простого калькулятора. Операции: сложение, вычитание, умножение и деление.
Разработка GUI производилась в Qt Designer """

import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from design import Ui_MainWindow

import config

from operator import add, sub, mul, truediv


class SimpleCalc(QMainWindow):
    """ Главное окно калькулятора """
    def __init__(self):
        super(SimpleCalc, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.tmp_val = self.ui.lbl_temp
        self.entry_val = self.ui.le_entry
        self.entry_max_len = self.entry_val.maxLength()
        self.initUI()

    def initUI(self):
        # обработка нажатия на кнопки калькулятора
        self.ui.btn_0.clicked.connect(self.press_digit)
        self.ui.btn_1.clicked.connect(self.press_digit)
        self.ui.btn_2.clicked.connect(self.press_digit)
        self.ui.btn_3.clicked.connect(self.press_digit)
        self.ui.btn_4.clicked.connect(self.press_digit)
        self.ui.btn_5.clicked.connect(self.press_digit)
        self.ui.btn_6.clicked.connect(self.press_digit)
        self.ui.btn_7.clicked.connect(self.press_digit)
        self.ui.btn_8.clicked.connect(self.press_digit)
        self.ui.btn_9.clicked.connect(self.press_digit)
        self.ui.btn_clear.clicked.connect(self.press_clear)
        self.ui.btn_ce.clicked.connect(self.press_reset)
        self.ui.btn_point.clicked.connect(self.press_point)
        self.ui.btn_add.clicked.connect(self.math_operation)
        self.ui.btn_sub.clicked.connect(self.math_operation)
        self.ui.btn_mul.clicked.connect(self.math_operation)
        self.ui.btn_div.clicked.connect(self.math_operation)
        self.ui.btn_eq.clicked.connect(self.calculation)
        self.ui.btn_neg.clicked.connect(self.negate)
        self.ui.btn_backspace.clicked.connect(self.backspace)
        self.ui.le_entry.textChanged.connect(self.adjust_entry_font_size)

    def press_digit(self):
        """ Цифры от 0 до 9 """
        self.remove_error()
        self.clear_temp_if_equality()
        btn = self.sender()
        if self.entry_val.text() == '0':
            self.entry_val.setText(btn.text())
        else:
            self.entry_val.setText(self.entry_val.text() + btn.text())
        self.adjust_entry_font_size()

    def press_clear(self):
        """ Очистка поля ввода """
        self.remove_error()
        self.entry_val.setText('0')
        self.adjust_entry_font_size()
        self.tmp_val.clear()
        self.adjust_temp_font_size()

    def press_reset(self):
        """ Очистка поля ввода и поля вывода"""
        self.remove_error()
        self.clear_temp_if_equality()
        self.entry_val.setText('0')
        self.adjust_entry_font_size()

    def press_point(self):
        """ Кнопка точка """
        self.clear_temp_if_equality()
        if '.' not in self.entry_val.text():
            self.entry_val.setText(self.entry_val.text() + '.')
            self.adjust_entry_font_size()

    def avoid_deleting_char_on_negation(self, entry: str):
        """ Помогает избежать удаления символа при подстановке знака минус к числу"""
        if len(entry) == self.entry_max_len + 1 and '-' in entry:
            self.entry_val.setMaxLength(self.entry_max_len + 1)
        else:
            self.entry_val.setMaxLength(self.entry_max_len)

    def negate(self):
        """ Кнопка +/-"""
        self.clear_temp_if_equality()
        entry = self.entry_val.text()
        if '-' not in entry:
            if entry != '0':
                entry = '-' + entry
        else:
            entry = entry[1:]
        self.avoid_deleting_char_on_negation(entry)
        self.entry_val.setText(entry)
        self.adjust_entry_font_size()

    def backspace(self):
        """ Кнопка удалить символ"""
        self.remove_error()
        self.clear_temp_if_equality()
        entry = self.entry_val.text()
        if len(entry) != 1:
            if len(entry) == 2 and '-' in entry:
                self.entry_val.setText('0')
            else:
                self.entry_val.setText(entry[:-1])
        else:
            self.entry_val.setText('0')
        self.adjust_entry_font_size()

    def clear_temp_if_equality(self):
        """ Очистка поля вывода после окончания вычислений"""
        if self.get_operation_sign() == '=':
            self.tmp_val.clear()
            self.adjust_temp_font_size()

    def write_lbl_temp(self):
        """ Запись в поле вывода (используется как временная память для сохранения первого числа)"""
        press_btn = self.sender()
        format_entry = self.remove_zero(self.entry_val.text())
        if not self.tmp_val.text() or self.get_operation_sign() == '=':
            self.tmp_val.setText(format_entry + f' {press_btn.text()} ')
            self.adjust_temp_font_size()
            self.entry_val.setText('0')
            self.adjust_entry_font_size()

    @staticmethod
    def remove_zero(number: str):
        """ Удаление незначащих нулей после точки"""
        num = str(float(number))
        return num.replace('.0', '') if num.endswith('.0') else num

    def get_entry_value(self):
        """ Получение второго числа (из поля ввода)"""
        val = self.entry_val.text()
        return float(val) if '.' in val else int(val)

    def get_temp_val(self):
        """ Получение первого числа из поля вывода (временной памяти)"""
        if self.tmp_val.text():
            temp = self.tmp_val.text().split()[0]
            return float(temp) if '.' in temp else int(temp)

    def get_operation_sign(self):
        """ Получение знака математической операции"""
        if self.tmp_val.text():
            return self.tmp_val.text().strip('.').split()[-1]

    def get_entry_text_width(self):
        """ Ширина поля ввода"""
        return self.entry_val.fontMetrics().boundingRect(self.entry_val.text()).width()

    def get_temp_text_width(self):
        """ Ширина поля вывода"""
        return self.tmp_val.fontMetrics().boundingRect(self.tmp_val.text()).width()

    def calculation(self):
        """ Кнопка равно, непосредственное вычисление результата"""
        try:
            if self.get_operation_sign() == '+':
                result = add(self.get_temp_val(), self.get_entry_value())
            elif self.get_operation_sign() == '-':
                result = sub(self.get_temp_val(), self.get_entry_value())
            elif self.get_operation_sign() == '*':
                result = mul(self.get_temp_val(), self.get_entry_value())
            else:
                result = truediv(self.get_temp_val(), self.get_entry_value())
            self.tmp_val.setText(self.tmp_val.text() + str(self.entry_val) + ' =')
            self.adjust_temp_font_size()
            self.entry_val.setText(str(result))
            self.adjust_entry_font_size()
            self.clear_temp_if_equality()
            return str(result)
        except KeyError:
            pass
        except ZeroDivisionError:
            self.show_zero_division_error()

    def show_zero_division_error(self):
        """ Сообщение при ошибке деления на ноль"""
        if self.get_temp_val() == 0:
            self.show_error(config.ERROR_UNDEFINED)
        else:
            self.show_error(config.ERROR_ZERO_DIV)

    def math_operation(self):
        """ Запись во временную память математического знака операции"""
        btn_val = self.sender()
        if not self.tmp_val.text():
            self.write_lbl_temp()
        else:
            if self.get_operation_sign() != btn_val.text():
                if self.get_operation_sign() == '=':
                    self.write_lbl_temp()
                else:
                    self.replace_temp_sign()
            else:
                try:
                    self.tmp_val.setText(self.calculation() + f' {btn_val.text()} ')
                except TypeError:
                    pass
        self.adjust_temp_font_size()

    def replace_temp_sign(self):
        """ Замена знака математической операции в поле вывода"""
        btn = self.sender()
        self.tmp_val.sender(self.tmp_val.text()[:-2] + f' {btn.text()} ')

    def show_error(self, text: str):
        """ Подготовка поля к выводу сообщений об ошибке"""
        self.entry_val.setMaxLength(len(text))
        self.entry_val.setText(text)
        self.adjust_entry_font_size()
        self.disable_buttons(True)

    def remove_error(self):
        """ Восстановление поля вывода после сообщения об ошибке"""
        if self.entry_val.text() in (config.ERROR_UNDEFINED, config.ERROR_ZERO_DIV):
            self.entry_val.setMaxLength(self.entry_max_len)
            self.entry_val.setText('0')
            self.adjust_entry_font_size()
            self.disable_buttons(False)

    def disable_buttons(self, disable: bool):
        """ Блокировка кнопок при выводе ошибки"""
        for btn in config.BUTTON_TO_DISABLE:
            getattr(self.ui, btn).setDisabled(disable)
        color = 'color: #888;' if disable else 'color: white;'
        self.change_button_color(color)

    def change_button_color(self, css_color: str):
        """ Изменение цвета кнопок при блокировке"""
        for btn in config.BUTTON_TO_DISABLE:
            getattr(self.ui, btn).setStyleSheet(css_color)

    def adjust_entry_font_size(self):
        """ Размер шрифта в поле ввода подстраивается под размер поля"""
        font_size = config.DEFAULT_ENTRY_FONT_SIZE
        while self.get_entry_text_width() > self.entry_val.width() - 15:
            font_size -= 1
            self.entry_val.setStyleSheet(f'font-size: {font_size}pt; border: none;')
        font_size = 1
        while self.get_entry_text_width() < self.entry_val.width() - 60:
            font_size += 1
            if font_size > config.DEFAULT_ENTRY_FONT_SIZE:
                break
            self.entry_val.setStyleSheet(f'font-size: {font_size}pt; border: none')

    def adjust_temp_font_size(self):
        """ Размер шрифта в поле вывода подстраивается под размер поля"""
        font_size = config.DEFAULT_FONT_SIZE
        while self.get_temp_text_width() > self.tmp_val.width() - 10:
            font_size -= 1
            self.tmp_val.setStyleSheet(f'font-size: {font_size}pt; border: none;')
        font_size = 1
        while self.get_temp_text_width() < self.tmp_val.width() - 60:
            font_size += 1
            if font_size > config.DEFAULT_FONT_SIZE:
                break
            self.tmp_val.setStyleSheet(f'font-size: {font_size}pt; border: none')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimpleCalc()
    window.show()
    sys.exit(app.exec())
