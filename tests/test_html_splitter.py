from chatgpt_md_converter.html_splitter import split_html_for_telegram

example_text = """
Конечно! Вот то же самое длинное сообщение в Markdown:

---

<b>Введение в асинхронное программирование в Python</b>

<b>Содержание</b>

1. <a href="#что-такое-асинхронность">Что такое асинхронность?</a>
2. <a href="#проблемы-синхронного-исполнения">Проблемы синхронного исполнения</a>
3. <a href="#асинхронное-программирование-концепции">Асинхронное программирование: концепции</a>
4. <a href="#модуль-asyncio">Модуль asyncio</a>
5. <a href="#ключевые-слова-async-и-await">Ключевые слова: async и await</a>
6. <a href="#асинхронные-функции-и-корутины">Асинхронные функции и корутины</a>
7. <a href="#пример-простейший-асинхронный-код">Пример — простейший асинхронный код</a>
8. <a href="#асинхронные-задачи-и-их-исполнение">Асинхронные задачи и их исполнение</a>
9. <a href="#работа-с-сетью-асинхронные-http-запросы">Работа с сетью: асинхронные HTTP-запросы</a>
10. <a href="#асинхронная-работа-с-файлами">Асинхронная работа с файлами</a>
11. <a href="#асинхронная-работа-с-базами-данных">Асинхронная работа с базами данных</a>
12. <a href="#типичные-ошибки-новичков">Типичные ошибки новичков</a>
13. <a href="#плюсы-и-минусы-асинхронности">Плюсы и минусы асинхронности</a>
14. <a href="#мини-faq">Мини-FAQ</a>

---

<b>Что такое асинхронность?</b>

Асинхронность — это способ организации выполнения кода, при котором операции, ожидающие завершения (например, ввод-вывод — I/O), не блокируют исполнение всей программы, а дают возможность выполнять другие задачи, пока основная операция не завершилась.

Это кардинально отличается от синхронного подхода, при котором все операции выполняются строго последовательно.

---

<b>Проблемы синхронного исполнения</b>

Синхронная программа может "замереть" в ожидании:

• Данных из сети
• Ответа от базы данных
• Входных данных от пользователя
• Завершения записи на диск

<b>Пример синхронного кода</b>:
<pre><code class="language-python">import time

def download_data():
    print("Запуск скачивания данных...")
    time.sleep(5)  # Имитируем задержку — например, скачивание файла
    print("Данные скачаны!")

download_data()
print("Обработка данных...")
</code></pre>
Пока идет <code>time.sleep(5)</code>, другой код не может исполниться! Если у нас есть много таких операций — программа начинает "тормозить".

---

<b>Асинхронное программирование: концепции</b>

Асинхронное программирование строится вокруг событийного цикла (event loop) и позволяет:

• Ожидать завершения задач, не блокируя главный поток исполнения
• Использовать неблокирующие функции и библиотеки
• Оптимально расходовать вычислительные ресурсы

Это особенно полезно для программ, работающих с большим количеством сетевых соединений, совершения HTTP-запросов, выполнения операций чтения/записи и пр.

---

<b>Модуль asyncio</b>

<code>asyncio</code> — стандартный модуль в Python (версии 3.4+), реализующий инструменты асинхронного исполнения.

<b>Кратко о главном</b>

• <b>Event Loop</b> — событийный цикл, в котором запускаются все задачи
• <b>Coroutine</b> — функция, которую можно приостановить и возобновить (ключевое слово <code>async</code>)
• <b>Task</b> — обёртка над корутиной, которая ставит её в очередь на исполнение
• <b>Future</b> — результат работы асинхронной операции (пока не завершилась — pending)

---

<b>Ключевые слова: async и await</b>

• <code>async</code> перед определением функции = функция становится асинхронной (корутиной)
• <code>await</code> внутри асинхронной функции — "дождаться результата выполнения" другой корутины

<b>Пример:</b>
<pre><code class="language-python">import asyncio

async def sleep_and_print():
    print("Ждем 2 секунды...")
    await asyncio.sleep(2)
    print("Готово!")

asyncio.run(sleep_and_print())
</code></pre>

---

<b>Асинхронные функции и корутины</b>

Асинхронная функция объявляется с помощью <code>async def</code>, а вызывается через <code>await</code> <b>только внутри другой асинхронной функции</b>.

<b>Важно:</b>  
• Функция с <code>async def</code> ничего НЕ будет исполнять до тех пор, пока "не будет запущена в event loop".
• Обычная main-функция НЕ может использовать <code>await</code> — только асинхронная!

---

<b>Пример — простейший асинхронный код</b>

<pre><code class="language-python">import asyncio

async def greet(name):
    print(f"Привет, {name}! Жду 1 секунду...")
    await asyncio.sleep(1)
    print(f"{name}, добро пожаловать!")

async def main():
    await greet("Пользователь")

asyncio.run(main())
</code></pre>

<b>Асинхронные задачи и их исполнение</b>

Можно запускать сразу несколько задач через <code>asyncio.create_task()</code>, чтобы они работали ПАРАЛЛЕЛЬНО (но всё равно в одном потоке).

<pre><code class="language-python">async def worker(number):
    print(f"Задача {number} стартовала")
    await asyncio.sleep(3)
    print(f"Задача {number} завершилась")

async def main():
    tasks = []
    for i in range(5):
        task = asyncio.create_task(worker(i))
        tasks.append(task)
    await asyncio.gather(*tasks)

asyncio.run(main())
</code></pre>
Этот код запустит 5 задач, и они выполнятся за 3 секунды, а не за 15!

---

<b>Работа с сетью: асинхронные HTTP-запросы</b>

Стандартная библиотека <code>asyncio</code>0 — синхронная. Специально для асинхронных задач используют, например, <b>aiohttp</b>.

<pre><code class="language-python">import aiohttp
import asyncio

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    urls = [
        "https://www.python.org",
        "https://www.asyncio.org"
    ]
    tasks = [fetch(url) for url in urls]
    results = await asyncio.gather(*tasks)
    for i, result in enumerate(results):
        print(f"Ответ с {urls[i]}: {len(result)} символов")

asyncio.run(main())
</code></pre>
---

<b>Асинхронная работа с файлами</b>

Встроенный <code>asyncio</code>1 — синхронный.  
Для асинхронного чтения используйте <b>aiofiles</b>:

<pre><code class="language-python">import aiofiles
import asyncio

async def read_my_file():
    async with aiofiles.open("somefile.txt", mode="r") as f:
        contents = await f.read()
        print(contents)

asyncio.run(read_my_file())
</code></pre>

---

<b>Асинхронная работа с базами данных</b>

Многие библиотеки поддерживают асинхронное взаимодействие с БД:  
• <b>Databases</b> (asynchronous database framework)
• <b>Tortoise ORM</b> (async ORM)
• <b>SQLAlchemy 1.4+</b> — поддержка асинхронности

<b>Пример на Databases:</b>
<pre><code class="language-python">import databases
import sqlalchemy
import asyncio

DATABASE_URL = "sqlite+aiosqlite:///test.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
)

async def main():
    await database.connect()
    query = notes.insert().values(text="Асинхронная запись!")
    await database.execute(query)
    await database.disconnect()

asyncio.run(main())
</code></pre>

---

<b>Типичные ошибки новичков</b>

1. <b>Попытка использовать await вне async-функции</b>
   <pre><code class="language-python">   await asyncio.sleep(2)   # Ошибка!
   </code></pre>

2. <b>Перезапуск event loop внутри уже работающего loop</b>
   <pre><code class="language-python">   asyncio.run(main())  # Нельзя вызывать внутри уже запущенного event loop
   </code></pre>

3. <b>Забыли добавить await</b>
   <pre><code class="language-python">   async def main():
       asyncio.sleep(2)  # Забыли await! Код не приостановится и не выполнится как надо
   </code></pre>

4. <b>Использование синхронных библиотек (например, requests) в async-коде</b>  
   Это приводит к блокировке event loop

---

<b>Плюсы и минусы асинхронности</b>

| Плюсы                         | Минусы                                       |
|-------------------------------|----------------------------------------------|
| + Много одновременных задач   | – Новый синтаксис, нужно переучиваться       |
| + Не тратятся idle-ресурсы    | – Не все сторонние библиотеки поддерживают   |
| + Высокая производительность  | – Дебаг и трейсбэки иногда сложнее          |
| + Удобно для сетевого I/O     | – Не ускоряет чисто вычислительные задачи    |

---

<b>Мини-FAQ</b>

<b><b>Вопрос:</b> Что лучше — <code>asyncio</code>2 или threading / multiprocessing?</b>

<b>Ответ:</b>  
Асинхронность — для больших I/O задач без необходимости запускать новую OS thread.  
Threading — когда нужно много небольших потоков (например, для GUI, небольших фоновых задач).  
Multiprocessing — для тяжёлых вычислений, которые нужно реально распараллелить по ядрам.

---

<b><b>Вопрос:</b> Можно ли смешивать синхронный и асинхронный код?</b>

<b>Ответ:</b>  
Можно, но аккуратно (и часто через launch/future/threadpool).

---

<b><b>Вопрос:</b> Нужно ли везде использовать асинхронность?</b>

<b>Ответ:</b>  
Нет. Если твоя программа делает много работы исключительно с CPU (<code>asyncio</code>3), асинхронность не даст прироста.  
Асинхронность полезна для большого числа сетевых и файловых операций.

---

<b><b>Вопрос:</b> Зачем нужны корутины, tasks и event loop?</b>

<b>Ответ:</b>  
• <b>Корутины</b> — функции, выполнение которых можно "приостанавливать" и "дожидаться" исполнения других корутин без блокировки event loop.
• <b>Tasks</b> — обёртки вокруг корутин, которые можно запустить параллельно.
• <b>Event Loop</b> — цикл, который управляет исполнением задач.

---

<b><b>Вопрос:</b> Как сделать паузу внутри асинхронного кода?</b>

<b>Ответ:</b>  
Вместо <code>asyncio</code>4 используйте:

<pre><code class="language-python">await asyncio.sleep(3)
</code></pre>

---

<b><b>Вопрос:</b> Как запустить асинхронный код из обычной функции?</b>

<b>Ответ:</b>  
Используйте <code>asyncio</code>5.

---

<b><b>Вопрос:</b> Какие есть реальные фреймворки для асинхронности в вебе?</b>

<b>Ответ:</b>  
• FastAPI (asgi, асинхронный)
• Starlette
• Sanic
• AIOHTTP

---

<b><b>Вопрос:</b> Где читать дальше?</b>

• https://docs.python.org/3/library/asyncio.html — официальная документация
• https://realpython.com/async-io-python/ — отличная статья на английском
• Книга "Python. Подробное руководство" (Билл Лубанович) — глава про асинхронность

---

<b>Заключение</b>

Асинхронное программирование — мощный инструмент для современных приложений, обрабатывающих множество одновременных запросов и событий. Оно не подходит для всех случаев, но там, где оно нужно — часто даёт ОГРОМНЫЙ прирост в производительности и удобстве кода.

Если есть вопросы — смело спрашивайте!  
Удачи в асинхронном мире Python!
"""


