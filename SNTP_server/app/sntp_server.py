import signal
import socket
import select
from struct import pack, unpack
from time import time
from app.dependencies import get_server_settings

SETTINGS = get_server_settings()
# Размер буфера для приема данных через сокет.
BUFFER_SIZE = 4096
# Формат заголовка пакета SNTP, используемый для упаковки и распаковки данных.
HEAD_FORMAT = ">BBBBII4sQQQQ"
# Смещение времени в секундах между меткой времени 1 января 1900 года и меткой времени 1 января 1970 года (эпоха Unix).
UTC_OFFSET = 2208988800
# Режим работы SNTP-сервера. Значение 4 указывает на серверный режим.
MODE = 4


class SNTPServer:
    """
    Класс, представляющий простой SNTP-сервер.
    """
    def __init__(self):
        self._stratum = SETTINGS["stratum"]
        self._leap_indicator = SETTINGS["leap_indicator"]
        self._version_number = SETTINGS["version_number"]
        self._offset = SETTINGS["offset"]
        self._socket = self._create_socket(SETTINGS["server_ip"],
                                           SETTINGS["server_port"])
        self._is_running = False
        signal.signal(signal.SIGINT, self._close)

    def run(self):
        """
        Запуск SNTP-сервера для обработки запросов.
        """
        self._is_running = True
        while self._is_running:
            if self._is_socket_ready():
                request, addr = self._socket.recvfrom(BUFFER_SIZE)
                response = self._handle_request(request)
                self._socket.sendto(response, addr)

    def _handle_request(self, request: bytes) -> bytes:
        """
        Обработка входящего запроса и формирование ответа.

        Args:
            request: Входящий запрос в виде байтов.

        Returns:
            bytes: Ответ на запрос в виде байтов.
        """
        dispatch_time = self._get_dispatch_time(request)
        receipt_time = self._get_current_time()
        return self._build_response(dispatch_time, receipt_time)

    def _build_response(self, dispatch_time, receipt_time) -> bytes:
        """
        Формирование ответа на запрос.

        Args:
            dispatch_time: Время отправки запроса.
            receipt_time: Время получения запроса.

        Returns:
            bytes: Ответ на запрос в виде байтов.
        """
        return pack(
            HEAD_FORMAT,
            self._leap_indicator << 6 | self._version_number << 3 | MODE,
            self._stratum,
            0, 0, 0, 0, b'', 0,
            dispatch_time,
            receipt_time,
            self._get_current_time()
        )

    def _is_socket_ready(self) -> bool:
        """
        Проверка готовности сокета для чтения.

        Returns:
            bool: True, если сокет готов для чтения, False в противном случае.
        """
        read_list, _, _ = select.select([self._socket], [], [], 1)
        return bool(read_list)

    def _get_current_time(self) -> int:
        """Получение текущего времени с учетом смещения.

        Returns:
            int: Текущее время в виде целого числа.
        """
        time_with_offset = time() + UTC_OFFSET + self._offset
        return int(time_with_offset * (2 ** 32))

    def _close(self, _, __):
        """
        Обработчик сигнала закрытия сервера.
        """
        self._is_running = False
        self._socket.close()

    @staticmethod
    def _get_dispatch_time(request: bytes) -> int:
        """Извлечение времени отправки из входящего запроса.

        Args:
            request: Входящий запрос в виде байтов.

        Returns:
            int: Время отправки запроса в виде целого числа.
        """
        return unpack(HEAD_FORMAT, request)[10]

    @staticmethod
    def _create_socket(ip: str, port: int) -> socket.socket:
        """
        Создание сокета и привязка к указанному IP и порту.

        Args:
            ip: IP-адрес сервера.
            port: Порт сервера.

        Returns:
            socket: Созданный сокет.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((ip, port))
        return sock
