@echo off
REM Переходим в директорию проекта
cd /d %~dp0

REM Выводим текущий путь для отладки
echo Current path: %cd%

REM Проверяем наличие файла requirements.txt
if not exist requirements.txt (
    echo File requirements.txt not found!
    pause
    exit /b 1
)

REM Создаем виртуальную среду, если она еще не создана
if not exist venv (
    python -m venv venv
)

REM Активируем виртуальную среду
call venv\Scripts\activate

REM Устанавливаем необходимые библиотеки, если они еще не установлены
pip install -r requirements.txt

REM Запускаем программу
python main.py

REM Деактивируем виртуальную среду после завершения работы программы
deactivate

pause