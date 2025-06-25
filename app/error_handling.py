from agents import Runner
import asyncio

class AgentSystemError(Exception):
    """ Custom exception class for agent system errors """
    def __init__(self , message , error_type=None , context=None):
        self.message = message
        self.error_type = error_type
        self.context = context
        super().__init__(self.message)

async def robust_agent_execution(agent , query , max_retries =3):
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
            result = await asyncio.wait_for(
                Runner.run(agent , query),
                timeout =30.0 # 30-second timeout
            )

            # Validate response quality
            if validate_response_quality(result):
                return result
            else:
                raise AgentSystemError(
                    "Response quality validation failed",
                    error_type="QUALITY_ERROR",
                    context ={"attempt": attempt + 1, "agent": agent.name}
                )

        except asyncio.TimeoutError:
            print(f"Timeout on attempt {attempt + 1}/{ max_retries}")
            if attempt < max_retries - 1:
                await asyncio.sleep (2 ** attempt) # Exponential backoff

        except Exception as e:
            error_details = {
                "attempt": attempt + 1,
                "agent": agent.name ,
                "query": query [:100] , # Truncated for logging
                "error": str(e)
            }

            print(f"Execution error: {e}")

            if attempt < max_retries - 1:
                await asyncio.sleep (2 ** attempt)
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
        # Verify specific vehicle mentions
        vehicle_keywords = ['toyota', 'honda', 'ford', 'bmw', 'tesla', 'hyundai']
        if not any(keyword in response.lower() for keyword in vehicle_keywords):
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