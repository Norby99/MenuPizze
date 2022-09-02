from datetime import datetime

class Logger():

    _log_file: str

    def __init__(self, log_file=None):
        self._log_file = log_file

    def write(self, msg):
        if self._log_file is None:
            raise AttributeError("Log file not specified")

        with open(self._log_file, 'a') as f:
            f.write(f"{self._text_converter(msg)}\n")

    def disp(self, msg):
        print(self._text_converter(msg))

    def _text_converter(self, text):
        return f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}"

if __name__ == '__main__':
    logger = Logger()
    logger.disp("test")
