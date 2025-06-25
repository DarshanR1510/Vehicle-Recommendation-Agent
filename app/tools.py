import os
from typing import Dict, List
from agents import function_tool
from inventory_cache import inventory_cache
from agents import Runner
import asyncio

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
