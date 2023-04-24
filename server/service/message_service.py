# Main logic to handle message and respond based on request
from datetime import datetime
import pandas as pd


class MessageService:
    def __init__(self, logger):
        self.logger = logger
        self.data = self.load_data()

    def load_data(self):
        df = pd.read_excel('./data_gen/products.xlsx')
        self.logger.info('Data loaded successfully')
        return df

    def process_client_msg(self, msg):

        self.logger.info(f'process_client_msg() - Started processing request from client. Message: {msg}')

        try:
            if msg is not None and len(msg.strip()) > 1:
                message = msg.lower()
                if 'hello' in message or 'hi' in message or 'greetings' in message:
                    response = "Hello! How can I help you?"
                elif 'time' in message:
                    response = f"The current time is: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                elif message.startswith("product"):
                    response = self.handle_product_id(message)
                elif message in ['list categories', 'get categories', 'all categories', 'categories']:
                    response = self.handle_category()
                else:
                    response = "Sorry, I didn't understand your request. Try again with another question"
            else:
                response = f'Sorry. I could not understand your message; {msg}'
        except Exception as e:
            self.logger.error(f'Server::process_client_msg() - Error: {e}')
            response = f'Sorry. An error occurred when I was processing your request, {msg}'

        return response

    def handle_product_id(self, msg):
        product_id = int(msg.split(" ")[1])
        product = self.data.loc[self.data["ProductID"] == product_id]
        if not product.empty:
            response = f"Product {product_id}: {product['ProductName'].values[0]} is in {product['Category'].values[0]} category and costs ${product['Price'].values[0]}"
        else:
            response = f"No product found with id {product_id}"
        return response

    def handle_category(self):
        unique_categories = self.data["Category"].unique()
        return f"List of all categories: {', '.join(unique_categories)}"


    def handle_prices(self, msg):
        pass


