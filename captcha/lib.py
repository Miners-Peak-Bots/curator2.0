import random
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


class CaptchaEngine:
    def __init__(self):
        self.num1 = random.randint(1, 99)
        self.num2 = random.randint(1, 99)
        self.ans = self.num1 + self.num2
        self.choices = []

    def __create_choice(self):
        num1 = random.randint(1, 99)
        num2 = random.randint(1, 99)
        return num1 + num2

    def keyboard(self, captcha_id):
        for i in range(8):
            choice = self.__create_choice()
            while choice in self.choices:
                choice = self.__create_choice()

            button = InlineKeyboardButton(choice,
                                          callback_data=f'umt_{captcha_id}_{choice}')
            self.choices.append(button)

        ansbutton = InlineKeyboardButton(self.ans,
                                         callback_data=f'umt_{captcha_id}_{self.ans}')
        self.choices.append(ansbutton)
        random.shuffle(self.choices)
        self.choices = list(chunks(self.choices, 3))
        return InlineKeyboardMarkup(self.choices)

    def msg(self):
        return f'What is {self.num1} + {self.num2}'
