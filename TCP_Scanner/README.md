TCP-UDP Scanner
======

Данный скрипт позволяет определить открытые TCP и UDP порты в заданном диапазоне, а также определить протокол, который работает на открытом порте.

## Параметры запуска
```
usage: scanner.py [-h] [-p PORTS] target

positional arguments:
  target                Целевой адрес сканирования

optional arguments:
  -h, --help            show this help message and exit
  -p PORTS, --ports PORTS
                        Список портов для сканирования, указанных через ",";
                        можно указывать диапазон (80, 144, 2303-2400)
```

## Пример запуска

```
>python3 scanner.py -p 631,6942,53 127.0.0.1
Scanning 127.0.0.1...
631/tcp 	ipp 	open
6942/udp 	open
53/tcp 	closed
```