import os
import random
from pygame import *
from settings import *


def load_image(
        name,
        sx=-1,
        sy=-1,
        colorkey=None,
) -> pygame.Surface:
    """
    Загружает изображение из каталога 'resources'.

    Аргументы:
        name (str): Имя файла изображения для загрузки.
        sx (int, опционально): Желаемая ширина загруженного изображения. По умолчанию -1, что означает без изменения размера.
        sy (int, опционально): Желаемая высота загруженного изображения. По умолчанию -1, что означает без изменения размера.
        colorkey (Optional[Union[Tuple[int, int, int], int]], опционально): Если указано, устанавливает цветовой ключ изображения,
            чтобы обеспечить прозрачность. Если это целое число, оно интерпретируется как цвет, который должен стать прозрачным.
            Если это кортеж (r, g, b), этот цвет будет сделан прозрачным. По умолчанию None, что означает отсутствие прозрачности.

    Возвращает:
        pygame.Surface: Загруженное изображение в виде объекта pygame Surface.

    Примечание:
        Эта функция предполагает, что изображения находятся в каталоге 'resources' относительно местоположения скрипта.
        Если colorkey установлен в -1, функция автоматически определяет цветовой ключ из верхнего левого пикселя загруженного изображения.
        """
    fullname = os.path.join('resources', name)
    img = pygame.image.load(fullname)
    img = img.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = img.get_at((0, 0))
        img.set_colorkey(colorkey, RLEACCEL)
    # !RLEACCEL мнговенно делает прозрычным экран

    if sx != -1 or sy != -1:
        img = pygame.transform.scale(img, (sx, sy))

    return (img, img.get_rect())


def load_sprite_sheet(
        s_name,
        namex,
        namey,
        scx=-1,
        scy=-1,
        c_key=None,
):
    """
    Загружает спрайтовый лист изображения из каталога 'resources'.

    Аргументы:
        s_name (str): Имя файла спрайтового листа для загрузки.
        namex (int): Количество спрайтов по горизонтали.
        namey (int): Количество спрайтов по вертикали.
        scx (int, опционально): Желаемая ширина спрайта. По умолчанию -1, что означает без изменения размера.
        scy (int, опционально): Желаемая высота спрайта. По умолчанию -1, что означает без изменения размера.
        c_key (Optional[Union[Tuple[int, int, int], int]], опционально): Если указан, устанавливает цветовой ключ изображения,
            чтобы обеспечить прозрачность. Если это целое число, оно интерпретируется как цвет, который должен стать прозрачным.
            Если это кортеж (r, g, b), этот цвет будет сделан прозрачным. По умолчанию None, что означает отсутствие прозрачности.

    Возвращает:
        Tuple[List[pygame.Surface], pygame.Rect]: Список спрайтов в виде объектов pygame Surface и прямоугольник, охватывающий один из спрайтов.
    """
    fullname = os.path.join('resources', s_name)
    sh = pygame.image.load(fullname)
    sh = sh.convert()

    sh_rect = sh.get_rect()

    sprites = []

    sx = sh_rect.width / namex
    sy = sh_rect.height / namey

    for i in range(0, namey):
        for j in range(0, namex):
            rect = pygame.Rect((j * sx, i * sy, sx, sy))
            img = pygame.Surface(rect.size)
            img = img.convert()
            img.blit(sh, (0, 0), rect)

            if c_key is not None:
                if c_key == -1:
                    c_key = img.get_at((0, 0))
                img.set_colorkey(c_key, RLEACCEL)

            if scx != -1 or scy != -1:
                img = pygame.transform.scale(img, (scx, scy))

            sprites.append(img)

    sprite_rect = sprites[0].get_rect()

    return sprites, sprite_rect


# ! это функция принимает кол-во спрайтов и местоположение(по умолчанию -1.-1) можно сделать прозрачность

