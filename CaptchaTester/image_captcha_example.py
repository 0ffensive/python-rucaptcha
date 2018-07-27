# v.1.6.6
import requests
import asyncio
import base64

from python_rucaptcha import ImageCaptcha
from python_rucaptcha import errors

"""
UPDATE 1.6.6
Добавлена возможность передачи изображения в формате base64
Добавление проверки на минимальное введённое время
Добавлен корректный перехват ошибки при невозможности чтения изображения из указанной папки - `errors.ReadError`
UPDATE 1.6.1
!!!ТОЛЬКО ДЛЯ СИНХРОННОГО МЕТОДА!!!
Добавлена возможность подключения к сайту, для получения изображения - через прокси.
Для этого нужно передать параметры, как и для бибилиотеки requests `.captcha_handler(......, 
                                                                                     proxies = {})`
!!!ТОЛЬКО ДЛЯ СИНХРОННОГО МЕТОДА!!!
Добавлена возможность скачивания изображений с незащищённых сайтов.
Для этого нужно передать параметры, как и для бибилиотеки requests `.captcha_handler(......, 
                                                                                     verify = False)`
"""


"""
Этот пример показывает то как нужно работать с модулем для распознования обычной капчи изображением,
на примере нашего сайта.
В общем случае вам потребуется получение:
1. Получить ссылку на изображение капчи(сртрока 15 в примере)
2. Передать эту ссылку в модуль ImageCaptcha(строка 20 в примере)
"""
# Введите ключ от рукапчи из своего аккаунта
RUCAPTCHA_KEY = 'aafb515dff0075f94b1f3328615bc0fd'
# Для получения ссылки на обычную капчу нужно послать GET запрос с соответствующим парметром
image_link = requests.get("http://85.255.8.26/api/",
                          params={"captcha_type": "get_common_captcha"}).json()["captcha_src"]

"""
Синхронный метод
"""

"""
Тут нужно воспользоваться бибилотекой, отослать на решение ссылку на капчу и получить ответ
далее его записать в user_answer
Первый пример демонстрирует сохранеие файла изображения как обычного файла в папу
"""
user_answer_const = ImageCaptcha.ImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY,
                                              save_format='const').captcha_handler(captcha_link=image_link)

"""
Второй пример демонстрирует сохранения файла как временного (temporary) - это стандартный вариант сохранения. 
Было выяснено, что он не работает с некоторыми видами капч - если возникают проблемы, то стоит использовать первый 
вариант
"""
user_answer_temp = ImageCaptcha.ImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY,
                                             save_format='temp').captcha_handler(captcha_link=image_link)

"""
Пример работы с передачей файла капчи уже закодированного в base64
"""
# закодировано: 976979
base_64_file = open('base64image.txt', 'rb')

user_answer_base64 = ImageCaptcha.ImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(captcha_base64=base_64_file)

"""
Пример работы с декодированием в base64 файла-капчи "налету"
"""
base_64_link = base64.b64encode(requests.get("http://85.255.8.26/static/image/common_image_example/862963.png").content).decode('utf-8')

user_answer_base64 = ImageCaptcha.ImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(captcha_base64=base_64_link)

'''
user_answer_... - это JSON строка с соответствующими полями
captchaSolve - решение капчи,
taskId - находится Id задачи на решение капчи,
errorId - 0 - если всё хорошо, 1 - если есть ошибка,
errorBody - тело ошибки, если есть.
{
    "captchaSolve": string,
    "taskId": int,
    "errorId": int, 1 or 0,
    "errorBody": string,
}
'''

if user_answer_const['errorId'] == 0:
    # решение капчи
    print(user_answer_const['captchaSolve'])
    print(user_answer_const['taskId'])
elif user_answer_const['errorId'] == 1:
    # Тело ошибки, если есть
    print(user_answer_const['errorBody'])

if user_answer_temp['errorId'] == 0:
    # решение капчи
    print(user_answer_temp['captchaSolve'])
    print(user_answer_temp['taskId'])
elif user_answer_temp['errorId'] == 1:
    # Тело ошибки, если есть
    print(user_answer_temp['errorBody'])

if user_answer_base64['errorId'] == 0:
    # решение капчи
    print(user_answer_base64['captchaSolve'])
    print(user_answer_base64['taskId'])
