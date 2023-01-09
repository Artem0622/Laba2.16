# !/usr/bin/env python3
import sys
import json
import jsonschema


def add(list_stud):
    """
    Запросить данные о студентах.
    """
    name = input("Фамилия и инициалы? ")
    number = input("Номер группы? ")
    marks = list(map(int, input("Успеваемость").split()))
    # Создать словарь.
    student = {
        "name": name,
        "number": number,
        "marks": marks,
    }
    # Добавить словарь в список.
    list_stud.append(student)
    # Отсортировать список в алфавитном порядке.
    if len(list_stud) > 1:
        list_stud.sort(key=lambda item: item.get("name", ""))
    return list_stud


def list_p():
    """
    Отабразить список работников
    """
    line = "+-{}-+-{}-+-{}-+-{}-+".format("-" * 4, "-" * 30, "-" * 20, "-" * 15)
    print(line)
    print(
        "| {:^4} | {:^30} | {:^20} | {:^15} |".format(
            "№", "Ф.И.О.", "Номер группы", "Успеваемость"
        )
    )
    print(line)
    # Вывести данные о всех студентах.
    for idx, worker in enumerate(students, 1):
        print(
            "| {:>4} | {:<30} | {:<20} | {:>15} |".format(
                idx,
                worker.get("name", ""),
                worker.get("number", ""),
                " ".join([str(x) for x in worker.get("marks", 0)]),
            )
        )
    print(line)


def select():
    """
    Выбрать студентов с оценками 2
    """
    # Инициализировать счётчик
    count = 0
    # Проверить студентов хотя бы на одну оценку.
    for student in students:
        if 2 in student.get("marks", []):
            count -= 1
            print(
                "{:>4} {}".format("*", student.get("name", "")),
                "{:>1} {}".format("группа №", student.get("number", "")),
            )
            # Если счётчик равен 0, то оценки не найдены.
    if count == 0:
        print("Таких студентов нет")


def save_students(file_name, students):
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(students, fout, ensure_ascii=False, indent=4, default=str)


def load_students(file_name):
    schema = {
        "type": "array",
        "items": [
            {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "number": {"type": "string"},
                    "marks": {
                        "type": "array",
                        "items": [
                            {"type": "integer"},
                            {"type": "integer"},
                            {"type": "integer"},
                            {"type": "integer"},
                            {"type": "integer"},
                        ],
                    },
                },
                "required": ["name", "number", "marks"],
            }
        ],
    }
    with open(file_name, "r", encoding="utf-8") as fin:
        loadfile = json.load(fin)
        validator = jsonschema.Draft7Validator(schema)
        try:
            if not validator.validate(loadfile):
                print("Валидация прошла успешно")
        except jsonschema.exceptions.ValidationError:
            print("Ошибка валидации", file=sys.stderr)
            exit()
        return loadfile


def help_d():
    """
    Отабразить список команд
    """
    print("Список команд:\n")
    print("add - добавить студента;")
    print("list - вывести список студентов;")
    print("select - вывести список студентов, имеющих оценку 2;")
    print("help - отобразить справку;")
    print("exit - завершить работу с программой.")


if __name__ == "__main__":
    # Список студентов.
    students = []
    # Организовать бесконечный цикл запроса команд.
    while True:
        # Запросить команду из терминала.
        command = input(">>> ").lower()
        # Выполнить действие в соответствие с командой.
        if command == "exit":
            break
        elif command == "add":
            students = add(students)
        elif command == "list":
            list_p()
        elif command == "select":
            select()
        elif command.startswith("save "):
            parts = command.split(maxsplit=1)
            file_name = parts[1]
            save_students(file_name, students)
        elif command.startswith("load "):
            parts = command.split(maxsplit=1)
            file_name = parts[1]
            students = load_students(file_name)
        elif command == "help":
            help_d()
        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)
