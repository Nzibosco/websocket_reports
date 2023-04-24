# Main class to configure certificates and provide an ssl context to secure server messages on the network
import ssl


class SslContext:

    def __init__(self, logger):
        self.logger = logger

    def get_context(self):
        try:
            self.logger.info("SslContext::get_context() - Started setting up ssl certificates")
            # SSL certificates
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ssl_context.load_cert_chain(certfile='server.crt', keyfile='server.key')
            self.logger.info("SslContext::get_context() - certificate set up success")

        except Exception as e:
            self.logger.error(f'SslContext::get_context() - Error: {e}')
