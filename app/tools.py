import os
from typing import Dict, List
from agents import function_tool
from inventory_cache import inventory_cache
from agents import Runner
import asyncio
import re
from functools import reduce
import operator

os.makedirs('data', exist_ok=True)

@function_tool
def search_vehicles_by_budget(max_budget: int, min_budget: int = 0) -> List[Dict]:
    """Searches Vehicles by Asked Budget Range"""
    
    cached_df = inventory_cache.get_inventory()
    if cached_df is None or cached_df.empty:
        print("No inventory available.")
        return []

    filtered = cached_df[
        (cached_df['price'] >= min_budget) &
        (cached_df['price'] <= max_budget) &
        (cached_df['availability'] == 'in_stock')
    ]
    return filtered.to_dict('records')


@function_tool
def search_vehicles_by_type(vehicle_types: List[str]) -> List[Dict]:
    """Searches Vehicles by Asked Vehicle Type"""

    cached_df = inventory_cache.get_inventory()
    if cached_df is None or cached_df.empty:
        print("No inventory available.")
        return []

    types_lower = [t.lower() for t in vehicle_types]
    filtered = cached_df[
        (cached_df['type'].str.lower().isin(types_lower) |
         cached_df['category'].str.lower().isin(types_lower)) &
        (cached_df['availability'] == 'in_stock')
    ]
    return filtered.to_dict('records')


@function_tool
def search_vehicles_by_features(required_features: List[str]) -> List[Dict]:   
    """Searches Vehicles by Asked Features"""

    cached_df = inventory_cache.get_inventory()
    if cached_df is None or cached_df.empty:
        print("No inventory available.")
        return []

    def has_features(vehicle_features, required):
        vehicle_features_lower = [f.lower() for f in vehicle_features]
        required_lower = [f.lower() for f in required]
        feature_text = ' '.join(vehicle_features_lower)
        return any(req in feature_text for req in required_lower)

    filtered = cached_df[
        cached_df['features'].apply(
            lambda x: has_features(x, required_features)
        ) &
        (cached_df['availability'] == 'in_stock')
    ]
    return filtered.to_dict('records')


@function_tool
def search_vehicles_by_fuel_type(fuel_types: List[str]) -> List[Dict]:   
    """Searches Vehicles by Asked Fuel Type"""

    cached_df = inventory_cache.get_inventory()
    if cached_df is None or cached_df.empty:
        print("No inventory available.")
        return []
    
    types_lower = [t.lower() for t in fuel_types]
    filtered = cached_df[
        (cached_df['fuel_type'].str.lower().isin(types_lower)) &
        (cached_df['availability'] == 'in_stock')
    ]
    return filtered.to_dict('records')


@function_tool
async def optimized_multi_agent_query(user_query: str) -> List[Dict]:
    """
    Optimized query processing with parallel agent execution

    Performance Benefits:
    - Concurrent specialist agent execution
    - Reduced total response time
    - Efficient resource utilization
    - Improved user experience
    """

    from vehicle_agents import budget_specialist, family_specialist, luxury_specialist, eco_specialist    


    # Analyze query to determine relevant specialists
    relevant_specialists = analyze_query_requirements(user_query)

    # Create concurrent tasks for relevant specialists
    specialist_tasks = []

    if 'budget' in relevant_specialists:
        specialist_tasks.append(
            Runner.run(budget_specialist, user_query)
        )

    if 'family' in relevant_specialists:
        specialist_tasks.append(
            Runner.run(family_specialist, user_query)
        )

    if 'luxury' in relevant_specialists:
        specialist_tasks.append(
            Runner.run(luxury_specialist, user_query)
        )

    if 'eco' in relevant_specialists:
        specialist_tasks.append(
            Runner.run(eco_specialist, user_query)
        )

    # Execute all relevant specialists concurrently
    specialist_results = await asyncio.gather(*specialist_tasks)    

    # Synthesize results from multiple specialists
    # final_recommendation = (
    #     specialist_results, user_query
    # )

    return specialist_results


def analyze_query_requirements(query):
    """
    Intelligent query analysis for specialist selection

    Uses keyword analysis and pattern matching to determine
    which specialists are most relevant to the user’s needs
    """
    query_lower = query.lower()
    relevant_specialists = []

    # Budget indicators
    if any(keyword in query_lower for keyword in
           ['budget', 'cheap', 'affordable', 'under', 'cost']):
        relevant_specialists.append('budget')

    # Family indicators
    if any(keyword in query_lower for keyword in
           ['family', 'kids', 'children', 'safe', 'safety']):
        relevant_specialists.append('family')

    # Luxury indicators
    if any(keyword in query_lower for keyword in
           ['luxury', 'premium', 'high-end', 'performance', 'exclusive', 'expensive']):
        relevant_specialists.append('luxury')

    # Environmental indicators
    if any(keyword in query_lower for keyword in
           ['eco', 'electric', 'hybrid', 'efficient', 'green']):
        relevant_specialists.append('eco')

    return relevant_specialists


@function_tool
def inventory_tools(query: str) -> List[Dict]:
    """
    General inventory tool to handle a wide range of inventory-related questions.

    Attempts to match the query to inventory attributes such as make, model, year,
    color, transmission, mileage, and more. Returns matching vehicles.
    """
    cached_df = inventory_cache.get_inventory()
    if cached_df is None or cached_df.empty:
        print("No inventory available.")
        return []

    query_lower = query.lower()
    filters = []

    # Example: simple keyword-based matching for common attributes
    if any(word in query_lower for word in ['red', 'blue', 'black', 'white', 'silver']):
        for color in ['red', 'blue', 'black', 'white', 'silver']:
            if color in query_lower:
                filters.append(cached_df['color'].str.lower() == color)

    if any(word in query_lower for word in ['automatic', 'manual']):
        if 'automatic' in query_lower:
            filters.append(cached_df['transmission'].str.lower() == 'automatic')
        if 'manual' in query_lower:
            filters.append(cached_df['transmission'].str.lower() == 'manual')

    # Year extraction (e.g., "2020 model")
    year_matches = re.findall(r'\b(20[0-4][0-9]|19[8-9][0-9])\b', query_lower)
    if year_matches:
        years = [int(y) for y in year_matches]
        filters.append(cached_df['year'].isin(years))

    # Make/model matching (example: "Toyota", "Camry")
    for col in ['make', 'model']:
        for val in cached_df[col].dropna().unique():
            if str(val).lower() in query_lower:
                filters.append(cached_df[col].str.lower() == str(val).lower())

    # Mileage (e.g., "under 50000 miles")
    mileage_match = re.search(r'under\s+(\d{2,6})\s*miles', query_lower)
    if mileage_match:
        max_mileage = int(mileage_match.group(1))
        filters.append(cached_df['mileage'] <= max_mileage)

    # Only show in-stock vehicles
    filters.append(cached_df['availability'] == 'in_stock')

    if filters:
        mask = reduce(operator.and_, filters)
        filtered = cached_df[mask]
    else:
        filtered = cached_df[cached_df['availability'] == 'in_stock']

    return filtered.to_dict('records')