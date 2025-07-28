"""
Example of working with the Assortment entity in MoySklad API.
"""

import sys
import os

from moysklad_api import MoySklad
from moysklad_api.entities.base import Meta
from moysklad_api.entities.assortment import Assortment, Service, Bundle
from decimal import Decimal

from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("MOYSKLAD_TOKEN")

# Initialize the client
client = MoySklad(
    token=token,
    debug=True
)

# Get assortment items with various filters
print("Fetching assortment items...")

# Build a query to get non-archived items
query = client.assortment.query()
query.filter().eq("archived", False)

items_form_all_pages = client.assortment.fetch_all(query)
items, meta = client.assortment.find_all(query)
print(f"Found {meta.size} total items, showing first {len(items)}")

for item in items:
    print(f"- {item.name} (Type: {item.productType}, ID: {item.id})")

# Search for specific items
search_term = "test"
search_results, _ = client.assortment.search_by_name(search_term)
print(f"\nSearch results for '{search_term}': {len(search_results)} items")
for item in search_results[:5]:  # Show first 5 only
    print(f"- {item.name} (Type: {item.productType})")

# Get items by type
products, _ = client.assortment.get_products()
print(f"\nProducts: {len(products)} items")

services, _ = client.assortment.get_services()
print(f"Services: {len(services)} items")

bundles, _ = client.assortment.get_bundles()
print(f"Bundles: {len(bundles)} items")

variants, _ = client.assortment.get_variants()
print(f"Variants: {len(variants)} items")

# Get items by barcode
barcode = "123456789"
barcode_items = client.assortment.get_by_barcode(barcode)
print(f"\nItems with barcode '{barcode}': {len(barcode_items)} items")

# Find items in a specific folder
if client.product_folders.find_all()[0]:
    folder = client.product_folders.find_all()[0][4]
    folder_items, _ = client.assortment.get_by_product_folder(folder.meta.href, with_subfolders=True)
    print(f"\nItems in folder '{folder.name}': {len(folder_items)} items")

# Create a new service
print("\nCreating a new service...")

default_currency = client.currencies.get_default()

default_price_type = client.price_types.get_default()

new_service = Service(
    meta=Meta.create_default(),
    name="Consulting Service",
    # code="",
    description="Professional consulting services",
    vat=20,
    discountProhibited=False,
    salePrices=[
        {
            "value": 10000,
            "currency": default_currency,
            "priceType": default_price_type,
        }
    ]
)

try:
    created_service = client.services.create(new_service)
    print(f"Created service: {created_service.name} (ID: {created_service.id})")

    # Update the service
    created_service.description += " (Updated)"
    updated_service = client.services.update(created_service)
    print(f"Updated service description: {updated_service.description}")

    # Delete the service
    client.services.delete(created_service.id)
    print(f"Deleted service: {created_service.name}")

except Exception as e:
    print(f"Error working with service: {e}")

# Create a bundle if we have products
try:
    if products:
        print("\nCreating a new bundle...")
        # Use first two products for the bundle
        components = []
        for i, product in enumerate(products[:2]):
            components.append({
                "assortment": {
                    "meta": product.meta
                },
                "quantity": i + 1
            })

        new_bundle = Bundle(
            meta=Meta.create_default(),
            name="Product Bundle",
            # code="BD001",
            description="Bundle of products",
            vat=20,
            components=components,
            salePrices=[
                {
                    "value": 15000,
                    "currency": default_currency,
                    "priceType": default_price_type,
                }
            ]
        )

        created_bundle = client.bundles.create(new_bundle)
        print(f"Created bundle: {created_bundle.name} (ID: {created_bundle.id})")

        # Get bundle components
        components = client.bundles.get_components(created_bundle.id)
        print(f"Bundle has {len(components)} components")

        # Delete the bundle
        client.bundles.delete(created_bundle.id)
        print(f"Deleted bundle: {created_bundle.name}")
except Exception as e:
    print(f"Error working with bundle: {e}")

# Get assortment settings
try:
    settings = client.assortment.get_settings()
    print("\nAssortment settings:")
    print(f"- Settings meta: {settings.meta} ")
except Exception as e:
    print(f"Error getting assortment settings: {e}")

print("\nAssortment example completed.")