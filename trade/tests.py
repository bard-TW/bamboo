from django.test import TestCase


class AnimalTestCase(TestCase):
    def setUp(self):
        pass

    def test_animals_can_speak(self):
        self.assertEqual('aa', 'aa')

    def test_bb(self):
        # 需要以test_開頭
        self.assertEqual('aa', 'bb')


# 測試指令
# python manage.py test
