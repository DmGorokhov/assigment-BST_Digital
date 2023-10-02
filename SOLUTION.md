
### *R4C - Robots for consumers test-assigment review*
___
[![Maintainability](https://api.codeclimate.com/v1/badges/5a0ee94f57ee088833e3/maintainability)](https://codeclimate.com/github/DmGorokhov/assigment-BST_Digital/maintainability)

### Task 1. От технического специалиста компании.
Создать API-endpoint, принимающий и обрабатывающий информацию в формате JSON. 
В результате web-запроса на этот endpoint, в базе данных появляется запись 
отражающая информацию о произведенном на заводе роботе.  
_**Примечание от старшего технического специалиста**_:  
Дополнительно предусмотреть валидацию входных данных, на соответствие существующим в системе моделям.
### Solution 1:
* /api/v1/robots/new
---
### Task 2. От директора компании
Я как директор хочу иметь возможность скачать по прямой
ссылке Excel-файл со сводкой по суммарным показателям
производства роботов за последнюю неделю.  
_**Примечание от менеджера**_. Файл должен включать в себя несколько страниц, на каждой из которых представлена информация об одной модели, но с детализацией по версии.
### Solution 2:
* /api/v1/robots/week_report
---

### Task 3. От клиента компании.
**Job story**: Если я оставляю заказ на робота, и его
нет в наличии, я готов подождать до момента появления робота.
После чего, пожалуйста пришлите мне письмо.

### Solution 3:
* /api/v1/orders/new
---

### Source code is available on GitHub:

```shell
https://github.com/DmGorokhov/assigment-BST_Digital
```

You can run the application with Poetry.

**Poetry** is setup by the commands:

**Linux, macOS, Windows (WSL):**

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Details on installing and using the **Poetry** package are available in [official documentation](https://python-poetry.org/docs/).

To install **Poetry** you need **Python 3.7+** use the information from the official website [python.org](https://www.python.org/downloads/)

When cloning app repository, you may need to install Make for run short console-commands described below.  
Also be sure what Redis is installed.

#### *Installation*

```
make install   # install poetry for dependency management
```
Set environment variables using file .env.example as example.

#### Basic shortcut commands:for development DEBUG variable must be set as True

```
make build   # run migrations
```
```
make setup   # create superuser 
```
---
#### *Usage*

```
make start   # starts both redis and app on the local server in the development environment
```
---
* If Redis already run on your host machine:
 ```
make start-server
```
---
```
make run-celery   # starts celery workers for background api tasks
```
 Now you can make requests to api endpoints described in Task-Solution sections above 

---
#### Additional service commands:
```
make test   # Run tests
```
```
make test-coverage   # generate test-coverage report for oberview in browser
```