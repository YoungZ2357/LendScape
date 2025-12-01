import random
import hashlib
from faker import Faker
from faker.providers import BaseProvider
from sqlalchemy import create_engine, text

fake = Faker()

# ============================================
# SUPABASE CONFIG - FILL THESE IN!
# ============================================
SUPABASE_USER = "postgres.your_project_ref"    
SUPABASE_PASSWORD = "your_password_here"          
SUPABASE_HOST = "db.xxxxx.supabase.co"           
SUPABASE_PORT = "5432"                           
SUPABASE_DBNAME = "postgres"                      
# ============================================
# CONFIGURATION
# ============================================

BOSTON_NEIGHBORHOODS = {
    'Back Bay': {
        'streets': [
            {'name': 'Newbury Street', 'range': (1, 400)},
            {'name': 'Boylston Street', 'range': (600, 900)},
            {'name': 'Commonwealth Avenue', 'range': (1, 400)},
            {'name': 'Beacon Street', 'range': (1, 500)},
            {'name': 'Marlborough Street', 'range': (1, 400)}
        ],
        'zip': '02116',
        'coords': (42.3505, -71.0820)
    },
    'South End': {
        'streets': [
            {'name': 'Tremont Street', 'range': (500, 1200)},
            {'name': 'Washington Street', 'range': (1700, 2300)},
            {'name': 'Columbus Avenue', 'range': (1, 600)},
            {'name': 'Shawmut Avenue', 'range': (1, 700)}
        ],
        'zip': '02118',
        'coords': (42.3418, -71.0695)
    },
    'Fenway': {
        'streets': [
            {'name': 'Boylston Street', 'range': (1200, 1400)},
            {'name': 'Park Drive', 'range': (1, 200)},
            {'name': 'Fenway', 'range': (1, 100)},
            {'name': 'Peterborough Street', 'range': (1, 200)}
        ],
        'zip': '02215',
        'coords': (42.3450, -71.0960)
    },
    'Beacon Hill': {
        'streets': [
            {'name': 'Charles Street', 'range': (1, 200)},
            {'name': 'Mount Vernon Street', 'range': (1, 100)},
            {'name': 'Pinckney Street', 'range': (1, 100)}
        ],
        'zip': '02114',
        'coords': (42.3590, -71.0660)
    },
    'Cambridge': {
        'streets': [
            {'name': 'Massachusetts Avenue', 'range': (1300, 1600)},
            {'name': 'Brattle Street', 'range': (1, 200)},
            {'name': 'Garden Street', 'range': (1, 200)}
        ],
        'zip': '02138',
        'coords': (42.3745, -71.1200)
    },
    'Allston': {
        'streets': [
            {'name': 'Commonwealth Avenue', 'range': (900, 1400)},
            {'name': 'Brighton Avenue', 'range': (1, 400)},
            {'name': 'Harvard Avenue', 'range': (1, 300)}
        ],
        'zip': '02134',
        'coords': (42.3520, -71.1285)
    },
    'Jamaica Plain': {
        'streets': [
            {'name': 'Centre Street', 'range': (600, 800)},
            {'name': 'South Street', 'range': (1, 300)},
            {'name': 'Pond Street', 'range': (1, 200)}
        ],
        'zip': '02130',
        'coords': (42.3120, -71.1100)
    },
    'North End': {
        'streets': [
            {'name': 'Hanover Street', 'range': (200, 400)},
            {'name': 'Salem Street', 'range': (1, 200)},
            {'name': 'Prince Street', 'range': (1, 100)}
        ],
        'zip': '02113',
        'coords': (42.3650, -71.0540)
    }
}

