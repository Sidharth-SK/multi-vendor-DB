from faker import Faker
import pandas as pd
import random
from tqdm import tqdm
import os

fake = Faker('en_IN')

os.makedirs('seed_data', exist_ok=True)

# ======================
# RECORD COUNTS
# ======================

NUM_USERS                = 100000
NUM_CUSTOMERS            = 100000
NUM_SELLERS              = 100000
NUM_ADDRESSES            = 100000

NUM_CATEGORIES           = 100000
NUM_BRANDS               = 100000
NUM_PRODUCTS             = 100000
NUM_PRODUCT_CATEGORIES   = 100000
NUM_PRODUCT_IMAGES       = 100000

NUM_WAREHOUSES           = 100
NUM_INVENTORY            = 100000
NUM_STOCK_MOVEMENTS      = 100000

NUM_CART                 = 100000
NUM_CART_ITEMS           = 100000

NUM_ORDERS               = 10000000  
NUM_ORDER_ITEMS          = 1000000

NUM_PAYMENTS             = 100000    
NUM_PAYMENT_TRANSACTIONS = 100000
NUM_INVOICES             = 100000

NUM_COUPONS              = 10000
NUM_COUPON_USAGE         = 100000

NUM_REVIEWS              = 100000
NUM_RATINGS              = 100000

NUM_RETURNS              = 100000
NUM_REFUNDS              = 100000

# ================================================
# SKIPPED (already generated):
#   users.csv
#   products.csv
#   orders.csv
#   payments.csv
# ================================================


# ======================
# 1. CUSTOMER PROFILES
# ======================

print("Generating customer_profiles...")

customer_profiles = []

for i in tqdm(range(1, NUM_CUSTOMERS + 1)):
    customer_profiles.append({
        'customer_id': i,
        'user_id': i,
        'loyalty_points': random.randint(0, 5000),
        'preferred_address': fake.address().replace('\n', ', '),
        'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=70)
    })

pd.DataFrame(customer_profiles).to_csv(
    'seed_data/customer_profiles.csv',
    index=False
)
print("customer_profiles.csv created")


# ======================
# 2. SELLER PROFILES
# ======================

# ======================
# 2. SELLER PROFILES
# ======================

print("Generating seller_profiles...")

seller_user_ids = random.sample(
    range(1, NUM_USERS + 1),
    NUM_SELLERS
)

seller_profiles = []

for i in tqdm(range(1, NUM_SELLERS + 1)):
    seller_profiles.append({
        'seller_id': i,  # UNIQUE
        'user_id': seller_user_ids[i - 1],  # UNIQUE
        'business_name': fake.company(),
        'gst_number': f"GST{i:010d}",
        'commission_rate': round(random.uniform(5.0, 20.0), 2),
        'verification_status': random.choice([True, False])
    })

pd.DataFrame(seller_profiles).to_csv(
    'seed_data/seller_profiles.csv',
    index=False
)

print("seller_profiles.csv created")


# ======================
# 3. ADDRESSES
# ======================

print("Generating addresses...")

addresses = []

for i in tqdm(range(1, NUM_ADDRESSES + 1)):
    addresses.append({
        'address_id': i,
        'user_id': random.randint(1, NUM_USERS),
        'address_line': fake.street_address(),
        'city': fake.city(),
        'state': fake.state(),
        'country': 'India',
        'postal_code': fake.postcode(),
        'address_type': random.choice(['home', 'work', 'other'])
    })

pd.DataFrame(addresses).to_csv(
    'seed_data/addresses.csv',
    index=False
)
print("addresses.csv created")


# ======================
# 4. CATEGORIES
# ======================

print("Generating categories...")

root_categories = [
    'Electronics', 'Fashion', 'Home & Kitchen',
    'Books', 'Toys', 'Sports', 'Grocery',
    'Beauty', 'Automotive', 'Health'
]

categories = []

for i, name in enumerate(root_categories, start=1):
    categories.append({
        'category_id': i,
        'category_name': name,
        'parent_category_id': None
    })

for i in tqdm(range(11, NUM_CATEGORIES + 1)):
    categories.append({
        'category_id': i,
        'category_name': fake.word().capitalize() + ' ' + fake.word().capitalize(),
        'parent_category_id': random.randint(1, 10)
    })

df = pd.DataFrame(categories)

