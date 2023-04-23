# Main server program to run the websocket application
import logging
class Server:
    def __init__(self, logger):
        self.logger = logger

    def run(self):
        self.logger.info('Server is running!')



def setup_logger():
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger('WEBSOCKET SERVER')

def main():
    logger = setup_logger()
    server = Server(logger)
    server.run()

if __name__ == '__main__':
    main()