ITEM_CATALOG = {
    'Tools': [
        ('DeWalt Drill', 25),
        ('Makita Circular Saw', 35),
        ('Werner Ladder', 20),
        ('Ryobi Pressure Washer', 45),
        ('Black & Decker Sander', 22),
        ('Milwaukee Nail Gun', 30),
        ('Bosch Tile Cutter', 28)
    ],
    'Electronics': [
        ('Canon DSLR Camera', 75),
        ('DJI Drone', 120),
        ('Epson Projector', 60),
        ('PlayStation Gaming Console', 50),
        ('GoPro Hero', 40),
        ('Pioneer DJ Controller', 80),
        ('Oculus VR Headset', 65)
    ],
    'Outdoor': [
        ('Coleman Tent', 35),
        ('Pelican Kayak', 55),
        ('Trek Mountain Bike', 45),
        ('Coleman Camping Stove', 25),
        ('Yeti Cooler', 30),
        ('North Face Sleeping Bag', 28),
        ('REI Hiking Backpack', 32)
    ],
    'Party': [
        ('JBL Speaker System', 85),
        ('Singing Machine Karaoke Machine', 65),
        ('Chauvet Fog Machine', 40),
        ('ADJ LED Lights', 55),
        ('SnapFloor Dance Floor', 120),
        ('Fun Booth Photo Booth', 150)
    ],
    'Sports': [
        ('Catch Surf Surfboard', 45),
        ('Burton Snowboard', 55),
        ('Callaway Golf Clubs', 60),
        ('Wilson Tennis Racket', 25),
        ('Rossignol Ski Equipment', 70),
        ('Red Paddleboard', 50)
    ]
}

DEFAULT_PHONE = 8573244764

# ============================================
# REVIEW GENERATOR
# ============================================

