"""
Basic usage example for the MoySklad API client.
"""

# import setup_path

from dotenv import load_dotenv
import os

load_dotenv()

from moysklad_api import MoySklad
from moysklad_api.entities.products import Product
from moysklad_api.entities.base import Meta
from moysklad_api.entities.counterparty import Counterparty
from moysklad_api.exceptions import NotFoundException

token = os.getenv("MOYSKLAD_TOKEN")

# Initialize the client
client = MoySklad(
    token=token,
    debug=True
)

# Get current user info
current_employee = client.employees.get_current()
print(f"Logged in as: {current_employee.fullName}")

# Get organizations
organizations, meta = client.organizations.find_all()
print(f"Found {len(organizations)} organizations")
print(f"First organization: {organizations[0].name}")

# Get product folders
folders, meta = client.product_folders.find_all()
print(f"Found {len(folders)} product folders")

if folders:
    folder_id = folders[0].id

    # Get products in a specific folder
    query = client.products.query()
    query.filter().eq("pathName", f"{folders[4].name}")
    # query.filter().eq("archived", False)
    query.limit(10)

    products, meta = client.products.find_all(query)
    print(f"Found {len(products)} products in folder '{folders[0].name}'")

    for product in products:
        print(f"- {product.name} (Code: {product.code})")

        # Get stock for this product
        try:
            stock = client.products.get_stock(product.id)
            print(f"  Stock: {stock}")
        except Exception as e:
            print(f"  Error getting stock: {e}")

# Create a new counterparty
new_counterparty = Counterparty(
    meta=Meta.create_default(),
    name="Example Company",
    companyType="legal",
    inn="1234567890",
    email="info@example.com",
    phone="+7 999 123-45-67"
)

try:
    created_counterparty = client.counterparties.create(new_counterparty)
    print(f"Created counterparty: {created_counterparty.name} (ID: {created_counterparty.id})")

    # Update the counterparty
    created_counterparty.description = "Added via API"
    updated_counterparty = client.counterparties.update(created_counterparty)
    print(f"Updated counterparty description: {updated_counterparty.description}")

    # Delete the counterparty
    client.counterparties.delete(created_counterparty.id)
    print(f"Deleted counterparty: {created_counterparty.name}")

    # Try to find the deleted counterparty
    try:
        client.counterparties.find_by_id(created_counterparty.id)
    except NotFoundException:
        print("Counterparty was successfully deleted")

except Exception as e:
    print(f"Error working with counterparty: {e}")

# Search for products
search_results = client.search("example product")
print(f"Search results: {search_results}")

# Get audit
audit = client.get_audit({"limit": 10})
print(f"Recent audit events: {audit}")