import unittest
from unittest.mock import Mock, patch
from objects import Dino
from settings import *
from objects import Cactus
from objects import birds
from objects import Cloud
from objects import Ground
from objects import Scoreboard

class TestDino(unittest.TestCase):
    """
    Класс для тестирования функционала класса Dino.
    """

    def setUp(self):
        """
        Настройка тестовых данных перед выполнением каждого теста.
        """
        # Инициализация экземпляра класса Dino для тестирования
        self.dino = Dino()

    def test_initialization(self):
        """
        Проверка правильной инициализации объекта Dino.
        """
        # Проверяем, что объект правильно инициализирован
        self.assertEqual(self.dino.rect.bottom, int(0.98 * height_screen))
        self.assertEqual(self.dino.rect.left, width_screen / 15)
        self.assertEqual(self.dino.image, self.dino.imgs[0])
        self.assertEqual(self.dino.index, 0)
        self.assertEqual(self.dino.counter, 0)
        self.assertEqual(self.dino.score, 0)
        self.assertFalse(self.dino.jumping)
        self.assertFalse(self.dino.dead)
        self.assertFalse(self.dino.ducking)
        self.assertFalse(self.dino.blinking)
        self.assertEqual(self.dino.movement, [0, 0])
        self.assertEqual(self.dino.jumpSpeed, 11.5)
        self.assertEqual(self.dino.stand_position_width, self.dino.rect.width)
        self.assertEqual(self.dino.duck_position_width, self.dino.rect1.width)

    def test_checkbounds(self):
        """
        Проверка метода checkbounds().
        """
        # Проверяем метод checkbounds()
        # Предположим, что экран имеет высоту 600
        self.dino.rect.bottom = 650
        self.dino.jumping = True
        self.dino.checkbounds()
        self.assertFalse(
            self.dino.jumping)  # Проверяем, что прыжок завершился, когда динозавр достиг нижней границы экрана

    @patch('pygame.mixer.get_init', return_value=True)
    def test_update_score_increment(self, mock_get_init):
        # Проверяем, что метод update() увеличивает счет, когда динозавр не мертв и не приседает
        initial_score = self.dino.score
        self.dino.update()
        self.assertEqual(self.dino.score, initial_score + 1)

    @patch('pygame.mixer.get_init', return_value=True)
    def test_update_score_checkpoint_sound(self, mock_get_init):
        # Проверяем, что метод update() воспроизводит звук контрольной точки при достижении определенного счета
        self.dino.score = 99
        self.dino.update()  # Увеличиваем счет до 100
        # Проверяем, что воспроизводится звук контрольной точки
        self.assertTrue(checkPoint_sound.play.called)


class TestCactus(unittest.TestCase):
    """
    Класс для тестирования функционала класса Cactus.
    """

    def test_initialization(self):
        """
        Проверка правильной инициализации объекта Cactus.
        """
        speed = 5
        cactus = Cactus(speed)
        self.assertEqual(cactus.rect.bottom, int(0.98 * height_screen))
        self.assertEqual(cactus.rect.left, width_screen + cactus.rect.width)
        self.assertIn(cactus.image, cactus.imgs)

    def test_update_movement(self):
        """
        Проверка обновления позиции объекта Cactus.
        """
        speed = 5
        cactus = Cactus(speed)
        initial_rect_left = cactus.rect.left
        cactus.update()
        self.assertEqual(cactus.rect.left, initial_rect_left + cactus.movement[0])

    def test_kill_when_off_screen(self):
        """
        Проверка удаления объекта Cactus, когда он уходит за экран.
        """
        speed = 5
        cactus = Cactus(speed)
        cactus.rect.right = -1
        cactus.kill = Mock()
        cactus.update()
        cactus.kill.assert_called_once()


