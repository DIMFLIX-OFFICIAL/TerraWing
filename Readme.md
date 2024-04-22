# TerraWing - БПЛА в АПК  
TerraWing - сервис для распознавания препятствий на пути движения БПЛА и их классификации. Наше решение предназначено для использования в агропромышленном комплексе.  
## Уникальность
- Быстродействие работы системы
- Проект доведен до стадии MVP
- Использование 
## Перспективы развития
- [ ] Специализированный датасет
- [ ] Плагины ИИ встраиваемые на сервере для возможности работы с разными задачами
- [ ] Автоматическое составление карты рабочей местности для дрона
- [ ] Совместная работа нескольких БПЛА
- [ ] Интеграция с погодными сервисами.
# Начало работы  
### Установим pyenv для удобного управления версиями python  
- Windows Chocolatey: `choco install pyenv-win`  
- Linux/macOS: `curl https://pyenv.run | bash`  
  
Просмотр доступных версий python в pyenv: `pyenv install --list`
Устанавливаем python не ниже версии 3.11: `pyenv install 3.11.8`  
  
### Устанавливаем пакетный менеджер poetry  
- Windows Powershell: `(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -`  
- Linux/macOS: `curl -sSL https://install.python-poetry.org | python3 -`  
  
### Виртуальное окружение  
Если Вы используете `pyenv` выполните следующие команды:  
- `poetry config virtualenvs.prefer-active-python true`  
- `pyenv local <номер версии python, в нашем случае 3.11.8>`  
  
Подготовка виртуального окружения для poetry: `poetry use env <номер версии python, в нашем случае 3.11.8>`  
Входим в виртуальное окружение `poetry shell`  
Установка зависимостей: `poetry install`  
  
Копируем шаблон файла настроек:  
- Windows: `copy .env.dist .env`  
- Linux/macOS: `cp .env.dist .env`  
  
Редактируем в .env наши настройки...  
  
### Запуск сервера  
Выполняем команду `python app.py`  
  
# Dev  
## Помощь в разработке  
- Линтер `ruff`   
  Для запуска использовать следующую команду `poetry run ruff check src`  
- Форматирование кода `black`   
  Для запуска используем следующую команду: `poetry run black src`  
  
## Тесты сервера  
В папке `tests` вы можете найти файл `test_video_stream.py` 
Этот файл дает нам возможность эмитировать дрон, посылая в качестве видеопотока на сервер либо любой файл с видео, либо транслировать свою веб-камеру. 

Для запуска клиента с трансляцией заранее заготовленного видео используйте эту команду:
`python test_video_stream.py <drone_id> <drone_secret> --video_source <путь>`

> [!NOTE] 
> Если вы хотите транслировать веб-камеру, то просто удалите аргумент **`video_source`**

## Обучение модели
По пути `src/neural_network` вы можете найти файл `TrainNeuralNetwork.ipynb`. Как-раз таки он служит для обучения нейронки. 

> [!NOTE] 
> Датасет должен находиться в папке **`src/data/DATASET`**

> [!WARNING]
> Если вы используете Pycharm и индексацию файлов, советуем вам добавить папку с датасетом в исключение (excluded). Это можно сделать нажатием правой кнопки мыши по папке, после чего выбрав пункт `Mark Directory as`. Там вам нужно выбрать `excluded`.

# License - Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
The full text of the license is available here: [CC BY-NC 4.0 Legal Code](https://creativecommons.org/licenses/by-nc/4.0/legalcode).

## You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material
The licensor cannot revoke these freedoms as long as you follow the license terms.

## Under the following terms:
- Attribution — You must give appropriate credit , provide a link to the license, and indicate if changes were made . You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- NonCommercial — You may not use the material for commercial purposes .
- No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

This is just a brief excerpt of the main points of the license. Please refer to the full legal text of the license for a full understanding of its terms.




