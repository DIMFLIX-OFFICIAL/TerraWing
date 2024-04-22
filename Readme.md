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
  
Просмотр доступных версий python в pyenv: `pyenv install --list`\  
Устанавливаем python не ниже версии 3.11: `pyenv install 3.11.8`  
  
### Устанавливаем пакетный менеджер poetry  
- Windows Powershell: `(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -`  
- Linux/macOS: `curl -sSL https://install.python-poetry.org | python3 -`  
  
### Виртуальное окружение  
Если Вы используете `pyenv` выполните следующие команды:  
- `poetry config virtualenvs.prefer-active-python true`  
- `pyenv local <номер версии python, в нашем случае 3.11.8>`  
  
Подготовка виртуального окружения для poetry: `poetry use env <номер версии python, в нашем случае 3.11.8>`\  
Входим в виртуальное окружение `poetry shell`\  
Установка зависимостей: `poetry install`  
  
Копируем шаблон файла настроек:  
- Windows: `copy .env.dist .env`  
- Linux/macOS: `cp .env.dist .env`  
  
Редактируем в .env наши настройки...  
  
### Запуск сервера  
Выполняем команду `python app.py`  
  
# Dev  
## Помощь в разработке  
- Линтер `ruff` \  
  Для запуска использовать следующую команду `poetry run ruff check src`  
- Форматирование кода `black` \  
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

# License
<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/">
  <a property="dct:title" rel="cc:attributionURL" href="https://github.com/DIMFLIX-OFFICIAL/TerraWing">TerraWing</a>
  by 
  <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://github.com/DIMFLIX-OFFICIAL">DIMFLIX-OFFICIAL</a> 
  is licensed under 
  <a href="https://creativecommons.org/licenses/by-nc/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">
    Creative Commons Attribution-NonCommercial 4.0 International<br>
    <img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt="">
    <img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt="">
    <img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nc.svg?ref=chooser-v1" alt="">
  </a>
</p>



