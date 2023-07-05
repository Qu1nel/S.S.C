from typing import LiteralString

# Аннотация typing.LiteralString полезна для конфиденциальных API, где произвольные строки, созданные пользователем,
# могут вызвать проблемы.


def run_query(query: LiteralString) -> None: ...


def caller(arbitrary_string: str, literal_string: LiteralString) -> None:
    run_query("SELECT * FROM students")  # проверка типа -> OK
    run_query(literal_string)  # проверка типа -> OK
    run_query("SELECT * FROM " + literal_string)  # проверка типа -> OK
    run_query(arbitrary_string)  # ошибка проверки типа
    run_query(  # ошибка проверки типа
        f"SELECT * FROM students WHERE name = {arbitrary_string}"
    )

# Аннотация LiteralString может использоваться для указания того, что параметр функции может относиться к любому
# литеральному строковому типу. Это позволяет функции принимать произвольные типы литеральных строк, а также строки,
# созданные из других литеральных строк. Затем средства проверки типов могут обеспечить, чтобы конфиденциальные
# функции, такие как те, которые выполняют операторы SQL или команды оболочки, вызывались только со статическими
# аргументами, обеспечивая защиту от атак путем внедрения.
