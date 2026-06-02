from faker import Faker
import pandas as pd
import random
from tqdm import tqdm

fake = Faker('en_IN')

# ======================
# RECORD COUNTS
# ======================

NUM_USERS = 100000
NUM_CUSTOMERS = 100000
NUM_SELLERS = 100000
NUM_ADDRESSES = 100000

NUM_CATEGORIES = 100000
NUM_BRANDS = 100000
NUM_PRODUCTS = 100000
NUM_PRODUCT_CATEGORIES = 100000
NUM_PRODUCT_IMAGES = 100000

NUM_WAREHOUSES = 100
NUM_INVENTORY = 100000
NUM_STOCK_MOVEMENTS = 100000

NUM_CART = 100000
NUM_CART_ITEMS = 100000

NUM_ORDERS = 10000000   # 1 CRORE
NUM_ORDER_ITEMS = 1000000

NUM_PAYMENTS = 100000
NUM_PAYMENT_TRANSACTIONS = 100000
NUM_INVOICES = 100000

NUM_COUPONS = 10000
NUM_COUPON_USAGE = 100000

NUM_REVIEWS = 100000
NUM_RATINGS = 100000

NUM_RETURNS = 100000
NUM_REFUNDS = 100000


# ======================
# USERS TABLE
# ======================

print("Generating users...")

users = []

for i in tqdm(range(1, NUM_USERS + 1)):
    role = random.choice([
        'customer',
        'seller'
    ])

    users.append({
        'user_id': i,
        'full_name': fake.name(),
        'email': f"user{i}@gmail.com",
        'password_hash':
            fake.sha256(),
        'role': role,
        'created_at':
            fake.date_time_this_decade()
    })

users_df = pd.DataFrame(users)

users_df.to_csv(
    'seed_data/users.csv',
    index=False
)

print("users.csv created")


# ======================
# PRODUCTS TABLE
# ======================

print("Generating products...")

product_names = [
    "iPhone",
    "Laptop",
    "Shoes",
    "Watch",
    "Headphones",
    "Bag",
    "T-shirt",
    "Keyboard",
    "Monitor",
    "Mouse"
]

products = []

for i in tqdm(
    range(1, NUM_PRODUCTS + 1)
):

    products.append({
        'product_id': i,
        'seller_id': random.randint(1, NUM_SELLERS),
        'brand_id': random.randint(1, NUM_BRANDS),
        'product_name':
            random.choice(
                product_names
            ),
        'sku': f"SKU{i}",
        'slug':
            f"product-{i}",
        'base_price':
            round(
                random.uniform(
                    100,
                    100000
                ),
                2
            ),
        'product_status':
            random.choice([
                'active',
                'inactive'
            ]),
        'created_at':
            fake.date_time_this_decade()
    })

products_df = pd.DataFrame(
    products
)

products_df.to_csv(
    'seed_data/products.csv',
    index=False
)

print("products.csv created")


# ======================
# ORDERS TABLE
# SAFE FOR 1 CRORE
# ======================

print(
    "Generating 1 crore orders..."
)

CHUNK_SIZE = 100000

order_status = [
    'pending',
    'confirmed',
    'shipped',
    'delivered',
    'cancelled'
]

first_chunk = True

for start in range(
    1,
    NUM_ORDERS + 1,
    CHUNK_SIZE
):

    orders = []

    end = min(
        start + CHUNK_SIZE,
        NUM_ORDERS + 1
    )

    print(
        f"Generating rows "
        f"{start} to "
        f"{end - 1}"
    )

    for i in tqdm(
        range(start, end)
    ):

        orders.append({
            'order_id': i,
            'customer_id':
                random.randint(
                    1,
                    NUM_USERS
                ),
            'order_status':
                random.choice(
                    order_status
                ),
            'total_amount':
                round(
                    random.uniform(
                        100,
                        50000
                    ),
                    2
                ),
            'created_at':
                fake.date_time_this_decade()
        })

    orders_df = pd.DataFrame(
        orders
    )

    orders_df.to_csv(
        'seed_data/orders.csv',
        mode='a',
        header=first_chunk,
        index=False
    )

    first_chunk = False

print("orders.csv created")


# ======================
# PAYMENTS TABLE
# ======================

print(
    "Generating payments..."
)

payment_methods = [
    'UPI',
    'Credit Card',
    'Debit Card',
    'Net Banking',
    'Wallet',
    'COD'
]

payment_status = [
    'success',
    'failed',
    'pending'
]

payments = []

for i in tqdm(
    range(
        1,
        NUM_PAYMENTS + 1
    )
):

    payments.append({
    'payment_id': i,
    'order_id': random.randint(1, NUM_ORDERS),
    'payment_method': random.choice(payment_methods),
    'payment_status': random.choice(payment_status),
    'gateway_reference': fake.uuid4(),
    'amount': round(random.uniform(100, 50000), 2),
    'paid_at': fake.date_time_this_decade()
})

payments_df = pd.DataFrame(
    payments
)

payments_df.to_csv(
    'seed_data/payments.csv',
    index=False
)

print(
    "payments.csv created"
)

print(
    "ALL CSV FILES GENERATED SUCCESSFULLY"
)