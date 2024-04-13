# TerraWing - БПЛА в АПК
TerraWing - сервис для распознавания препятствий на пути движения БПЛА и их классификация. 
Наше решение предназначено для использования в агропромышленном комплексе.

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
Выполняем команду `python3 app.py`

# Dev Dependencies
Линтер `ruff`
Для запуска использовать следующую команду `poetry run ruff src`

Так-же для автоматического форматирования кода под стандарт PEP8 мы используем black. 
Для запуска используем следующую команду: `poetry run black src`
