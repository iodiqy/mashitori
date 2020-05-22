import re

login_pattern = re.compile(r'^student_[0-9]+ \w+$', re.MULTILINE)


def repeat_all_messages(message):
    try:
        matches = re.match(login_pattern, message)
        print(message)
        # Вылавливаем ошибку, если вдруг юзер ввёл чушь
        # или задумался после ввода первого числа
    except AttributeError as ex:
        print("WRONG!")
        return


if __name__ == '__main__':
    repeat_all_messages(input())