class TestBirds(unittest.TestCase):
    """
    Класс для тестирования функционала класса birds.
    """

    def test_initialization(self):
        """
        Проверка правильной инициализации объекта birds.
        """
        speed = 5
        bird = birds(speed)
        self.assertIn(bird.image, bird.imgs)
        self.assertTrue(bird.rect.centery in bird.birds_height)
        self.assertEqual(bird.rect.left, width_screen + bird.rect.width)

    def test_update_movement(self):
        """
        Проверка обновления позиции объекта birds.
        """
        speed = 5
        bird = birds(speed)
        initial_rect_left = bird.rect.left
        bird.update()
        self.assertEqual(bird.rect.left, initial_rect_left + bird.movement[0])

    def test_kill_when_off_screen(self):
        """
        Проверка удаления объекта birds, когда он уходит за экран.
        """
        speed = 5
        bird = birds(speed)
        bird.rect.right = -1
        bird.kill = Mock()
        bird.update()
        bird.kill.assert_called_once()


class TestGround(unittest.TestCase):
    """
    Класс для тестирования функционала класса Ground.
    """

    def test_initialization(self):
        """
        Проверка правильной инициализации объекта Ground.
        """
        speed = -5
        ground = Ground(speed)
        self.assertEqual(ground.rect.bottom, height_screen)
        self.assertEqual(ground.rect1.bottom, height_screen)
        self.assertEqual(ground.rect1.left, ground.rect.right)
        self.assertEqual(ground.speed, speed)

    def test_update_movement(self):
        """
        Проверка обновления позиции объекта Ground.
        """
        speed = -5
        ground = Ground(speed)
        initial_rect_left = ground.rect.left
        initial_rect1_left = ground.rect1.left
        ground.update()
        self.assertEqual(ground.rect.left, initial_rect_left + speed)
        self.assertEqual(ground.rect1.left, initial_rect1_left + speed)

    def test_wraparound(self):
        """
        Проверка переноса объекта Ground за экран, когда он уходит за его пределы.
        """
        speed = -5
        ground = Ground(speed)
        ground.rect.right = -1
        ground.rect1.right = -1
        ground.update()
        self.assertTrue(ground.rect.left == ground.rect1.right or ground.rect1.left == ground.rect.right)


class TestCloud(unittest.TestCase):
    """
    Класс для тестирования функционала класса Cloud.
    """

    def test_initialization(self):
        """
        Проверка правильной инициализации объекта Cloud.
        """
        x = 100
        y = 200
        cloud = Cloud(x, y)
        self.assertEqual(cloud.rect.left, x)
        self.assertEqual(cloud.rect.top, y)
        self.assertEqual(cloud.speed, 1)

    def test_update_movement(self):
        """
        Проверка обновления позиции объекта Cloud.
        """
        cloud = Cloud(100, 200)
        initial_rect_left = cloud.rect.left
        cloud.update()
        self.assertEqual(cloud.rect.left, initial_rect_left - cloud.speed)

    @patch.object(Cloud, 'kill')
    def test_kill_when_off_screen(self, mock_kill):
        """
        Проверка удаления объекта Cloud, когда он уходит за экран.
        """
        cloud = Cloud(0, 200)
        cloud.rect.right = -1
        cloud.update()
        mock_kill.assert_called_once()


class TestScoreboard(unittest.TestCase):
    """
    Класс для тестирования функционала класса Scoreboard.
    """

    def test_initialization_default_position(self):
        """
        Проверка правильной инициализации объекта Scoreboard со значениями по умолчанию.
        """
        scoreboard = Scoreboard()
        self.assertEqual(scoreboard.rect.left, width_screen * 0.89)
        self.assertEqual(scoreboard.rect.top, height_screen * 0.1)

    def test_initialization_custom_position(self):
        """
        Проверка правильной инициализации объекта Scoreboard с пользовательскими координатами.
        """
        x = 100
        y = 200
        scoreboard = Scoreboard(x, y)
        self.assertEqual(scoreboard.rect.left, x)
        self.assertEqual(scoreboard.rect.top, y)

    @patch('pygame.Surface')
    def test_update(self, mock_surface):
        """
        Проверка обновления счета на доске.
        """
        scoreboard = Scoreboard()
        mock_surface.get_rect.return_value = mock_rect = Mock()
        mock_rect.width = 10
        mock_rect.left = 0

        score = 12345
        scoreboard.update(score)

        self.assertEqual(scoreboard.score, score)
        mock_surface.fill.assert_called_once_with(bg_color)
        self.assertEqual(mock_rect.left, 0)



if __name__ == '__main__':
    unittest.main()