chunk_1 = """
Конечно! Вот то же самое длинное сообщение в Markdown:

---

<b>Введение в асинхронное программирование в Python</b>

<b>Содержание</b>

1. <a href="#что-такое-асинхронность">Что такое асинхронность?</a>
2. <a href="#проблемы-синхронного-исполнения">Проблемы синхронного исполнения</a>
3. <a href="#асинхронное-программирование-концепции">Асинхронное программирование: концепции</a>
4. <a href="#модуль-asyncio">Модуль asyncio</a>
5. <a href="#ключевые-слова-async-и-await">Ключевые слова: async и await</a>
6. <a href="#асинхронные-функции-и-корутины">Асинхронные функции и корутины</a>
7. <a href="#пример-простейший-асинхронный-код">Пример — простейший асинхронный код</a>
8. <a href="#асинхронные-задачи-и-их-исполнение">Асинхронные задачи и их исполнение</a>
9. <a href="#работа-с-сетью-асинхронные-http-запросы">Работа с сетью: асинхронные HTTP-запросы</a>
10. <a href="#асинхронная-работа-с-файлами">Асинхронная работа с файлами</a>
11. <a href="#асинхронная-работа-с-базами-данных">Асинхронная работа с базами данных</a>
12. <a href="#типичные-ошибки-новичков">Типичные ошибки новичков</a>
13. <a href="#плюсы-и-минусы-асинхронности">Плюсы и минусы асинхронности</a>
14. <a href="#мини-faq">Мини-FAQ</a>

---

<b>Что такое асинхронность?</b>

Асинхронность — это способ организации выполнения кода, при котором операции, ожидающие завершения (например, ввод-вывод — I/O), не блокируют исполнение всей программы, а дают возможность выполнять другие задачи, пока основная операция не завершилась.

Это кардинально отличается от синхронного подхода, при котором все операции выполняются строго последовательно.

---

<b>Проблемы синхронного исполнения</b>

Синхронная программа может "замереть" в ожидании:

• Данных из сети
• Ответа от базы данных
• Входных данных от пользователя
• Завершения записи на диск

<b>Пример синхронного кода</b>:
<pre><code class="language-python">import time

def download_data():
    print("Запуск скачивания данных...")
    time.sleep(5)  # Имитируем задержку — например, скачивание файла
    print("Данные скачаны!")

download_data()
print("Обработка данных...")
</code></pre>
Пока идет <code>time.sleep(5)</code>, другой код не может исполниться! Если у нас есть много таких операций — программа начинает "тормозить".

---

<b>Асинхронное программирование: концепции</b>

Асинхронное программирование строится вокруг событийного цикла (event loop) и позволяет:

• Ожидать завершения задач, не блокируя главный поток исполнения
• Использовать неблокирующие функции и библиотеки
• Оптимально расходовать вычислительные ресурсы

Это особенно полезно для программ, работающих с большим количеством сетевых соединений, совершения HTTP-запросов, выполнения операций чтения/записи и пр.

---

<b>Модуль asyncio</b>

<code>asyncio</code> — стандартный модуль в Python (версии 3.4+), реализующий инструменты асинхронного исполнения.

<b>Кратко о главном</b>

• <b>Event Loop</b> — событийный цикл, в котором запускаются все задачи
• <b>Coroutine</b> — функция, которую можно приостановить и возобновить (ключевое слово <code>async</code>)
• <b>Task</b> — обёртка над корутиной, которая ставит её в очередь на исполнение
• <b>Future</b> — результат работы асинхронной операции (пока не завершилась — pending)

---

<b>Ключевые слова: async и await</b>

• <code>async</code> перед определением функции = функция становится асинхронной (корутиной)
• <code>await</code> внутри асинхронной функции — "дождаться результата выполнения" другой корутины

<b>Пример:</b>
<pre><code class="language-python">import asyncio

async def sleep_and_print():
    print("Ждем 2 секунды...")
    await asyncio.sleep(2)
    print("Готово!")

asyncio.run(sleep_and_print())
</code></pre>"""

