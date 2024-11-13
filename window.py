import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtGui import QTextCharFormat, QFont, QColor, QSyntaxHighlighter
from PyQt5.QtCore import Qt, QRegExp

from main import run


class LispSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(Qt)
        self.keyword_patterns = [
            r'\bdefun\b', r'\bcar\b', r'\bcond\b',
            r'\bquote\b', r'\bcdr\b', r'\blist\b'
        ]
        self.keyword_regex = QRegExp('|'.join(self.keyword_patterns))
        self.keyword_format = keyword_format

        single_line_comment_format = QTextCharFormat()
        single_line_comment_format.setForeground(Qt.darkGreen)
        self.single_line_comment_regex = QRegExp(r';[^\n]*')
        self.single_line_comment_format = single_line_comment_format

        quotation_format = QTextCharFormat()
        quotation_format.setForeground(Qt.darkRed)
        self.quotation_regex = QRegExp(r'\'[^\']*')
        self.quotation_format = quotation_format

    def highlightBlock(self, text):
        self.setFormat(0, len(text), Qt.black)

        index = self.keyword_regex.indexIn(text)
        while index >= 0:
            length = self.keyword_regex.matchedLength()
            self.setFormat(index, length, self.keyword_format)
            index = self.keyword_regex.indexIn(text, index + length)

        index = self.single_line_comment_regex.indexIn(text)
        while index >= 0:
            length = self.single_line_comment_regex.matchedLength()
            self.setFormat(index, length, self.single_line_comment_format)
            index = self.single_line_comment_regex.indexIn(text, index + length)

        index = self.quotation_regex.indexIn(text)
        while index >= 0:
            length = self.quotation_regex.matchedLength()
            self.setFormat(index, length, self.quotation_format)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Lisp Editor with Compiler")
        self.setGeometry(100, 100, 800, 600)

        # Главный виджет
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Текстовый редактор
        self.textEdit = QTextEdit()
        self.highlighter = LispSyntaxHighlighter(self.textEdit.document())
        main_layout.addWidget(self.textEdit)

        # Кнопка компиляции
        compile_button = QPushButton('Compile')
        compile_button.clicked.connect(self.compile_code)
        main_layout.addWidget(compile_button)

        # Окно вывода
        self.outputLabel = QLabel("Output will be shown here...")
        self.outputLabel.setStyleSheet("QLabel { background-color : lightgrey; }")
        self.outputLabel.setAlignment(Qt.AlignTop)
        self.outputLabel.setWordWrap(True)
        main_layout.addWidget(self.outputLabel)

        # Настройка виджета и компоновки
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.show()

    def compile_code(self):
        # Получаем текст из редактора
        code = self.textEdit.toPlainText()
        print(code)
        print(run(code))

        # Пытаемся выполнить введённый Лисп-код (здесь вызывается интерпретатор)
        try:
            result = self.run_lisp_code(code)
            self.outputLabel.setText(f"Result: {result}")
        except Exception as e:
            self.outputLabel.setText(f"Error: {e}")

    def run_lisp_code(self, code):
        '''
        # Функция для компиляции/интерпретации Лисп-кода
        tokens = self.tokenize(code)
        ast = self.parse(tokens)
        env = self.standard_env()
        return self.eval_lisp(ast, env)'''
        return run(code)

    # Ниже простая реализация интерпретатора Лисп, которую можно расширять
    def tokenize(self, source):
        import re
        source = re.sub(r'([\(\)])', r' \1 ', source)
        return source.split()

    def parse(self, tokens):
        if len(tokens) == 0:
            raise SyntaxError("Unexpected EOF")
        
        token = tokens.pop(0)
        if token == '(':
            l = []
            while tokens[0] != ')':
                l.append(self.parse(tokens))
            tokens.pop(0)  # Убираем закрывающую скобку
            return l
        elif token == ')':
            raise SyntaxError("Unexpected )")
        else:
            return self.atom(token)

    def atom(self, token):
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except ValueError:
                return str(token)

    def eval_lisp(self, x, env):
        if isinstance(x, str):
            return env[x]
        elif isinstance(x, (int, float)):
            return x
        
        operator = x[0]
        args = x[1:]
        
        if operator == 'quote':
            return args[0]
        elif operator == 'if':
            test, consequent, alternative = args
            exp = (consequent if self.eval_lisp(test, env) else alternative)
            return self.eval_lisp(exp, env)
        elif operator == 'define':
            symbol, exp = args
            env[symbol] = self.eval_lisp(exp, env)
        elif operator == 'lambda':
            params, body = args
            return lambda *arguments: self.eval_lisp(body, dict(env, **dict(zip(params, arguments))))
        else:
            proc = self.eval_lisp(operator, env)
            values = [self.eval_lisp(arg, env) for arg in args]
            return proc(*values)

    def standard_env(self):
        import operator as op
        env = {
            '+': op.add,
            '-': op.sub,
            '*': op.mul,
            '/': op.truediv,
            '>': op.gt,
            '<': op.lt,
            '>=': op.ge,
            '<=': op.le,
            '=': op.eq,
            'abs': abs,
            'list': lambda *x: list(x),
            'list?': lambda x: isinstance(x, list),
            'null?': lambda x: x == [],
            'number?': lambda x: isinstance(x, (int, float)),
        }
        return env


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
