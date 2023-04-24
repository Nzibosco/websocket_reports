# Main logic to handle message and respond based on request
import re
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
                if 'hello' in message or 'greetings' in message:
                    response = "Hello! How can I help you?"
                elif 'time' in message:
                    response = f"The current time is: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                elif message.startswith("product"):
                    response = self.__handle_product_id(message)
                elif message in ['list categories', 'get categories', 'all categories', 'categories']:
                    response = self.__handle_category()
                elif "average price" in message or "avg price" in message or "average" in message or "avg" in message:
                    response = self.__handle_average_price()
                elif "highest prices" in message or "most expensive products" in message:
                    response = self.__highest_prices_products(message)
                elif "lowest prices" in message or "cheapest products" in message:
                    response = self.__cheapest_products(message)
                elif "price range" in message or "products between" in message:
                    response = self.__price_range(message)
                else:
                    response = "Sorry, I didn't understand your request. Try again with another question"
            else:
                response = f'Sorry. I could not understand your message; {msg}'
        except Exception as e:
            self.logger.error(f'Server::process_client_msg() - Error: {e}')
            response = f'Sorry. An error occurred when I was processing your request, {msg}'

        return response

    def __handle_product_id(self, msg):
        product_id = int(msg.split(" ")[1])
        product = self.data.loc[self.data["ProductID"] == product_id]
        if not product.empty:
            response = f"Product {product_id}: {product['ProductName'].values[0]} is in {product['Category'].values[0]} category and costs ${product['Price'].values[0]}"
        else:
            response = f"No product found with id {product_id}"
        return response

    def __handle_category(self):
        unique_categories = self.data["Category"].unique()
        return f"List of all categories: {', '.join(unique_categories)}"

    def __handle_average_price(self):
        avg_price = self.data["Price"].mean()
        return f"The average price of all products is: ${avg_price:.2f}"

    def __highest_prices_products(self, message):

        try:
            n = int(message.split(" ")[1])  # Extract the desired number
        except ValueError:
            n = 10  # Default value for N if it's not provided or cannot be parsed

        top_n_products = self.data.nlargest(n, "Price")
        top_n_products_list = top_n_products.apply(lambda x: f"{x['ProductName']} (${x['Price']})", axis=1).tolist()
        return f"Top {n} products with the highest prices: {', '.join(top_n_products_list)}"

    def __cheapest_products(self, message):

        try:
            n = int(message.split(" ")[1])  # Extract the desired number
        except ValueError:
            n = 10  # Default value for N if it's not provided or cannot be parsed

        cheap_products = self.data.nsmallest(n, "Price")
        cheap_products_list = cheap_products.apply(lambda x: f"{x['ProductName']} (${x['Price']})", axis=1).tolist()
        return f"Top {n} products with the highest prices: {', '.join(cheap_products_list)}"

    def __price_range(self, message):
        try:
            prices = [float(x) for x in
                      re.findall(r'\d+(?:\.\d+)?', message)]  # Extract the price range values from the command
            if len(prices) != 2:
                raise ValueError("Invalid price range")
            min_price, max_price = min(prices), max(prices)
        except ValueError as e:
            response = "Please provide a valid price range. Example: 'price range 100 to 500' or 'products between 100 and 500'"
        else:
            products_in_range = self.data[(self.data["Price"] >= min_price) & (self.data["Price"] <= max_price)]
            products_in_range_list = products_in_range.apply(lambda x: f"{x['ProductName']} (${x['Price']})",
                                                             axis=1).tolist()
            response = f"Products in the price range ${min_price} to ${max_price}: {', '.join(products_in_range_list)}"
        return response