def gameover_display_message(rbtn_image, gmo_image):
    """
        Отображает сообщение о завершении игры на экране.

        Аргументы:
            rbtn_image (pygame.Surface): Изображение кнопки "Повторить".
            gmo_image (pygame.Surface): Изображение сообщения о завершении игры.

        Примечание:
            Изображение кнопки "Повторить" и сообщения о завершении игры должны быть предварительно загружены.

        """
    rbtn_rect = rbtn_image.get_rect()

    # &get_react() дает возможность изменять картинку
    rbtn_rect.centerx = width_screen / 2
    rbtn_rect.top = height_screen * 0.52

    gmo_rect = gmo_image.get_rect()
    gmo_rect.centerx = width_screen / 2
    gmo_rect.centery = height_screen * 0.35

    screen_layout_display.blit(rbtn_image, rbtn_rect)
    screen_layout_display.blit(gmo_image, gmo_rect)


# & blit build image

def extractDigits(num):
    """
       Извлекает цифры из числа и возвращает их в виде списка.

       Аргументы:
           num (int): Число, из которого необходимо извлечь цифры.

       Возвращает:
           List[int]: Список цифр, извлеченных из числа. Если число меньше 0, возвращает пустой список.

       Пример:
           extractDigits(12345) -> [1, 2, 3, 4, 5]
           extractDigits(7) -> [0, 0, 0, 0, 7]
       """
    if num > -1:
        d = []
        i = 0
        while (num / 10 != 0):
            d.append(num % 10)
            num = int(num / 10)

        d.append(num % 10)
        for i in range(len(d), 5):
            d.append(0)
        d.reverse()
        return d


class Dino():
    """
    Класс, представляющий персонажа динозавра в игре.

    Атрибуты:
        imgs (List[pygame.Surface]): Список изображений для анимации бега динозавра.
        rect (pygame.Rect): Прямоугольник, ограничивающий изображение динозавра.
        imgs1 (List[pygame.Surface]): Список изображений для анимации удара динозавра.
        rect1 (pygame.Rect): Прямоугольник, ограничивающий изображение динозавра при ударе.
        score (int): Текущий счет игрока.
        jumping (bool): Флаг, указывающий, выполняется ли прыжок.
        dead (bool): Флаг, указывающий, умер ли персонаж.
        ducking (bool): Флаг, указывающий, находится ли персонаж в положении "присесть".
        blinking (bool): Флаг, указывающий, мигает ли персонаж.
        movement (List[int]): Список с компонентами движения динозавра.
        jumpSpeed (float): Скорость прыжка динозавра.
        stand_position_width (int): Ширина прямоугольника при стоящем положении динозавра.
        duck_position_width (int): Ширина прямоугольника при положении "присесть" динозавра.
        index (int): Индекс текущего изображения в анимации.
        counter (int): Счетчик кадров для анимации и других событий.
    """
    def __init__(self, sx: int = -1, sy: int = -1):
        """
        Инициализация объекта динозавра.

        Аргументы:
            sx (int, опционально): Желаемая ширина спрайта динозавра. По умолчанию -1, что означает без изменения размера.
            sy (int, опционально): Желаемая высота спрайта динозавра. По умолчанию -1, что означает без изменения размера.
        """
        self.imgs, self.rect = load_sprite_sheet('dino.png', 5, 1, sx, sy, -1)
        self.imgs1, self.rect1 = load_sprite_sheet('dino_ducking.png', 2, 1, 59, sy, -1)
        self.rect.bottom = int(0.98 * height_screen)
        self.rect.left = width_screen / 15
        self.image = self.imgs[0]
        self.index = 0
        self.counter = 0
        self.score = 0
        self.jumping = False
        self.dead = False
        self.ducking = False
        self.blinking = False
        self.movement = [0, 0]
        self.jumpSpeed = 11.5

        self.stand_position_width = self.rect.width
        self.duck_position_width = self.rect1.width

    def draw(self):
        """Отображает изображение динозавра на экране."""
        screen_layout_display.blit(self.image, self.rect)

    def checkbounds(self):
        """Проверяет, находится ли динозавр в пределах экрана, и корректирует его положение при необходимости."""
        if self.rect.bottom > int(0.98 * height_screen):
            self.rect.bottom = int(0.98 * height_screen)
            self.jumping = False

    def update(self):
        """Обновляет состояние динозавра на основе текущего счетчика кадров."""
        if self.jumping:
            self.movement[1] = self.movement[1] + gravity

        if self.jumping:
            self.index = 0
        elif self.blinking:
            if self.index == 0:
                if self.counter % 400 == 399:
                    self.index = (self.index + 1) % 2
            else:
                if self.counter % 20 == 19:
                    self.index = (self.index + 1) % 2

        elif self.ducking:
            if self.counter % 5 == 0:
                self.index = (self.index + 1) % 2
        else:
            if self.counter % 5 == 0:
                self.index = (self.index + 1) % 2 + 2

        if self.dead:
            self.index = 4

        if not self.ducking:
            self.image = self.imgs[self.index]
            self.rect.width = self.stand_position_width
        else:
            self.image = self.imgs1[(self.index) % 2]
            self.rect.width = self.duck_position_width

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

        if not self.dead and self.counter % 7 == 6 and self.blinking == False:
            self.score += 1
            if self.score % 100 == 0 and self.score != 0:
                if pygame.mixer.get_init() != None:
                    checkPoint_sound.play()
        self.counter = (self.counter + 1)



