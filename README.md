# Скрипт для создания отчетов на основе log файлов
## Запуск скрипта
1. Скопировать репозиторий и затем перейти в выбранную папку.
2. Создать виртуальное окружение и активировать его.
   ```bash
   python -m venv .venv
   source .venv/bin/activate #(Linux)
   ```
   или
   ```bash
   source .venv/scripts/activate #(Windows)
   ```
4. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```
5. Запустить скрипт командой:
   ```bash
   python main.py --file <путь_до_log_файлов> --report average
   ```
6. Также можно использовать необязательный параметр --date для отображения отчетов только для логов с этой датой:
   ```bash
   python main.py --file <путь_до_log_файлов> --report average --date <дата>
   ```
## Примеры запуска скрипта
Запуск скрипта без параметра --date:
<img width="1493" height="190" alt="image" src="https://github.com/user-attachments/assets/ccc38729-d17f-452b-b35a-6097d775e2a1" />
Запуск скрипта с параметром --date:
<img width="1860" height="205" alt="image" src="https://github.com/user-attachments/assets/6693c46c-3abb-4465-8dd5-815f41aa613a" />
## Особенности добавления нового функционала для создания других отчетов
Для того, чтобы добавить новый функционал для создания других отчетов, например user-agent, нужно создать функцию, которая будет создавать отчет и обернуть ее в декоратор reg_report("название_отчета"), например:
```python
@reg_report("user-agent")
def process_logs_user_agent(logs: list[dict[str, Any]],
                         date_filter: str = None) -> list[tuple]:
  pass #Вместо этого должна быть реализация для создания отчета
```
А также добавить нужные столбцы при создании таблицы, в данный момент там переданы столбцы для отчета average.
## Запуск тестов
Для запуска тестов нужно ввести команду:
```bash
pytest
```
или если нужно проверь покрытие:
```bash
pytest --cov
```
## Примеры запуска тестов
Запуск тестов:
<img width="1919" height="434" alt="image" src="https://github.com/user-attachments/assets/f7f76472-753f-460e-b765-65ffcbf0162b" />
Запуск тестов с оценкой покрытия:
<img width="1918" height="636" alt="image" src="https://github.com/user-attachments/assets/3830bd12-be81-4027-8c3f-18d9932f468e" />


   
   
