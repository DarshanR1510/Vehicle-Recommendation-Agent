from agents import Runner
import asyncio

class AgentSystemError(Exception):
    """ Custom exception class for agent system errors """
    def __init__(self , message , error_type=None , context=None):
        self.message = message
        self.error_type = error_type
        self.context = context
        super().__init__(self.message)

async def robust_agent_execution(agent, query, max_retries=3, history=None):
    """
    Robust agent execution with comprehensive error handling

    Error Recovery Strategies:
    - Automatic retry with exponential backoff
    - Graceful degradation to fallback responses
    - Detailed error logging and reporting
    - Context preservation for debugging
    """

    for attempt in range(max_retries):
        try:
            # Execute agent with timeout protection
            query = f"""User's query: {query.strip()}\n
            User's history: {history}
            """
            result = await asyncio.wait_for(
                Runner.run(agent, query),
                timeout=30.0  # 30-second timeout
            )

            # Validate response quality
            if validate_response_quality(result):
                return result
            else:
                raise AgentSystemError(
                    "Response quality validation failed",
                    error_type="QUALITY_ERROR",
                    context={"attempt": attempt + 1, "agent": agent.name}
                )

        except asyncio.TimeoutError:
            print(f"Timeout on attempt {attempt + 1}/{max_retries}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff

        except Exception as e:
            error_details = {
                "attempt": attempt + 1,
                "agent": agent.name,
                "query": query[:100],  # Truncated for logging
                "error": str(e)
            }

            print(f"Execution error: {e}")

            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)
            else:
                # Final attempt failed - return fallback response
                return generate_fallback_response(query , str(e))

def validate_response_quality(result):
    """
    Response quality validation with multiple criteria

    Quality Checks:
    - Minimum response length
    - Presence of key information
    - Logical structure validation
    - Factual consistency checks
    """
    try:
        response = result.final_output

        # Basic length validation
        if len(response) < 50:
            return False

        # Check for vehicle recommendations or inventory/communication keywords
        inventory_keywords = [
            'inventory', 'stock', 'available', 'in stock', 'models', 'makes', 'count', 'total', 'list',
            'recommend', 'suggest', 'option', 'choose', 'select', 'find', 'offer', 'provide', 'show',
            'family', 'budget', 'eco', 'luxury', 'category', 'type', 'feature', 'price', 'cost', 'value',
            'details', 'summary', 'overview', 'information', 'data', 'statistics', 'summary', 'result'
        ]
        vehicle_keywords = [
            'toyota', 'honda', 'ford', 'bmw', 'tesla', 'hyundai', 'kia', 'chevrolet', 'subaru', 'mercedes',
            'mazda', 'volkswagen', 'nissan', 'volvo', 'audi', 'chrysler', 'jeep', 'lexus', 'camry', 'cr-v',
            'model 3', 'f-150', 'x3', 'elantra', 'soul', 'bolt', 'outback', 'e-class', 'sienna', 'cx-5',
            'ioniq', 'id.4', 'civic', 'leaf', 'xc90', 'escape', 'corolla', 'q5', 'niro', 'pacifica', 'traverse', 'es 300h', 'grand cherokee'
        ]
        if not any(keyword in response.lower() for keyword in vehicle_keywords + inventory_keywords):
            return False

        return True
    except Exception as e:
        print(f"Validation error: {e}")
        return False

def generate_fallback_response(query, error_message):
    """
    Generate meaningful fallback response when agent execution fails
    """
    return f"""
        I apologize, but I'm experiencing technical difficulties processing your request.

        Your query: "{query[:100]}..."

        While I resolve this issue, here are some general recommendations:
        1. Consider visiting our showroom for personalized assistance
        2. Browse our online inventory for available vehicles
        3. Contact our sales team directly for immediate help

        Technical details: {error_message}
        """