chunk_2 = """

---

<b>Асинхронные функции и корутины</b>

Асинхронная функция объявляется с помощью <code>async def</code>, а вызывается через <code>await</code> <b>только внутри другой асинхронной функции</b>.

<b>Важно:</b>  
• Функция с <code>async def</code> ничего НЕ будет исполнять до тех пор, пока "не будет запущена в event loop".
• Обычная main-функция НЕ может использовать <code>await</code> — только асинхронная!

---

<b>Пример — простейший асинхронный код</b>

<pre><code class="language-python">import asyncio

async def greet(name):
    print(f"Привет, {name}! Жду 1 секунду...")
    await asyncio.sleep(1)
    print(f"{name}, добро пожаловать!")

async def main():
    await greet("Пользователь")

asyncio.run(main())
</code></pre>

<b>Асинхронные задачи и их исполнение</b>

Можно запускать сразу несколько задач через <code>asyncio.create_task()</code>, чтобы они работали ПАРАЛЛЕЛЬНО (но всё равно в одном потоке).

<pre><code class="language-python">async def worker(number):
    print(f"Задача {number} стартовала")
    await asyncio.sleep(3)
    print(f"Задача {number} завершилась")

async def main():
    tasks = []
    for i in range(5):
        task = asyncio.create_task(worker(i))
        tasks.append(task)
    await asyncio.gather(*tasks)

asyncio.run(main())
</code></pre>
Этот код запустит 5 задач, и они выполнятся за 3 секунды, а не за 15!

---

<b>Работа с сетью: асинхронные HTTP-запросы</b>

Стандартная библиотека <code>asyncio</code>0 — синхронная. Специально для асинхронных задач используют, например, <b>aiohttp</b>.

<pre><code class="language-python">import aiohttp
import asyncio

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    urls = [
        "https://www.python.org",
        "https://www.asyncio.org"
    ]
    tasks = [fetch(url) for url in urls]
    results = await asyncio.gather(*tasks)
    for i, result in enumerate(results):
        print(f"Ответ с {urls[i]}: {len(result)} символов")

asyncio.run(main())
</code></pre>
---

<b>Асинхронная работа с файлами</b>

Встроенный <code>asyncio</code>1 — синхронный.  
Для асинхронного чтения используйте <b>aiofiles</b>:

<pre><code class="language-python">import aiofiles
import asyncio

async def read_my_file():
    async with aiofiles.open("somefile.txt", mode="r") as f:
        contents = await f.read()
        print(contents)

asyncio.run(read_my_file())
</code></pre>

---

<b>Асинхронная работа с базами данных</b>

Многие библиотеки поддерживают асинхронное взаимодействие с БД:  
• <b>Databases</b> (asynchronous database framework)
• <b>Tortoise ORM</b> (async ORM)
• <b>SQLAlchemy 1.4+</b> — поддержка асинхронности

<b>Пример на Databases:</b>
<pre><code class="language-python">import databases
import sqlalchemy
import asyncio

DATABASE_URL = "sqlite+aiosqlite:///test.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
)

async def main():
    await database.connect()
    query = notes.insert().values(text="Асинхронная запись!")
    await database.execute(query)
    await database.disconnect()

asyncio.run(main())
</code></pre>

---

<b>Типичные ошибки новичков</b>

1. <b>Попытка использовать await вне async-функции</b>
   <pre><code class="language-python">   await asyncio.sleep(2)   # Ошибка!
   </code></pre>

2. <b>Перезапуск event loop внутри уже работающего loop</b>
   <pre><code class="language-python">   asyncio.run(main())  # Нельзя вызывать внутри уже запущенного event loop
   </code></pre>

3. <b>Забыли добавить await</b>
   <pre><code class="language-python">   async def main():
       asyncio.sleep(2)  # Забыли await! Код не приостановится и не выполнится как надо
   </code></pre>"""

