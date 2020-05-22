import requests
from bs4 import BeautifulSoup as BS


# print("login:")
# login = input()
# print("\npassword:")
# password = input()


def get_string_of_points(login, password):
    s = requests.Session()

    auth_html = s.get('https://sirius.kaznmu.kz/')
    auth_html = BS(auth_html.content, 'html.parser')

    payload = {
        'returnUrl': '/',
        # 'LoginForm[username]': 'student_56169',
        # 'LoginForm[password]': 'ABSS2gp',
        'LoginForm[username]': login,
        'LoginForm[password]': password,
        'LoginForm[rememberMe]': 1
    }

    s.post('https://sirius.kaznmu.kz/sirius/index.php?r=user/auth/login/', data=payload)

    ass = s.get('https://sirius.kaznmu.kz/student/index.php?r=gradebook/main/')
    ass_bs = BS(ass.content, 'html.parser')
    s1 = ''
    i = 0
    for info in ass_bs.find_all('td'):
        if i > 100:
            break
        if i > 3:
            s1 = s1 + info.text + "\n"
        i = i + 1
    return s1