class CategoryAwareReviewProvider(BaseProvider):
    def __init__(self, generator):
        super().__init__(generator)
        
        self.categories = {
            'Tools': {
                'items': ['Drill', 'Circular Saw', 'Ladder', 'Pressure Washer', 'Sander', 'Nail Gun', 'Tile Cutter'],
            },
            'Electronics': {
                'items': ['Camera', 'Drone', 'Projector', 'VR Headset', 'Gaming Console', 'GoPro', 'DJ Controller'],
            },
            'Outdoor': {
                'items': ['Tent', 'Kayak', 'Mountain Bike', 'Camping Stove', 'Cooler', 'Sleeping Bag', 'Hiking Backpack'],
            },
            'Party': {
                'items': ['Speaker System', 'Karaoke Machine', 'Fog Machine', 'LED Lights', 'Dance Floor', 'Photo Booth'],
            },
            'Sports': {
                'items': ['Surfboard', 'Snowboard', 'Golf Clubs', 'Tennis Racket', 'Ski Equipment', 'Paddleboard'],
            }
        }
        
        self.universal_openings = {
            5: ["Perfect rental experience!", "Exactly what I needed!", "Couldn't be happier!"],
            4: ["Good rental overall.", "Pretty satisfied.", "Worked well for my needs."],
            3: ["It was okay.", "Did the job.", "Average experience."],
            2: ["Pretty disappointed.", "Not great.", "Had issues."],
            1: ["Terrible experience.", "Complete waste.", "Awful."]
        }
        
        self.positive_attributes = {
            'Tools': {
                'Drill': ["powerful motor", "long-lasting battery", "all drill bits included"],
                'Circular Saw': ["blade was sharp", "cuts were clean and straight", "safety guard worked well"],
                'Ladder': ["very stable", "felt safe even at full height", "perfect height for my project"],
                'Pressure Washer': ["great pressure", "cleaned everything easily", "all attachments included"]
            },
            'Electronics': {
                'Camera': ["amazing image quality", "all lenses included", "battery lasted all day"],
                'Drone': ["stable flight", "long battery life", "easy to control"],
                'Projector': ["bright clear image", "easy to set up", "worked with my laptop"],
                'Gaming Console': ["all controllers worked", "no lag or issues", "came with great games"]
            },
            'Outdoor': {
                'Tent': ["kept us completely dry", "easy to set up", "spacious inside"],
                'Kayak': ["stable on water", "comfortable seat", "paddles were good quality"],
                'Mountain Bike': ["shifts smoothly", "brakes worked great", "comfortable ride"],
                'Camping Stove': ["boiled water quickly", "fuel lasted long time", "easy to light"]
            },
            'Party': {
                'Speaker System': ["incredible bass", "crystal clear sound", "bluetooth worked perfectly"],
                'Karaoke Machine': ["microphones worked great", "huge song selection", "easy to use"],
                'Fog Machine': ["created perfect atmosphere", "fog was thick", "remote worked"],
                'LED Lights': ["bright colors", "lots of patterns", "synced to music perfectly"]
            },
            'Sports': {
                'Surfboard': ["great balance", "caught waves easily", "wax was fresh"],
                'Snowboard': ["edges were sharp", "bindings fit perfectly", "base was waxed"],
                'Golf Clubs': ["full set included", "grips were good", "even had tees and balls"],
                'Tennis Racket': ["perfect tension", "comfortable grip", "came with balls"]
            }
        }
        
        self.negative_attributes = {
            'Tools': {
                'Drill': ["battery died quickly", "chuck kept slipping", "no drill bits included"],
                'Circular Saw': ["blade was dull", "guard was broken", "wouldn't cut straight"],
                'Ladder': ["wobbly and unsafe", "missing rubber feet", "locking mechanism broken"],
                'Pressure Washer': ["weak pressure", "leaking connections", "hose was cracked"]
            },
            'Electronics': {
                'Camera': ["blurry images", "battery died in 10 minutes", "lens was scratched"],
                'Drone': ["couldn't maintain altitude", "battery lasted 5 minutes", "controller disconnected"],
                'Projector': ["dim image", "wouldn't focus", "fan was loud"],
                'Gaming Console': ["kept freezing", "controller drift", "overheated"]
            },
            'Outdoor': {
                'Tent': ["leaked in light rain", "poles were bent", "zipper broken"],
                'Kayak': ["had a slow leak", "seat was broken", "unstable in water"],
                'Mountain Bike': ["gears kept skipping", "brakes barely worked", "chain fell off"],
                'Camping Stove': ["wouldn't stay lit", "fuel leaked", "took forever to boil"]
            },
            'Party': {
                'Speaker System': ["distorted sound", "one speaker dead", "no bass"],
                'Karaoke Machine': ["microphone didn't work", "screen was broken", "kept freezing"],
                'Fog Machine': ["barely any fog", "leaked fluid everywhere", "remote broken"],
                'LED Lights': ["half didn't work", "stuck on one color", "too dim"]
            },
            'Sports': {
                'Surfboard': ["huge ding on bottom", "no wax", "fins were loose"],
                'Snowboard': ["edges were dull", "bindings broken", "base needed wax"],
                'Golf Clubs': ["grips were worn", "missing clubs", "bag was broken"],
                'Tennis Racket': ["strings were loose", "grip was worn off", "no balls included"]
            }
        }
        
        self.closings = {
            5: ["Will definitely rent again!", "Highly recommend!", "Perfect for my project!"],
            4: ["Would rent again.", "Good option.", "Worked for what I needed."],
            3: ["It was fine.", "Did the job.", "Might rent again."],
            2: ["Look elsewhere.", "Won't rent again.", "Not recommended."],
            1: ["Avoid at all costs!", "Never again!", "Total waste!"]
        }
    
    def get_item_category(self, item_name):
        item_lower = item_name.lower()
        for category, details in self.categories.items():
            for item in details['items']:
                if item.lower() in item_lower:
                    return category, item
        return 'General', None
    
    def category_aware_review(self, item_name, rating=None):
        category, item_type = self.get_item_category(item_name)
        
        if not item_type:
            return self.generic_review(rating)
        
        if rating is None:
            rating = random.choices([5, 4, 3, 2, 1], weights=[40, 30, 15, 10, 5])[0]
        
        review_parts = []
        review_parts.append(random.choice(self.universal_openings[rating]))
        
        if rating >= 4:
            if item_type in self.positive_attributes[category]:
                attribute = random.choice(self.positive_attributes[category][item_type])
                review_parts.append(f"The {item_name}'s {attribute}.")
        elif rating <= 2:
            if item_type in self.negative_attributes[category]:
                issue = random.choice(self.negative_attributes[category][item_type])
                review_parts.append(f"The {item_name} {issue}.")
        else:
            review_parts.append(f"The {item_name} worked adequately but nothing special.")
        
        review_parts.append(random.choice(self.closings[rating]))
        return " ".join(review_parts)
    
    def generic_review(self, rating=None):
        if rating is None:
            rating = random.choices([5, 4, 3, 2, 1], weights=[40, 30, 15, 10, 5])[0]
        
        generic_reviews = {
            5: "Excellent rental! Item was in perfect condition. Highly recommend!",
            4: "Good rental. Item worked well. Would rent again.",
            3: "Average experience. Item did the job. Fair for the price.",
            2: "Below expectations. Several issues. Would look elsewhere next time.",
            1: "Terrible experience. Item was not as described. Would not recommend."
        }
        return generic_reviews[rating]