chunk_3 = """

4. <b>Использование синхронных библиотек (например, requests) в async-коде</b>  
   Это приводит к блокировке event loop

---

<b>Плюсы и минусы асинхронности</b>

| Плюсы                         | Минусы                                       |
|-------------------------------|----------------------------------------------|
| + Много одновременных задач   | – Новый синтаксис, нужно переучиваться       |
| + Не тратятся idle-ресурсы    | – Не все сторонние библиотеки поддерживают   |
| + Высокая производительность  | – Дебаг и трейсбэки иногда сложнее          |
| + Удобно для сетевого I/O     | – Не ускоряет чисто вычислительные задачи    |

---

<b>Мини-FAQ</b>

<b><b>Вопрос:</b> Что лучше — <code>asyncio</code>2 или threading / multiprocessing?</b>

<b>Ответ:</b>  
Асинхронность — для больших I/O задач без необходимости запускать новую OS thread.  
Threading — когда нужно много небольших потоков (например, для GUI, небольших фоновых задач).  
Multiprocessing — для тяжёлых вычислений, которые нужно реально распараллелить по ядрам.

---

<b><b>Вопрос:</b> Можно ли смешивать синхронный и асинхронный код?</b>

<b>Ответ:</b>  
Можно, но аккуратно (и часто через launch/future/threadpool).

---

<b><b>Вопрос:</b> Нужно ли везде использовать асинхронность?</b>

<b>Ответ:</b>  
Нет. Если твоя программа делает много работы исключительно с CPU (<code>asyncio</code>3), асинхронность не даст прироста.  
Асинхронность полезна для большого числа сетевых и файловых операций.

---

<b><b>Вопрос:</b> Зачем нужны корутины, tasks и event loop?</b>

<b>Ответ:</b>  
• <b>Корутины</b> — функции, выполнение которых можно "приостанавливать" и "дожидаться" исполнения других корутин без блокировки event loop.
• <b>Tasks</b> — обёртки вокруг корутин, которые можно запустить параллельно.
• <b>Event Loop</b> — цикл, который управляет исполнением задач.

---

<b><b>Вопрос:</b> Как сделать паузу внутри асинхронного кода?</b>

<b>Ответ:</b>  
Вместо <code>asyncio</code>4 используйте:

<pre><code class="language-python">await asyncio.sleep(3)
</code></pre>

---

<b><b>Вопрос:</b> Как запустить асинхронный код из обычной функции?</b>

<b>Ответ:</b>  
Используйте <code>asyncio</code>5.

---

<b><b>Вопрос:</b> Какие есть реальные фреймворки для асинхронности в вебе?</b>

<b>Ответ:</b>  
• FastAPI (asgi, асинхронный)
• Starlette
• Sanic
• AIOHTTP

---

<b><b>Вопрос:</b> Где читать дальше?</b>

• https://docs.python.org/3/library/asyncio.html — официальная документация
• https://realpython.com/async-io-python/ — отличная статья на английском
• Книга "Python. Подробное руководство" (Билл Лубанович) — глава про асинхронность

---

<b>Заключение</b>

Асинхронное программирование — мощный инструмент для современных приложений, обрабатывающих множество одновременных запросов и событий. Оно не подходит для всех случаев, но там, где оно нужно — часто даёт ОГРОМНЫЙ прирост в производительности и удобстве кода.

Если есть вопросы — смело спрашивайте!  
Удачи в асинхронном мире Python!
"""

valid_chunks = [chunk_1, chunk_2, chunk_3]

def test():
  chunks = split_html_for_telegram(example_text)
  assert chunks == valid_chunks