elif user_answer_base64['errorId'] == 1:
    # Тело ошибки, если есть
    print(user_answer_base64['errorBody'])

'''
Так же класс в качестве параметра может принимать список необязательных переменных, таких как:
phrase = 0, 
regsense = 0, 
numeric = 0, 
calc = 0, 
min_len = 0, 
max_len = 0, 
language = 0,
textinstructions = '', 
pingback = ''
и прочие.
Полный пример выглядит так:
'''
user_answer_full = ImageCaptcha.ImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY,
                                             save_format='temp',
                                             phrase=0,
                                             regsense=0,
                                             numeric=0,
                                             calc=0,
                                             min_len=0,
                                             max_len=0,
                                             language=0,
                                             textinstructions='',
                                             pingback='').captcha_handler(captcha_link=image_link,
                                                                          verify = False,
                                                                          proxies = {})

if user_answer_full['errorId'] == 0:
    # решение капчи
    print(user_answer_full['captchaSolve'])
    print(user_answer_full['taskId'])
elif user_answer_full['errorId'] == 1:
    # Тело ошибки, если есть
    print(user_answer_full['errorBody'])

"""
Пример для работы с локальными файлами
"""
# папка в которой находится изображение, один из вариантов написания
captcha_file = '088636.png'

# так же есть возможность передать так:
# captcha_file = r'D:\Python\933588.png'
# captcha_file = 'D:\/Python\/933588.png'
try:
    user_answer_local = ImageCaptcha.ImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY).captcha_handler(captcha_file=captcha_file)
    if user_answer_local['errorId'] == 0:
        # решение капчи
        print(user_answer_local['captchaSolve'])
        print(user_answer_local['taskId'])
    elif user_answer_local['errorId'] == 1:
        # Тело ошибки, если есть
        print(user_answer_local['errorBody'])

# отлов ошибки при проблемах чтения файла-изображения
except errors.ReadError as err:
    print(err)
"""
Асинхронный пример
Асинхронный способ поддерживает все параметры обычного метода
UPDATE 1.6.2
Добавлена поддержка прокси для асинхронного метода
!!!Поддерживаются только HTTP прокси!!!
Подробнее про него можно посмотреть тут:
https://docs.aiohttp.org/en/stable/client_advanced.html#proxy-support
"""


async def run():
    try:
        answer_aio_image = await ImageCaptcha.aioImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY) \
            .captcha_handler(captcha_link=image_link)
        if answer_aio_image['errorId'] == 0:
            # решение капчи
            print(answer_aio_image['captchaSolve'])
            print(answer_aio_image['taskId'])
        elif answer_aio_image['errorId'] == 1:
            # Тело ошибки, если есть
            print(answer_aio_image['errorBody'])
    except Exception as err:
        print(err)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run())
    loop.close()



"""
Пример для работы с локальными файлами
"""
# папка в которой находится изображение, один из вариантов написания
# captcha_file = r'D:\Python\933588.png'
# так же есть возможность передать так:
# captcha_file = 'D:\/Python\/933588.png'


# Асинхронный

async def run():
    try:
        answer_aio_local_image = await ImageCaptcha.aioImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY)\
            .captcha_handler(captcha_file=captcha_file)
        if answer_aio_local_image['errorId'] == 0:
            # решение капчи
            print(answer_aio_local_image['captchaSolve'])
            print(answer_aio_local_image['taskId'])
        elif answer_aio_local_image['errorId'] == 1:
            # Тело ошибки, если есть
            print(answer_aio_local_image['errorBody'])
    except Exception as err:
        print(err)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run)
    loop.close()

"""
UPDATE 1.6.2 с прокси
!!!Поддерживаются только HTTP прокси!!!
"""


async def run():
    try:
        answer_aio_image = await ImageCaptcha.aioImageCaptcha(rucaptcha_key=RUCAPTCHA_KEY)\
            .captcha_handler(captcha_link=image_link, proxy='http://85.21.83.186:8080')
        if answer_aio_image['errorId'] == 0:
            # решение капчи
            print(answer_aio_image['captchaSolve'])
            print(answer_aio_image['taskId'])
        elif answer_aio_image['errorId'] == 1:
            # Тело ошибки, если есть
            print(answer_aio_image['errorBody'])
    except Exception as err:
        print(err)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run())
    loop.close()