# ============================================
# DATA GENERATOR
# ============================================

class CompleteDataGenerator:
    def __init__(self):
        self.review_provider = CategoryAwareReviewProvider(fake)
        fake.add_provider(self.review_provider)
    
    def generate_locations(self, count):
        locations = []
        neighborhoods = list(BOSTON_NEIGHBORHOODS.keys())
        
        for i in range(1, count + 1):
            neighborhood = neighborhoods[(i - 1) % len(neighborhoods)]
            hood_data = BOSTON_NEIGHBORHOODS[neighborhood]
            street_data = random.choice(hood_data['streets'])
            street_name = street_data['name']
            street_number = random.randint(street_data['range'][0], street_data['range'][1])
            
            address = f"{street_number} {street_name}"
            if random.random() < 0.6:
                floor = random.randint(1, 4)
                unit = random.choice(['A', 'B', 'C', 'D'])
                address += f", Apt {floor}{unit}"
            
            city = 'Cambridge' if neighborhood == 'Cambridge' else 'Boston'
            
            locations.append({
                'locationId': i,
                'address': address,
                'city': city,
                'state': 'MA',
                'country': 'USA',
                'postcode': hood_data['zip'],
                'is_default': True,
                '_neighborhood': neighborhood,
                '_lat': hood_data['coords'][0] + random.uniform(-0.005, 0.005),
                '_lng': hood_data['coords'][1] + random.uniform(-0.005, 0.005)
            })
        
        return locations
    
    def generate_users(self, count):
        users = []
        for i in range(1, count + 1):
            first_name = fake.first_name()
            last_name = fake.last_name()
            
            email_formats = [
                f"{first_name.lower()}.{last_name.lower()}",
                f"{first_name.lower()}{last_name[0].lower()}",
                f"{first_name[0].lower()}{last_name.lower()}",
                f"{first_name.lower()}{random.randint(1, 99)}"
            ]
            email_prefix = random.choice(email_formats)
            email_domain = random.choice(['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com'])
            email = f"{email_prefix}@{email_domain}"
            
            user_class = random.choices(['active', 'inactive', 'admin'], weights=[0.35, 0.60, 0.05])[0] #Made changes here -> user_class = [active, inactive, admin] from [lender, borrower, admin]
            status = random.choices(['active', 'deactivated', 'banned'], weights=[0.85, 0.12, 0.03])[0]
            pwd = hashlib.md5(f"password{i}".encode()).hexdigest()[:20]
            
            users.append({
                'userId': i,
                'firstName': first_name,
                'lastName': last_name,
                'email': email,
                'locationId': i,
                'phoneNumber': DEFAULT_PHONE,
                'class': user_class,
                'pwd': pwd,
                'status': status
            })
        
        return users
    
    def generate_items(self, users, count):
        items = []
        
        lenders = [u for u in users if u['class'] == 'active'] # Made changes here -> from lender to active
        active_borrowers = [u for u in users if u['class'] == 'inactive' and u['status'] == 'active'] # Made changes here -> from borrower to inactive

        lending_borrowers = random.sample(active_borrowers, max(1, len(active_borrowers) // 5))
        potential_lenders = lenders + lending_borrowers
        
        if not potential_lenders:
            raise ValueError("No lenders found!")
        
        for i in range(1, count + 1):
            category = random.choice(list(ITEM_CATALOG.keys()))
            item_name, base_price = random.choice(ITEM_CATALOG[category])
            price = round(base_price * random.uniform(0.8, 1.3), 2)
            owner = random.choice(potential_lenders)
            
            condition = random.choice(['Like New', 'Excellent', 'Very Good', 'Good'])
            year = random.randint(2019, 2024)
            descriptions = [
                f"{item_name} in {condition.lower()} condition. Well maintained and ready to rent.",
                f"{year} {item_name}. {condition} condition, includes all accessories.",
                f"Rent my {item_name}! {condition} condition, perfect for your needs."
            ]
            
            items.append({
                'itemId': i,
                'itemName': item_name,
                'userId': owner['userId'],
                'description': random.choice(descriptions),
                'price': price,
                'image_url': f"https://example.com/images/{category.lower()}/{i}.jpg",
                'is_available': random.choices([True, False], weights=[0.85, 0.15])[0],
                '_category': category
            })
        
        return items
    
    def generate_orders(self, users, items, count):
        orders = []
        active_borrowers = [u for u in users if u['class'] == 'inactive' and u['status'] == 'active'] #made changes here -> from borrower to inactive
        
        for i in range(1, count + 1):
            item = random.choice(items)
            renter_id = item['userId']
            
            valid_borrowers = [b for b in active_borrowers if b['userId'] != renter_id]
            if not valid_borrowers:
                continue
            
            borrower = random.choice(valid_borrowers)
            orders.append({
                'orderId': i,
                'renterId': renter_id,
                'borrowerId': borrower['userId'],
                'reviewId': None,
                '_orderDate': fake.date_between(start_date='-6m', end_date='today'),
                '_itemId': item['itemId']
            })
        
        return orders
    
    def generate_reviews(self, orders, items, review_percentage=0.7):
        reviews = []
        review_id = 1
        
        num_to_review = int(len(orders) * review_percentage)
        orders_to_review = random.sample(orders, min(num_to_review, len(orders)))
        
        for order in orders_to_review:
            item = next((i for i in items if i['itemId'] == order['_itemId']), None)
            if not item:
                continue
            
            rating = random.choices([5, 4, 3, 2, 1], weights=[40, 30, 15, 10, 5])[0]
            content = self.review_provider.category_aware_review(item['itemName'], rating)
            
            reviews.append({
                'reviewId': review_id,
                'userId': order['borrowerId'],
                'itemId': item['itemId'],
                'orderId': order['orderId'],
                'content': content,
                'rating': rating
            })
            
            order['reviewId'] = review_id
            review_id += 1
        
        return reviews
    
    def generate_user_items(self, items):
        user_items = []
        for item in items:
            user_items.append({
                'userId': item['userId'],
                'itemId': item['itemId']
            })
        return user_items
    
    def generate_all(self, num_users=20, num_items=50, num_orders=40):
        print("\n" + "=" * 70)
        print("BOSTON RENTAL DATA GENERATOR")
        print("=" * 70)
        
        print("\n📍 Generating locations...")
        locations = self.generate_locations(num_users)
        print(f"✓ Generated {len(locations)} locations")
        
        print("\n👥 Generating users...")
        users = self.generate_users(num_users)
        print(f"✓ Generated {len(users)} users")
        
        print("\n📦 Generating items...")
        items = self.generate_items(users, num_items)
        print(f"✓ Generated {len(items)} items")
        
        print("\n📋 Generating orders...")
        orders = self.generate_orders(users, items, num_orders)
        print(f"✓ Generated {len(orders)} orders")
        
        print("\n⭐ Generating reviews...")
        reviews = self.generate_reviews(orders, items)
        print(f"✓ Generated {len(reviews)} reviews")
        
        print("\n🔗 Generating user-item relationships...")
        user_items = self.generate_user_items(items)
        print(f"✓ Generated {len(user_items)} relationships")
        
        return {
            'users': users,
            'locations': locations,
            'items': items,
            'orders': orders,
            'reviews': reviews,
            'user_items': user_items
        }


# ============================================
# SQL EXPORTER
# ============================================

def export_to_sql(data, filename='complete_boston_rental.sql'):
    """Export data to SQL file"""
    with open(filename, 'w') as f:
        f.write("-- COMPLETE BOSTON RENTAL PLATFORM DATA\n")
        f.write("-- Generated with geographically accurate Boston addresses\n\n")
        
        # Locations
        f.write("-- LOCATIONS\n\n")
        for loc in data['locations']:
            f.write(f"INSERT INTO lendscapev1.\"Location\" (locationId, address, city, state, country, postcode, is_default) VALUES\n")
            f.write(f"  ({loc['locationId']}, '{loc['address']}', '{loc['city']}', '{loc['state']}', "
                    f"'{loc['country']}', '{loc['postcode']}', {str(loc['is_default']).lower()});\n")
        
        # Users
        f.write("\n-- USERS\n\n")
        for user in data['users']:
            f.write(f"INSERT INTO lendscapev1.\"User\" (userId, firstName, lastName, email, locationId, phoneNumber, class, pwd, status) VALUES\n")
            f.write(f"  ({user['userId']}, '{user['firstName']}', '{user['lastName']}', '{user['email']}', "
                    f"{user['locationId']}, {user['phoneNumber']}, '{user['class']}', '{user['pwd']}', '{user['status']}');\n")
        
        # Items
        f.write("\n-- ITEMS\n\n")
        for item in data['items']:
            desc = item['description'].replace("'", "''")
            f.write(f"INSERT INTO lendscapev1.\"Item\" (itemId, itemName, userId, description, price, image_url, is_available) VALUES\n")
            f.write(f"  ({item['itemId']}, '{item['itemName']}', {item['userId']}, '{desc}', "
                    f"{item['price']}, '{item['image_url']}', {str(item['is_available']).lower()});\n")
        
        # Orders
        f.write("\n-- ORDERS\n\n")
        for order in data['orders']:
            review_id = order['reviewId'] if order['reviewId'] else 'NULL'
            f.write(f"INSERT INTO lendscapev1.\"Order\" (orderId, renterId, borrowerId, reviewId) VALUES\n")
            f.write(f"  ({order['orderId']}, {order['renterId']}, {order['borrowerId']}, {review_id});\n")
        
        # Reviews
        f.write("\n-- REVIEWS\n\n")
        for review in data['reviews']:
            content = review['content'].replace("'", "''")
            f.write(f"INSERT INTO lendscapev1.\"Review\" (reviewId, userId, itemId, orderId, content, rating) VALUES\n")
            f.write(f"  ({review['reviewId']}, {review['userId']}, {review['itemId']}, "
                    f"{review['orderId']}, '{content}', {review['rating']});\n")
        
        # UserItem
        f.write("\n-- USERITEM\n\n")
        for ui in data['user_items']:
            f.write(f"INSERT INTO lendscapev1.\"UserItem\" (userId, itemId) VALUES\n")
            f.write(f"  ({ui['userId']}, {ui['itemId']});\n")
    
    print(f"\n✓ SQL file exported to {filename}")


# ============================================
# SUPABASE UPLOADER
# ============================================

def upload_to_supabase(sql_filename='complete_boston_rental.sql'):
    """Upload SQL file directly to Supabase"""
    
    print("\n" + "=" * 70)
    print("UPLOADING TO SUPABASE")
    print("=" * 70)
    
    # Build connection string
    DATABASE_URL = f"postgresql+psycopg2://{SUPABASE_USER}:{SUPABASE_PASSWORD}@{SUPABASE_HOST}:{SUPABASE_PORT}/{SUPABASE_DBNAME}?sslmode=require"
    
    try:
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        # Connect and execute
        with engine.connect() as connection:
            print("\n✓ Connection to Supabase successful!")
            
            # Read SQL file
            with open(sql_filename, 'r') as file:
                sql_script = file.read()
            
            print(f"✓ Read SQL file: {sql_filename}")
            
            # Execute SQL (IMPORTANT: wrap in text())
            connection.execute(text(sql_script))
            connection.commit()
            
            print("✓ SQL file executed successfully!")
            print("\n🎉 All data uploaded to Supabase!")
            return True
    
    except Exception as e:
        print(f"\n❌ Failed to upload to Supabase: {e}")
        return False


# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("STARTING DATA GENERATION AND UPLOAD")
    print("=" * 70)
    
    # Step 1: Generate data
    generator = CompleteDataGenerator()
    data = generator.generate_all(
        num_users=20,
        num_items=50,
        num_orders=40
    )
    
    # Step 2: Export to SQL file
    print("\n" + "=" * 70)
    print("EXPORTING TO SQL FILE")
    print("=" * 70)
    export_to_sql(data)
    
    # Step 3: Upload to Supabase
    upload_to_supabase()
    
    print("\n" + "=" * 70)
    print("✅ COMPLETE!")
    print("=" * 70)