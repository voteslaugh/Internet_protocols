# Кэширующий DNSServer сервер

Этот проект представляет собой реализацию кэширующего DNSServer сервера на Python. Сервер прослушивает 53 порт и позволяет выполнить разрешение DNSServer-запроса клиента.

## Как это работает

При первом запуске кэш пустой. Сервер получает от клиента рекурсивный запрос и выполняет разрешение запроса. Получив ответ, сервер разбирает пакет ответа, извлекает из него всю полезную информацию, т. е. все ресурсные записи, а не только то, о чем спрашивал клиент, и сохраняет ее в кэше сервера. 

Сервер регулярно просматривает кэш и удаляет просроченные записи, используя поле TTL.

Сервер не теряет работоспособность, если старший сервер почему-то не ответил на запрос. 

Во время штатного выключения сервер сериализует данные из кэша, сохраняя их на диск. При повторных запусках сервер считывает данные с диска и удаляет просроченные записи, инициализирует таким образом свой кэш.

## Использование

1. Склонируйте проект к себе на компьютер.
2. Запустите сервер, выполнив следующую команду в терминале:

   ```
   python main.py
   ```
   
   По умолчанию сервер прослушивает 53 порт и использует стандартный DNSServer-сервер Google (`8.8.8.8`).