class Cactus(pygame.sprite.Sprite):
    """
    Класс, представляющий кактус в игре.

    Атрибуты:
        speed (int): Скорость движения кактуса по горизонтали.
        imgs (List[pygame.Surface]): Список изображений для анимации движения кактуса.
        rect (pygame.Rect): Прямоугольник, ограничивающий изображение кактуса.
        movement (List[int]): Список с компонентами движения кактуса.
    """
    def __init__(self, speed: int = 5, sx: int = -1, sy: int = -1):
        """
        Инициализация объекта кактуса.

        Аргументы:
            speed (int, опционально): Скорость движения кактуса по горизонтали. По умолчанию 5.
            sx (int, опционально): Желаемая ширина спрайта кактуса. По умолчанию -1, что означает без изменения размера.
            sy (int, опционально): Желаемая высота спрайта кактуса. По умолчанию -1, что означает без изменения размера.
        """
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.imgs, self.rect = load_sprite_sheet('cactus-small.png', 3, 1, sx, sy, -1)
        self.rect.bottom = int(0.98 * height_screen)
        self.rect.left = width_screen + self.rect.width
        self.image = self.imgs[random.randrange(0, 3)]
        self.movement = [-1 * speed, 0]

    def draw(self):
        """Отображает изображение кактуса на экране."""
        screen_layout_display.blit(self.image, self.rect)

    def update(self):
        """Обновляет состояние кактуса."""
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:
            self.kill()


class birds(pygame.sprite.Sprite):
    """
    Класс, представляющий птицу в игре.

    Атрибуты:
        speed (int): Скорость движения птицы по горизонтали.
        imgs (List[pygame.Surface]): Список изображений для анимации движения птицы.
        rect (pygame.Rect): Прямоугольник, ограничивающий изображение птицы.
        birds_height (List[int]): Список возможных высот, на которых может появиться птица.
        index (int): Индекс текущего изображения в анимации.
        counter (int): Счетчик кадров для анимации.
        movement (List[int]): Список с компонентами движения птицы.
    """
    def __init__(self, speed: int = 5, sx: int = -1, sy: int = -1):
        """
        Инициализация объекта птицы.

        Аргументы:
            speed (int, опционально): Скорость движения птицы по горизонтали. По умолчанию 5.
            sx (int, опционально): Желаемая ширина спрайта птицы. По умолчанию -1, что означает без изменения размера.
            sy (int, опционально): Желаемая высота спрайта птицы. По умолчанию -1, что означает без изменения размера.
        """
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.imgs, self.rect = load_sprite_sheet('birds.png', 2, 1, sx, sy, -1)
        self.birds_height = [height_screen * 0.82, height_screen * 0.75, height_screen * 0.60]
        self.rect.centery = self.birds_height[random.randrange(0, 3)]
        self.rect.left = width_screen + self.rect.width
        self.image = self.imgs[0]
        self.movement = [-1 * speed, 0]
        self.index = 0
        self.counter = 0

    def draw(self):
        """Отображает изображение птицы на экране."""
        screen_layout_display.blit(self.image, self.rect)

    def update(self):
        """Обновляет состояние птицы."""
        if self.counter % 10 == 0:
            self.index = (self.index + 1) % 2
        self.image = self.imgs[self.index]
        self.rect = self.rect.move(self.movement)
        self.counter = (self.counter + 1)
        if self.rect.right < 0:
            self.kill()


