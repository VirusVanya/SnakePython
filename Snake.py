from tkinter import *
import random

# Создаем глобальные переменные
# Ширина экрана
WIDTH = 800

# Высота экрана
HEIGHT = 600

# Размер сегмента змеи
SEG_SIZE = 20

# Переменная, отвечающая за состояние игры
IN_GAME = True


# Вспомогательная функция
def create_block1():
    """ Создаем еду для змейки """
    global BLOCK1
    posx = SEG_SIZE * random.randint(1, (WIDTH - SEG_SIZE) / SEG_SIZE)
    posy = SEG_SIZE * random.randint(1, (HEIGHT - SEG_SIZE) / SEG_SIZE)
    BLOCK1 = c.create_oval(posx, posy,
                          posx + SEG_SIZE, posy + SEG_SIZE,
                          fill="red")
def create_block2():
    """ Создаем еду для змейки """
    global BLOCK2
    posx = SEG_SIZE * random.randint(1, (WIDTH - SEG_SIZE) / SEG_SIZE)
    posy = SEG_SIZE * random.randint(1, (HEIGHT - SEG_SIZE) / SEG_SIZE)
    BLOCK2 = c.create_oval(posx, posy,
                          posx + SEG_SIZE, posy + SEG_SIZE,
                          fill="green")

# Подсчет очков
class Score(object):

    # функция отображения очков на экране
    def __init__(self):
        self.score = 0
        self.x = 55
        self.y = 15
        c.create_text(self.x, self.y, text="Score: {}".format(self.score), font="Arial 20",
                      fill="Yellow", tag="score", state='hidden')

    # функция счета очков и вывод на экран
    def increment(self):
        c.delete("score")
        self.score += 1
        c.create_text(self.x, self.y, text="Score: {}".format(self.score), font="Arial 20",
                      fill="Yellow", tag="score")
    
    def unincrement(self):
        c.delete("score")
        self.score -= 1
        c.create_text(self.x, self.y, text="Score: {}".format(self.score), font="Arial 20",
                      fill="Yellow", tag="score")

    # функция сброса очков при начале новой игры
    def reset(self):
        c.delete("score")
        self.score = 0

# Функция для управления игровым процессом
def main():
    """ Моделируем игровой процесс """
    global IN_GAME
    if IN_GAME:
        s.move()

        # Определяем координаты головы
        head_coords = c.coords(s.segments[-1].instance)
        x1, y1, x2, y2 = head_coords

        # столкновения с краями игрового поля
        if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
            IN_GAME = False

        # Поедание яблока
        elif head_coords == c.coords(BLOCK1):
            s.add_segment()
            c.delete(BLOCK1)
            create_block1()
        elif head_coords == c.coords(BLOCK2):
            s.remove_segment()
            c.delete(BLOCK2)
            create_block2()
        # Поедание змейки
        else:
            for index in range(len(s.segments) - 1):
                if head_coords == c.coords(s.segments[index].instance):
                    IN_GAME = False

        # скорость змейки
        root.after(200 - (3*len(s.segments)), main)
    # Не IN_GAME -> останавливаем игру и выводим сообщения
    else:
        set_state(restart_text, 'normal')
        set_state(game_over_text, 'normal')
        set_state(close_but, 'normal')

class Segment(object):
    """ Сегмент змейки """
    def __init__(self, x, y):
        self.instance = c.create_oval(x, y,
                                           x + SEG_SIZE, y + SEG_SIZE,
                                           fill="green",)       
class Snake(object):
    """ Класс змейки """
    def __init__(self, segments):
        self.segments = segments

        # Варианты движения
        self.mapping = {"Down": (0, 1), "Right": (1, 0), "Up": (0, -1), "Left": (-1, 0)}

        # инициируем направление движения
        self.vector = self.mapping["Right"]

    def move(self):
        """ Двигаем змейку в заданном направлении """
        for index in range(len(self.segments) - 1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = c.coords(self.segments[index + 1].instance)
            c.coords(segment, x1, y1, x2, y2)


        x1, y1, x2, y2 = c.coords(self.segments[-2].instance)
        c.coords(self.segments[-1].instance,
                 x1 + self.vector[0] * SEG_SIZE, y1 + self.vector[1] * SEG_SIZE,
                 x2 + self.vector[0] * SEG_SIZE, y2 + self.vector[1] * SEG_SIZE)

    def add_segment(self):
        """ Добавляем сегмент змейки """
        score.increment()
        last_seg = c.coords(self.segments[0].instance)
        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE
        self.segments.insert(0, Segment(x, y))
    
    def remove_segment(self):
        """ Добавляем сегмент змейки """
        if (len(self.segments) > 3):
            score.unincrement()
            last_seg = c.coords(self.segments[0].instance)
            c.delete(self.segments[0].instance)

    def change_direction(self, event):
        """ Изменение направления движения змейки """
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]

    # Функция обновления змейки при старте новой игры
    def reset_snake(self):
        for segment in self.segments:
            c.delete(segment.instance)

# функция для вывода сообщения
def set_state(item, state):
    c.itemconfigure(item, state=state)
    c.itemconfigure(BLOCK1, state='hidden')
    c.itemconfigure(BLOCK2, state='hidden')


# Функция для нажатия кнопки (новая игра)
def clicked(event):
    global IN_GAME
    s.reset_snake()
    IN_GAME = True
    c.delete(BLOCK1)
    c.delete(BLOCK2)
    score.reset()
    c.itemconfigure(restart_text, state='hidden')
    c.itemconfigure(game_over_text, state='hidden')
    c.itemconfigure(close_but, state='hidden')
    start_game()

# Функция для старта игры
def start_game():
    global s
    create_block1()
    create_block2()
    s = create_snake()

    # Реагируем на нажатие клавиш
    c.bind("<KeyPress>", s.change_direction)
    main()


# Создаем сегменты и змейку
def create_snake():
    segments = [Segment(SEG_SIZE, SEG_SIZE),
                Segment(SEG_SIZE * 2, SEG_SIZE),
                Segment(SEG_SIZE * 3, SEG_SIZE)]
    return Snake(segments)
    
# выход из игры
def close_win(root):
    exit()

# Настройка главного окна
root = Tk()
root.title("Змейка")

# Создаем экземпляр класса Canvas
c = Canvas(root, width=WIDTH, height=HEIGHT, bg="#000000")
c.grid()

# Захватываем фокус для отлавливания нажатий клавиш
c.focus_set()

# Текст результата игры
game_over_text = c.create_text(WIDTH / 2, HEIGHT / 2, text="Ты проиграл!",
                               font='Arial 20', fill='red',
                               state='hidden')
                               
# Текст начала новой игры после проигрыша
restart_text = c.create_text(WIDTH / 2, HEIGHT - HEIGHT / 3,
                             font='Arial 25',
                             fill='green',
                             activefill = 'Yellow',
                             text="Начать новую игру",
                             state='hidden')

# Текст выхода из программы после проигрыша
close_but = c.create_text(WIDTH / 2, HEIGHT - HEIGHT / 5, font='Arial 25',
                          fill='green',
                          activefill = 'Yellow',
                          text="Выход из игры",
                          state='hidden')

# Отработка событий при нажимания кнопок
c.tag_bind(restart_text, "<Button-1>", clicked)
c.tag_bind(close_but, "<Button-1>", close_win)

# Считаем очки
score = Score()

# Запускаем игру
start_game()

# запускаем окно
root.mainloop()