# hlynov-test-assignment

Тестовое задание специалоьно для банка Хлынов

## Опсиание задания

[task_description](https://github.com/akorzunin/hlynov-test-assignment/blob/main/task_description.md)

## Установка

### via poetry

```sh
    pip install poetry
    poetry install --no-dev
    poetry shell
    python main.py {file}
```

### via pip

```sh
    python -m pip install -r requirements.txt
    python main.py {file}
```

## Тесты

```sh
    poetry install
    poetry shell
    pytest ./test/test_main.py
```