df["parent_category_id"] = (
    df["parent_category_id"]
      .astype("Int64")
)

df.to_csv(
    "seed_data/categories.csv",
    index=False
)
print("categories.csv created")


# ======================
# 5. BRANDS
# ======================

print("Generating brands...")

brands = []

for i in tqdm(range(1, NUM_BRANDS + 1)):
    brands.append({
        'brand_id':  i,
        'brand_name': f"{fake.company()} Brand {i}",
        'is_verified': random.choice([True, False])
    })

pd.DataFrame(brands).to_csv(
    'seed_data/brands.csv',
    index=False
)
print("brands.csv created")


# ======================
# 6. PRODUCT CATEGORIES
# ======================

print("Generating product_categories...")

product_categories = []
seen_pc = set()

i = 0
with tqdm(total=NUM_PRODUCT_CATEGORIES) as pbar:
    while i < NUM_PRODUCT_CATEGORIES:
        pid = random.randint(1, NUM_PRODUCTS)
        cid = random.randint(1, NUM_CATEGORIES)
        key = (pid, cid)
        if key not in seen_pc:
            seen_pc.add(key)
            product_categories.append({
                'product_id': pid,
                'category_id': cid
            })
            i += 1
            pbar.update(1)

pd.DataFrame(product_categories).to_csv(
    'seed_data/product_categories.csv',
    index=False
)
print("product_categories.csv created")


# ======================
# 7. PRODUCT IMAGES
# ======================

print("Generating product_images...")

product_images = []

for i in tqdm(range(1, NUM_PRODUCT_IMAGES + 1)):
    product_images.append({
        'image_id': i,
        'product_id': random.randint(1, NUM_PRODUCTS),
        'image_url': f"https://cdn.example.com/products/img_{i}.jpg",
        'sort_order': random.randint(1, 5),
        'is_primary': random.choice([True, False])
    })

pd.DataFrame(product_images).to_csv(
    'seed_data/product_images.csv',
    index=False
)
print("product_images.csv created")


# ======================
# 8. WAREHOUSES
# ======================

print("Generating warehouses...")

indian_cities = [
    'Mumbai', 'Delhi', 'Bengaluru', 'Hyderabad', 'Chennai',
    'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow',
    'Surat', 'Kochi', 'Bhopal', 'Indore', 'Nagpur'
]

indian_states = [
    'Maharashtra', 'Delhi', 'Karnataka', 'Telangana', 'Tamil Nadu',
    'West Bengal', 'Maharashtra', 'Gujarat', 'Rajasthan', 'Uttar Pradesh',
    'Gujarat', 'Kerala', 'Madhya Pradesh', 'Madhya Pradesh', 'Maharashtra'
]

warehouses = []

for i in tqdm(range(1, NUM_WAREHOUSES + 1)):
    idx = (i - 1) % len(indian_cities)
    warehouses.append({
        'warehouse_id': i,
        'warehouse_name': f"Warehouse {i} - {indian_cities[idx]}",
        'city': indian_cities[idx],
        'state': indian_states[idx],
        'capacity': random.randint(1000, 50000)
    })

pd.DataFrame(warehouses).to_csv(
    'seed_data/warehouses.csv',
    index=False
)
print("warehouses.csv created")


# ======================
# 9. INVENTORY
# ======================

print("Generating inventory...")

inventory = []

for i in tqdm(range(1, NUM_INVENTORY + 1)):
    inventory.append({
        'inventory_id': i,
        'product_id': random.randint(1, NUM_PRODUCTS),
        'warehouse_id': random.randint(1, NUM_WAREHOUSES),
        'quantity_available': random.randint(0, 10000),
        'reorder_threshold': random.randint(5, 100)
    })

pd.DataFrame(inventory).to_csv(
    'seed_data/inventory.csv',
    index=False
)
print("inventory.csv created")


# ======================
# 10. STOCK MOVEMENTS
# ======================
# ======================
# 10. STOCK MOVEMENTS
# ======================

print("Generating stock_movements...")

stock_movements = []

for i in tqdm(range(1, NUM_STOCK_MOVEMENTS + 1)):
    stock_movements.append({
        'movement_id': i,
        'product_id': random.randint(1, NUM_PRODUCTS),  # FIXED
        'warehouse_id': random.randint(1, NUM_WAREHOUSES),
        'movement_type': random.choice([
            'inbound',
            'outbound',
            'return',
            'adjustment'
        ]),
        'quantity': random.randint(1, 500),
        'movement_date': fake.date_time_this_decade()
    })

