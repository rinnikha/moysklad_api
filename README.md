# MoySklad API Client

A comprehensive Python client for the MoySklad JSON API v1.2.

## Installation

```bash
pip install r-moysklad-api
```

## Basic Usage

```python
from moysklad_api import MoySklad

# Initialize the client
client = MoySklad(
    login="your_login",
    password="your_password",
    debug=True  # Enable debug logging
)

# Get all products, filtered and sorted
query = client.products.query()
query.filter().eq("archived", False)
query.order_by().add("name")
query.limit(10)
query.expand("owner", "group")

products, meta = client.products.find_all(query)
for product in products:
    print(f"Product: {product.name}, ID: {product.id}")

# Create a new product
from moysklad_api.entities.products import Product
from moysklad_api.entities.base import Meta

new_product = Product(
    meta=Meta.create_default(),
    name="Test Product",
    code="TP001",
    description="A test product created via API"
)
created_product = client.products.create(new_product)
print(f"Created product with ID: {created_product.id}")

# Find a specific product
product = client.products.find_by_id(created_product.id)
print(f"Found product: {product.name}")

# Update the product
product.description = "Updated description"
updated_product = client.products.update(product)
print(f"Updated product: {updated_product.description}")

# Delete the product
client.products.delete(product.id)
print(f"Deleted product with ID: {product.id}")
```

## Repository Pattern

Each entity type has its own repository with specialized methods:

```python
# Find counterparties by phone number
counterparties = client.counterparties.get_by_phone("+7 999 123-45-67")

# Get invoices for a customer order
invoices = client.invoices.get_by_customer_order(order_id)

# Add a contact person to a counterparty
from moysklad_api.entities.counterparty import ContactPerson
from moysklad_api.entities.base import Meta

contact = ContactPerson(
    meta=Meta.create_default(),
    name="John Doe",
    email="john@example.com",
    phone="+7 999 123-45-67"
)
client.counterparties.add_contact_person(counterparty_id, contact)
```

## Advanced Queries

```python
# Find products in a specific folder with price range
query = client.products.query()

# Filter by folder
query.filter().eq("productFolder.id", folder_id)

# Filter by price (between 100 and 1000)
query.filter().gte("salePrices.value", 100)
query.filter().lte("salePrices.value", 1000)

# Search by keyword
query.search("premium")

# Sort by name descending
query.order_by().add("name", "desc")

# Paginate results
query.limit(20).offset(40)

# Expand related entities
query.expand("owner", "group", "images")

# Execute the query
products, meta = client.products.find_all(query)
```

## Bulk Operations

```python
# Create multiple products at once
products_to_create = [
    Product(meta=Meta.create_default(), name="Product 1"),
    Product(meta=Meta.create_default(), name="Product 2"),
    Product(meta=Meta.create_default(), name="Product 3")
]
created_products = client.products.create_bulk(products_to_create)

# Update multiple products at once
products[0].description = "Updated description 1"
products[1].description = "Updated description 2"
updated_products = client.products.update_bulk(products)

# Delete multiple products at once
product_ids = [p.id for p in products]
client.products.delete_bulk(product_ids)
```

## Error Handling

```python
from moysklad_api.exceptions import (
    MoySkladException,
    AuthenticationException,
    NotFoundException,
    ValidationException,
    RateLimitException
)

try:
    product = client.products.find_by_id("non-existent-id")
except NotFoundException:
    print("Product not found")
except ValidationException as e:
    print(f"Validation error: {e.error_message}")
except RateLimitException as e:
    print(f"Rate limit exceeded. Retry after {e.retry_after} seconds")
except AuthenticationException:
    print("Authentication failed")
except MoySkladException as e:
    print(f"API error: {e.status_code} - {e.error_message}")
```

## Custom Repositories

```python
from moysklad_api.entities.base import MetaEntity, Meta
from dataclasses import dataclass

# Define a custom entity
@dataclass
class CustomEntity(MetaEntity):
    entity_name: ClassVar[str] = "entity/customentity/your_custom_entity"
    # Add your custom fields here
    custom_field: Optional[str] = None

# Create a repository for the custom entity
custom_repo = client.create_repository("entity/customentity/your_custom_entity", CustomEntity)

# Use the repository
custom_entities, meta = custom_repo.find_all()
```