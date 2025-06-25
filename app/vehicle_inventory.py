from dotenv import load_dotenv
import json
import os

load_dotenv(override=True)

def generate_synthetic_inventory():
    """ Generate synthetic vehicle inventory with realistic market representation """
    
    inventory_data = [
        {
            "id": "V001",               # Unique identifier for referencing
            "make": "Toyota",           # Manufacturer brand
            "model": "Camry",           # Specific model name
            "year": 2024,               # Model year
            "type": "Sedan",            # Vehicle category classification
            "price": 28000,             # MSRP in USD
            "mpg_city": 28,             # City fuel efficiency rating
            "mpg_highway": 39,          # Highway fuel efficiency rating
            "seating_capacity": 5,      # Passenger capacity
            "safety_rating": 5,         # NHTSA-style 1-5 star rating
            "drivetrain": "FWD",        # Drive system configuration
            "fuel_type": "Hybrid",    # Power source type
            "features": [               # Comprehensive feature list
                "Backup Camera",
                "Bluetooth",
                "Lane Assist",
                "Adaptive Cruise Control",
                "Automatic Emergency Braking"
            ],
            "colors_available": [       # Available color options
                "White", 
                "Black", 
                "Silver", 
                "Red", 
                "Blue"
            ],
            "availability": "in_stock",  # Current stock status
            "stock_count": 12,           # Units available
            "category": "family",        # Classification for filtering
            "description": "Reliable family sedan with excellent fuel economy and safety features"
        },
        {
            "id": "V002",
            "make": "Honda",
            "model": "CR-V",
            "year": 2024,
            "type": "Compact SUV",
            "price": 32000,
            "mpg_city": 27,
            "mpg_highway": 33,
            "seating_capacity": 5,
            "safety_rating": 5,
            "drivetrain": "AWD",
            "fuel_type": "Gasoline",
            "features": [
                "Backup Camera",
                "Bluetooth",
                "Adaptive Cruise Control",
                "Blind Spot Monitor",
                "Spacious Interior"
            ],
            "colors_available": [
                "Silver", "White", "Gray", "Blue", "Black"
            ],
            "availability": "in_stock",
            "stock_count": 8,
            "category": "family",
            "description": "Versatile compact SUV ideal for family transport, known for safety and versatility."
        },
        {
            "id": "V003",
            "make": "Tesla",
            "model": "Model 3",
            "year": 2024,
            "type": "Electric Sedan",
            "price": 42000,
            "mpg_city": 132,  # MPGe
            "mpg_highway": 121,  # MPGe
            "seating_capacity": 5,
            "safety_rating": 5,
            "drivetrain": "RWD",
            "fuel_type": "Electric",
            "features": [
                "Autopilot",
                "Touchscreen Display",
                "Over-the-air Updates",
                "Heated Seats",
                "Premium Audio System"
            ],
            "colors_available": [
                "White", "Black", "Red", "Blue", "Gray"
            ],
            "availability": "in_stock",
            "stock_count": 7,
            "category": "eco",
            "description": "Tech-forward electric sedan offering Autopilot and strong sustainability credentials."
        },
        {
            "id": "V004",
            "make": "Ford",
            "model": "F-150",
            "year": 2024,
            "type": "Pickup Truck",
            "price": 38000,
            "mpg_city": 20,
            "mpg_highway": 26,
            "seating_capacity": 5,
            "safety_rating": 4,
            "drivetrain": "4WD",
            "fuel_type": "Gasoline",
            "features": [
                "Towing Package",
                "Large Bed",
                "Trailer Assist",
                "Off-road Capability",
                "Sync 4 Infotainment"
            ],
            "colors_available": [
                "White", "Black", "Red", "Blue", "Gray"
            ],
            "availability": "in_stock",
            "stock_count": 9,
            "category": "work",
            "description": "Robust pickup truck known for work capability, towing prowess, and durability."
        },
        {
            "id": "V005",
            "make": "BMW",
            "model": "X3",
            "year": 2024,
            "type": "Luxury SUV",
            "price": 48000,
            "mpg_city": 23,
            "mpg_highway": 29,
            "seating_capacity": 5,
            "safety_rating": 5,
            "drivetrain": "AWD",
            "fuel_type": "Gasoline",
            "features": [
                "Leather Seats",
                "Panoramic Sunroof",
                "Heads-up Display",
                "Harman Kardon Sound",
                "Parking Assistant Plus"
            ],
            "colors_available": [
                "Black", "White", "Blue", "Silver", "Gray"
            ],
            "availability": "in_stock",
            "stock_count": 5,
            "category": "luxury",
            "description": "Premium luxury SUV offering a refined driving experience and high-end features."
        },
        {
            "id": "V006",
            "make": "Hyundai",
            "model": "Elantra",
            "year": 2024,
            "type": "Compact Sedan",
            "price": 22000,
            "mpg_city": 31,
            "mpg_highway": 40,
            "seating_capacity": 5,
            "safety_rating": 4,
            "drivetrain": "FWD",
            "fuel_type": "Gasoline",
            "features": [
                "Touchscreen Display",
                "Apple CarPlay",
                "Android Auto",
                "Lane Keeping Assist",
                "Forward Collision Avoidance"
            ],
            "colors_available": [
                "White", "Black", "Silver", "Red", "Blue"
            ],
            "availability": "in_stock",
            "stock_count": 15,
            "category": "budget",
            "description": "Cost-conscious budget sedan offering great value, fuel efficiency, and a solid warranty."
        }
    ]

    # Persist data to JSON for consistency across sessions [4]
    os.makedirs('data', exist_ok=True) # Ensure 'data' directory exists
    with open('data/synthetic_inventory.json', 'w') as f:
        json.dump(inventory_data, f, indent=2)

    return inventory_data

# To generate the inventory after any modifications:
# generate_synthetic_inventory()