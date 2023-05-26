import os
from base64 import b64encode


class Message:
    def __init__(self):
        self._msg = ''

    def configure_message(self, sender, receiver, subject, text, path):
        if not subject:
            subject = ''
        mail_subject = '=?UTF-8?B?' + b64encode(subject.encode('utf-8')).decode('utf-8') + '?='
        mail_text = b64encode(text.encode('utf-8')).decode('utf-8')

        body = "Mime-Version: 1.0\n"
        body += "Content-Type: multipart/mixed; boundary=\"my_bound\"\n\n"
        body += '--my_bound\nContent-Type: text/plain;\n\tcharset=\"UTF-8\"\nContent-Transfer-Encoding: base64\n\n' \
                + mail_text + '\n'

        for _, binary in enumerate(self._get_binary_from(path)):
            body += '--my_bound\nContent-Type: application/octet-stream; name=' + binary[0] + '\n'
            body += "Content-Transfer-Encoding: base64\n"
            body += 'Content-Disposition: inline; filename=' + binary[0] + '\n\n'
            body += binary[1] + '\n'
        body += "\n--my_bound--\n"

        self._msg = f'From:{sender}\n\rTo:{receiver}\n\rSubject:{mail_subject}\n\r{body}\n\r.\n\r'

    @staticmethod
    def _get_binary_from(path):
        if not path:
            return b''
        for filename in os.listdir(path):
            with open(os.path.join(path, filename), 'rb') as file:
                content = b''
                for lines in file:
                    content += lines
                yield filename, b64encode(content).decode('utf-8')

    @property
    def message(self):
        return self._msg
