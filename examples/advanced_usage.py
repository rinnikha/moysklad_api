"""
Advanced usage example for the MoySklad API client.
"""

from moysklad_api import MoySklad
from moysklad_api.entities.documents import (
    CustomerOrder,
    Position,
    InvoiceOut,
    PaymentIn,
)
from moysklad_api.entities.base import Meta
from moysklad_api.entities.counterparty import Counterparty, ContactPerson
from moysklad_api.entities.products import Product

from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("MOYSKLAD_TOKEN")

# Initialize the client
client = MoySklad(
    token=token,
    debug=True,
)

report_url = "https://api.moysklad.ru/api/remap/1.2/report/stock/bystore/current?changedSince=2025-08-17 04:20:00"
stock = client.stock_report.get_stock_from_webhook_report(report_url)


client.product_folders.create_bulk()

# Create new counterparty
default_price_type = client.price_types.get_default()

new_counterparty = Counterparty(
    meta=Meta.create_default(),
    name="New Counterparty1",
    description="New Counterparty1 description",
    phone="+123456442",
    priceType=default_price_type,
)


counterparty = client.counterparties.create(new_counterparty)
print(f"Created new counterparty: {counterparty.name}")

# Get or create a contact person
contact_persons = client.counterparties.get_contact_persons(counterparty.id)
if contact_persons:
    contact_person = contact_persons[0]
    print(f"Using existing contact person: {contact_person.name}")
else:
    # Create a new contact person
    new_contact = ContactPerson(
        # meta=Meta.create_default(),
        name="John Doe",
        email="john@example.com",
        phone="+7 999 123-45-67",
    )
    contact_person = client.counterparties.add_contact_person(
        counterparty.id, new_contact
    )
    print(f"Created new contact person: {contact_person.name}")

# Find products to add to order
query = client.assortment.query()
query.filter().eq("archived", False)
query.limit(2)

products, _ = client.assortment.find_all(query)
if not products:
    print("No products found")
    exit()

print(f"Found products: {', '.join(p.name for p in products)}")

# Get the default organization
organizations, _ = client.organizations.find_all()
if not organizations:
    print("No organizations found")
    exit()

organization = organizations[0]

# Get the default store
stores, _ = client.stores.find_all()
if not stores:
    print("No stores found")
    exit()

store = stores[0]

# Create a new customer order
new_order = CustomerOrder(
    # meta=Meta.create_default(),
    # name="Order from API",
    organization={"meta": organization.meta},
    agent={"meta": counterparty.meta},
    store={"meta": store.meta},
)

created_order = client.customer_orders.create(new_order)
print(f"Created order: {created_order.name} (ID: {created_order.id})")

# Add positions to the order
for i, product in enumerate(products):
    new_position = Position(
        assortment={"meta": product.meta}, discount=0, quantity=2, vat=20, price=100
    )

    created_position = client.customer_orders.create_position(
        created_order.id, new_position
    )
    print(f"Added position: {product.name} (Quantity: 1)")

# Reload the order to see positions
updated_order = client.customer_orders.find_by_id(created_order.id)
positions, _ = client.customer_orders.get_positions(created_order.id)

print(f"Order now has {len(positions)} positions")

new_invoice = InvoiceOut(
    organization={"meta": organization.meta},
    agent={"meta": counterparty.meta},
    customerOrder={"meta": created_order.meta},
    sum=created_order.sum,
)

created_invoice = client.invoiceouts.create(new_invoice)
print(f"Created invoice: {created_invoice.name} (ID: {created_invoice.id})")

# Reload customer order after linking invoice
query = client.customer_orders.query()
query.expand("invoicesOut")
created_order = client.customer_orders.find_by_id(created_order.id, query)

# Get all invoices for this order
order_invoices = created_order.invoicesOut
print(f"Order has {len(order_invoices)} invoices")

# Create a payment for the invoice
new_payment = PaymentIn(
    organization={"meta": organization.meta},
    agent={"meta": counterparty.meta},
    operations=[{"meta": created_invoice.meta, "linked_sum": created_invoice.sum}],
    sum=sum(float(p.price) * float(p.quantity) for p in positions),
)

created_payment = client.payment_ins.create(new_payment)
print(f"Created payment: {created_payment.name} (ID: {created_payment.id})")

client.payment_ins.delete(created_payment.id)
print(f"Deleted payment: {created_payment.name}")

client.invoiceouts.delete(created_invoice.id)
print(f"Deleted invoice: {created_invoice.name}")

client.customer_orders.delete(created_order.id)
print(f"Deleted order: {created_order.name}")

client.counterparties.delete(counterparty.id)
print(f"Deleted counterparty: {counterparty.id}s")

print("Advanced example completed successfully!")
