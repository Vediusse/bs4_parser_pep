# Парсер документации python и PEP
## Описание
Парсер информации о python с сайтов 
**https://docs.python.org/3/**
**https://peps.python.org/**

Клонирование репозитория к себе на компбютер: 

```
git clone git@github.com:Vediusse/bs4_parser_pep.git
```

Создание виртуального окружения и установка зависимостей:

```
python -m venv venv

pip install -r requirements.txt
```

```
cd src/
```

### Работа с прасером

```
python main.py [вариант парсера] [аргументы]
```
Для получения полного списка команд и описания работы парсера:
```
python main.py -h
```

### Парсеры 

- whats-new   
**https://docs.python.org/3/whatsnew/**
```
python main.py whats-new [аргументы]
```
Парсер вывода списока изменений в python.

- latest_versions
**https://docs.python.org/3/whatsnew/**
```
python main.py latest-versions [аргументы]
```
Парсер вывода списка версий python и ссылки на их документацию.

- download
**https://docs.python.org/3/download.html**
```
python main.py download [аргументы]
```
Парсер скачивания документации zip-архивов с документацией python

- pep 
```
python main.py pep [аргументы]
```
Парсер вывода списка статусов pep и количесвтодокументов в каждом статусе


### Аргументы
- -c, --clear-cache
Очистка кеша перед выполнением парсинга.
```
python main.py [вариант парсера] -c
```
- -o {pretty,file}, --output {pretty,file}   
Дополнительные способы вывода данных   
pretty - выводит данные в командной строке в таблице в формате PrettyTable
file - сохраняет информацию в формате csv в папке ./results/
```
python main.py [вариант парсера] -o file
```


### Автор
- [Рублёв Валерий](https://github.com/Vediusse "GitHub аккаунт")


