import pandas as pd

# Generate sample data about random products
products = []
for i in range(1, 10001):
    products.append({
        "ProductID": i,
        "ProductName": f"Product {i}",
        "Category": f"Category {i % 10}",
        "Price": i * 10
    })

# Create a DataFrame from the sample products generated from above
df = pd.DataFrame(products)

# Save the DataFrame to an Excel file on local file system
df.to_excel("./products.xlsx", index=False)
