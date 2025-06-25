import os
import json

def generate_customer_personas():
    """ Create diverse customer profiles for comprehensive testing """
    personas = [
        {
            "name": "Young Professional",
            "budget_max": 30000,
            "family_size": 1,
            "priorities": ["fuel_economy", "technology", "style"],
            "usage": "daily_commute",
            "preferences": ["compact", "sedan"],
            "test_query": "I need a fuel-efficient car for my daily commute under $30k"
        },
        {
            "name": "Growing Family",
            "budget_max": 40000,
            "family_size": 4,
            "priorities": ["safety", "space", "reliability"],
            "usage": "family_trips",
            "preferences": ["suv", "minivan"],
            "test_query": "I have two kids and need a safe, spacious vehicle for family trips"
        },
        {
            "name": "Eco-Conscious",
            "budget_max": 50000,
            "family_size": 2,
            "priorities": ["environmental", "technology", "efficiency"],
            "usage": "mixed",
            "preferences": ["electric", "hybrid"],
            "test_query": "I want an environmentally friendly car with the latest technology"
        },
        {
            "name": "Work Contractor",
            "budget_max": 45000,
            "family_size": 1,
            "priorities": ["capability", "durability", "utility"],
            "usage": "work_hauling",
            "preferences": ["truck", "van"],
            "test_query": "I need a truck for my construction business that can haul materials"
        }
    ]

    # Persist data to JSON for consistency across sessions
    os.makedirs('data', exist_ok=True) # Ensure 'data' directory exists
    with open('data/customer_personas.json', 'w') as f:
        json.dump(personas, f, indent=2)

    return personas

