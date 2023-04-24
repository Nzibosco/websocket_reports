# Main server program to run the websocket application
import asyncio
import logging
import ssl

import websockets
from websockets.exceptions import ConnectionClosed

from security.ssl_certs import SslContext
from service.message_service import MessageService


class Server:
    def __init__(self, logger):
        self.logger = logger
        self.service = MessageService(logger)

    async def handle_client_comm(self, websocket, path):
        remote_addr = websocket.remote_address
        self.logger.info(f'Server::handle_client_comm() - Connection established. remote address: {remote_addr}')

        try:

            async for msg in websocket:
                self.logger.info(f'Server::handle_client_comm() - Received message from client: {msg}')
                res = self.service.process_client_msg(msg)
                await websocket.send(res)
                self.logger.info(f'Server::handle_client_comm() - Sent response to client: {res}')
        except ConnectionClosed as e:
            self.logger.error(f'Server::handle_client_comm() - Error. Connection closed by client: {e}')

    def run(self, address, port):
        self.logger.info(f'Starting websocket server on port {port}')

        #ssl_context = SslContext(self.logger).get_context()
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(certfile='server.crt', keyfile='server.key')
        start_server = websockets.serve(self.handle_client_comm,
                                        address,
                                        port,
                                        ssl=ssl_context)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()


def setup_logger():
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger('WEBSOCKET SERVER')


def main():
    logger = setup_logger()
    server = Server(logger)
    port = 8765
    address = 'localhost'
    server.run(address, port)


if __name__ == '__main__':
    main()