pd.DataFrame(stock_movements).to_csv(
    'seed_data/stock_movements.csv',
    index=False
)

print("stock_movements.csv created")

# ======================
# 11. CART
# ======================

print("Generating cart...")

cart = []

for i in tqdm(range(1, NUM_CART + 1)):
    cart.append({
        'cart_id': i,
        'customer_id': i,
        'expires_at': fake.future_datetime()
    })

pd.DataFrame(cart).to_csv(
    'seed_data/cart.csv',
    index=False
)
print("cart.csv created")


# ======================
# 12. CART ITEMS
# ======================

print("Generating cart_items...")

cart_items = []

for i in tqdm(range(1, NUM_CART_ITEMS + 1)):
    cart_items.append({
        'cart_item_id': i,
        'cart_id': random.randint(1, NUM_CART),
        'product_id': random.randint(1, NUM_PRODUCTS),
        'quantity': random.randint(1, 10)
    })

pd.DataFrame(cart_items).to_csv(
    'seed_data/cart_items.csv',
    index=False
)
print("cart_items.csv created")


# ======================
# 13. ORDER ITEMS
# ======================

# ======================
# 13. ORDER ITEMS
# ======================

print("Generating order_items...")

CHUNK_SIZE = 100000
first_chunk = True

for start in range(1, NUM_ORDER_ITEMS + 1, CHUNK_SIZE):
    end = min(start + CHUNK_SIZE, NUM_ORDER_ITEMS + 1)

    print(f"Rows {start} to {end - 1}")

    batch = []

    for i in tqdm(range(start, end)):
        batch.append({
            'order_item_id': i,
            'order_id': random.randint(1, NUM_ORDERS),  # FIXED
            'product_id': random.randint(1, NUM_PRODUCTS),
            'quantity': random.randint(1, 5),
            'unit_price': round(random.uniform(100, 50000), 2)
        })

    pd.DataFrame(batch).to_csv(
        'seed_data/order_items.csv',
        mode='a',
        header=first_chunk,
        index=False
    )

    first_chunk = False

print("order_items.csv created")




# ======================
# 14. PAYMENT TRANSACTIONS
# ======================

print("Generating payment_transactions...")

payment_transactions = []

for i in tqdm(range(1, NUM_PAYMENT_TRANSACTIONS + 1)):
    payment_transactions.append({
        'transaction_id': i,
        'payment_id': random.randint(1, 100000),  # FIXED
        'transaction_status': random.choice([
            'success', 'failed', 'pending', 'reversed'
        ]),
        'transaction_date': fake.date_time_this_decade()
    })

pd.DataFrame(payment_transactions).to_csv(
    'seed_data/payment_transactions.csv',
    index=False
)

print("payment_transactions.csv created")



# ======================
# 15. INVOICES
# ======================

print("Generating invoices...")

invoices = []

for i in tqdm(range(1, NUM_INVOICES + 1)):
    invoices.append({
        'invoice_id': i,
        'order_id': random.randint(1, 100000),  # FIXED
        'invoice_date': fake.date_time_this_decade(),
        'total_amount': round(random.uniform(100, 50000), 2)
    })

pd.DataFrame(invoices).to_csv(
    'seed_data/invoices.csv',
    index=False
)

print("invoices.csv created")

# ======================
# 16. COUPONS
# ======================

print("Generating coupons...")

coupons = []

for i in tqdm(range(1, NUM_COUPONS + 1)):
    dtype = random.choice(['flat', 'percentage'])
    coupons.append({
        'coupon_id': i,
        'coupon_code': f"COUP{i:06d}",
        'discount_type': dtype,
        'discount_value': (
            round(random.uniform(10, 500), 2)
            if dtype == 'flat'
            else round(random.uniform(5, 50), 2)
        ),
        'max_uses': random.randint(50, 10000),
        'expiry_date': fake.future_date(),
        'minimum_order_value': round(random.uniform(200, 5000), 2)
    })

pd.DataFrame(coupons).to_csv(
    'seed_data/coupons.csv',
    index=False
)
print("coupons.csv created")


# ======================
# 17. COUPON USAGE
# ======================

