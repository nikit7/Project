import tkinter as tk
from tkinter import messagebox as mbox
from random import randint as ri


class Sapper:
    def __init__(self, master, rows, cols, mines):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.flags = 0
        self.game_over = False

        # Поле
        self.field = [[0 for _ in range(cols)] for _ in range(rows)]
        self.create_mines()
        self.calculate_mines()

        # GUI
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        self.create_buttons()

    # Создание мин
    def create_mines(self):
        mines_placed = 0
        while mines_placed < self.mines:
            row = ri(0, self.rows - 1)
            col = ri(0, self.cols - 1)
            if self.field[row][col] == 0:
                self.field[row][col] = -1
                mines_placed += 1

    # Подсчёт количества мин вокруг каждой клетки
    def calculate_mines(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.field[i][j] != -1:
                    cnt = 0
                    for x in range(max(0, i - 1), min(i + 2, self.rows)):
                        for y in range(max(0, j - 1), min(j + 2, self.cols)):
                            if self.field[x][y] == -1:
                                cnt += 1
                    self.field[i][j] = cnt

    # Создание кнопок
    def create_buttons(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.buttons[i][j] = tk.Button(self.master, width=2, command=lambda i=i, j=j: self.click(i, j))
                self.buttons[i][j].bind("<Button-3>", lambda event, i=i, j=j: self.flag(i, j))
                self.buttons[i][j].grid(row=i, column=j)

    # Обработка клика мыши
    def click(self, row, col):
        # Если игра окончена, или клетка уже открыта, или стоит флажок, то ничего не делаем
        if self.game_over or self.buttons[row][col]['state'] != 'normal' or self.buttons[row][col]['text'] == '🚩':
            return

        # Если найдена мина - проиграл
        if self.field[row][col] == -1:
            self.buttons[row][col].config(text='🧨', bg='#FF0000')
            self.game_over = True
            mbox.showinfo('Игра окончена', 'Вы проиграли!')
            self.restart_game()
        # Иначе открываем все соседние клетки с числовыми значениями или без
        else:
            self.dislose(row, col)

    # Открываем все соседние пустые клетки
    def dislose(self, row, col):
        line = [(row, col)]
        while line:
            row, col = line.pop(0)
            if self.field[row][col] != 0:
                self.buttons[row][col].config(text=str(self.field[row][col]), bg='#809BC7')
            else:
                self.buttons[row][col].config(text='', bg='#C1C1C1')
                for x in range(max(0, row - 1), min(row + 2, self.rows)):
                    for y in range(max(0, col - 1), min(col + 2, self.cols)):
                        if self.buttons[x][y]['state'] == 'normal':
                            line.append((x, y))
            self.buttons[row][col].config(state='disabled')

        if self.win():
            self.game_over = True
            mbox.showinfo('Игра окончена', 'Вы выиграли!')
            self.restart_game()

    # Установка флажка
    def flag(self, row, col):
        if self.buttons[row][col]['text'] == '' and self.buttons[row][col]['state'] == 'normal' and self.flags < 9:
            self.buttons[row][col].config(text='🚩', bg='#FFA200')
            self.flags += 1
        elif self.buttons[row][col]['text'] == '🚩':
            self.buttons[row][col].config(text='', bg='SystemButtonFace')
            self.flags -= 1
        else:
            mbox.showwarning('Внимание!', 'Можно установить только 9 флажков!')

    # Если все клетки без мин открыты - победа
    def win(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.field[i][j] != -1 and self.buttons[i][j]['state'] == 'normal':
                    return False
        return True

    # Перезапуск игры
    def restart_game(self):
        self.flags = 0
        self.game_over = False
        self.field = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.create_mines()
        self.calculate_mines()
        for i in range(self.rows):
            for j in range(self.cols):
                self.buttons[i][j].config(text='', state='normal', bg='SystemButtonFace')