class Ground():
    """
    Класс, представляющий землю в игре.

    Атрибуты:
        speed (int): Скорость движения земли по горизонтали.
        image (pygame.Surface): Изображение земли для первого блока.
        rect (pygame.Rect): Прямоугольник, ограничивающий первый блок изображения земли.
        image1 (pygame.Surface): Изображение земли для второго блока.
        rect1 (pygame.Rect): Прямоугольник, ограничивающий второй блок изображения земли.
    """
    def __init__(self, speed: int = -5):
        """
        Инициализация объекта земли.

        Аргументы:
            speed (int, опционально): Скорость движения земли по горизонтали. По умолчанию -5.
        """
        self.image, self.rect = load_image('ground.png', -1, -1, -1)
        self.image1, self.rect1 = load_image('ground.png', -1, -1, -1)
        self.rect.bottom = height_screen
        self.rect1.bottom = height_screen
        self.rect1.left = self.rect.right
        self.speed = speed

    def draw(self):
        """Отображает изображения земли на экране."""
        screen_layout_display.blit(self.image, self.rect)
        screen_layout_display.blit(self.image1, self.rect1)

    def update(self):
        """Обновляет состояние земли."""
        self.rect.left += self.speed
        self.rect1.left += self.speed

        if self.rect.right < 0:
            self.rect.left = self.rect1.right

        if self.rect1.right < 0:
            self.rect1.left = self.rect.right

class Cloud(pygame.sprite.Sprite):
    """
    Класс, представляющий облако в игре.

    Атрибуты:
        speed (int): Скорость движения облака по горизонтали.
        image (pygame.Surface): Изображение облака.
        rect (pygame.Rect): Прямоугольник, ограничивающий изображение облака.
        movement (List[int]): Список с компонентами движения облака.
    """
    def __init__(self, x: int, y: int):
        """
        Инициализация объекта облака.

        Аргументы:
            x (int): Координата X для размещения облака на экране.
            y (int): Координата Y для размещения облака на экране.
        """
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = load_image('cloud.png', int(90 * 30 / 42), 30, -1)
        self.speed = 1
        self.rect.left = x
        self.rect.top = y
        self.movement = [-1 * self.speed, 0]

    def draw(self):
        """Отображает изображение облака на экране."""
        screen_layout_display.blit(self.image, self.rect)

    def update(self):
        """Обновляет состояние облака."""
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0:
            self.kill()


class Scoreboard():
    """
    Класс, представляющий табло счета игрока.

    Атрибуты:
        score (int): Текущий счет игрока.
        scre_img (List[pygame.Surface]): Список изображений для отображения цифр счета.
        screrect (pygame.Rect): Прямоугольник, ограничивающий одну изображение цифры счета.
        image (pygame.Surface): Поверхность для отображения табло счета.
        rect (pygame.Rect): Прямоугольник, ограничивающий изображение табло счета.
    """
    def __init__(self, x: int = -1, y: int = -1):
        """
        Инициализация объекта табло счета.

        Аргументы:
            x (int, опционально): Координата X для размещения табло счета на экране. По умолчанию -1.
            y (int, опционально): Координата Y для размещения табло счета на экране. По умолчанию -1.
        """
        self.score = 0
        self.scre_img, self.screrect = load_sprite_sheet('numbers.png', 12, 1, 11, int(11 * 6 / 5), -1)
        self.image = pygame.Surface((55, int(11 * 6 / 5)))
        self.rect = self.image.get_rect()
        if x == -1:
            self.rect.left = width_screen * 0.89
        else:
            self.rect.left = x
        if y == -1:
            self.rect.top = height_screen * 0.1
        else:
            self.rect.top = y

    def draw(self):
        """Отображает табло счета на экране."""
        screen_layout_display.blit(self.image, self.rect)

    def update(self, score: int):
        """
        Обновляет табло счета.

        Аргументы:
            score (int): Новое значение счета игрока.
        """
        score_digits = extractDigits(score)
        self.image.fill(bg_color)
        for s in score_digits:
            self.image.blit(self.scre_img[s], self.screrect)
            self.screrect.left += self.screrect.width
        self.screrect.left = 0