print("Generating coupon_usage...")

coupon_usage = []

for i in tqdm(range(1, NUM_COUPON_USAGE + 1)):
    coupon_usage.append({
        'usage_id': i,
        'coupon_id': random.randint(1, NUM_COUPONS),
        'customer_id': random.randint(1, NUM_CUSTOMERS),
        'used_at': fake.date_time_this_decade()
    })

pd.DataFrame(coupon_usage).to_csv(
    'seed_data/coupon_usage.csv',
    index=False
)
print("coupon_usage.csv created")


# ======================
# 18. REVIEWS
# ======================

review_titles = [
    "Good Product",
    "Excellent Quality",
    "Worth the Price",
    "Average Product",
    "Highly Recommended"
]

review_texts = [
    "Very good product. Quality is excellent.",
    "Worth buying. Value for money.",
    "Average product but works fine.",
    "Excellent quality and fast delivery.",
    "Not bad for the price.",
    "Highly recommended product.",
    "Satisfied with the purchase.",
    "Good product and nice packaging."
]

reviews = []

for i in range(1, 100001):
    reviews.append({
        'review_id': i,
        'customer_id': random.randint(1, 100000),
        'product_id': random.randint(1, NUM_PRODUCTS),
        'title': random.choice(review_titles),
        'review_body': random.choice(review_texts),
        'verified_purchase': random.choice([True, False]),
        'helpful_votes': random.randint(0, 500)
    })

pd.DataFrame(reviews).to_csv(
    'seed_data/reviews.csv',
    index=False
)

print("reviews.csv created")

# ======================
# RATINGS
# ======================

print("Generating ratings...")

ratings = []

for i in tqdm(range(1, NUM_RATINGS + 1)):
    ratings.append({
        'rating_id': i,
        'customer_id': random.randint(1, NUM_CUSTOMERS),
        'product_id': random.randint(1, NUM_PRODUCTS),
        'rating_value': random.randint(1, 5),
        'moderation_status': random.choice([
            'approved',
            'pending',
            'rejected'
        ])
    })

pd.DataFrame(ratings).to_csv(
    'seed_data/ratings.csv',
    index=False
)

print("ratings.csv created")

# ======================
# 20. RETURNS
# ======================

print("Generating returns...")

returns = []

for i in tqdm(range(1, NUM_RETURNS + 1)):
    returns.append({
        'return_id': i,
        'order_item_id': random.randint(1, 1000000),  # FIXED
        'reason_code': random.choice([
            'defective_product',
            'wrong_item_delivered',
            'not_as_described',
            'changed_mind',
            'damaged_in_transit',
            'size_issue'
        ]),
        'item_condition': random.choice([
            'unopened',
            'opened',
            'damaged',
            'used'
        ]),
        'returned_at': fake.date_time_this_decade()
    })

pd.DataFrame(returns).to_csv(
    'seed_data/returns.csv',
    index=False
)

print("returns.csv created")


# ======================
# 21. REFUNDS
# ======================

print("Generating refunds...")

refunds = []

for i in tqdm(range(1, NUM_REFUNDS + 1)):
    refunds.append({
        'refund_id': i,
        'return_id': i,
        'refund_amount': round(random.uniform(50, 50000), 2),
        'refund_method': random.choice([
            'original_payment_method', 'wallet_credit',
            'bank_transfer', 'UPI'
        ]),
        'processed_at': fake.date_time_this_decade()
    })

pd.DataFrame(refunds).to_csv(
    'seed_data/refunds.csv',
    index=False
)
print("refunds.csv created")


# ======================
# DONE
# ======================

print("\n ALL 21 CSV FILES GENERATED SUCCESSFULLY")
print("\nFiles created in seed_data/:")
new_files = [
    "customer_profiles", "seller_profiles", "addresses",
    "categories", "brands", "product_categories", "product_images",
    "warehouses", "inventory", "stock_movements",
    "cart", "cart_items", "order_items",
    "payment_transactions", "invoices",
    "coupons", "coupon_usage",
    "reviews", "ratings",
    "returns", "refunds"
]
for f in new_files:
    print(f"  -> seed_data/{f}.csv")

print("\nSKIPPED (already exist):")
for f in ["users", "products", "orders", "payments"]:
    print(f"  -- seed_data/{f}.csv  (not touched)")