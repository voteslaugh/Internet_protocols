# SMTP Client

## Как работает
Необходимо включить соответствующие разрешения в Вашем почтовом сервисе
## Параметры запуска
```
usage: smtp-client.py [-h] [--server SERVER] [--port PORT]
                      [--username USERNAME] [--subject SUBJECT] [--text TEXT]
                      [--path PATH]
                      login password receiver

SMTP client

positional arguments:
  login                 Sender email address
  password              Password
  receiver              Receiver email address

optional arguments:
  -h, --help            show this help message and exit
  --server SERVER       SMTP server
  --port PORT           Port to use
  --username USERNAME   Username
  --subject SUBJECT, -s SUBJECT
                        Message subject
  --text TEXT, -t TEXT  Message text
  --path PATH, -p PATH  Path for attachment
```

## Пример использования
```bash
python3 main.py почта_отправителя@почта.домен **password** почта_получателя@почта2.домен2 -t Hello
```