import datetime

class myCustomLogger:
    
    def __init__(self, name, level):
        self.name = name
        self.level = level
        
    def debug(self, message):
        self.log('DEBUG', message)
        
    def info(self, message):
        self.log('INFO', message)
        
    def warning(self, message):
        self.log('WARNING', message)
        
    def error(self, message):
        self.log('ERROR', message)
        
    def critical(self, message):
        self.log('CRITICAL', message)
        
    def log(self, level, message):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f'{timestamp} [{self.name}] {level}: {message}'
        print(log_message)
