import gradio as gr
import asyncio
from agents import Runner
from error_handling import robust_agent_execution
from vehicle_agents import vehicle_recommendation_agent
from inventory_cache import inventory_cache

# Ensure inventory is loaded at startup
def ensure_inventory():
    cached_df = inventory_cache.get_inventory()
    return f"<span style='color:#ff9800;font-weight:bold'>Inventory loaded: {len(cached_df)} vehicles available.</span>"

async def agent_response_async(user_input, history=None):
    if history is not None and len(history) > 0:
        formatted_history = []
        for user_msg, agent_msg in history:
            formatted_history.append({"role": "user", "content": user_msg})
            formatted_history.append({"role": "assistant", "content": agent_msg})
        result = await robust_agent_execution(vehicle_recommendation_agent, user_input, history=formatted_history)
    else:
        result = await robust_agent_execution(vehicle_recommendation_agent, user_input)    
    return result if isinstance(result, str) else result.final_output

def agent_response(user_input, history=None):
    return asyncio.run(agent_response_async(user_input, history))

with gr.Blocks(theme=gr.themes.Base(), css="""
    body { background: #23272a; }
    #main-title {text-align:center; font-size:2.5em; font-weight:700; color:#ff9800; margin-bottom:0.2em;}
    #subtitle {text-align:center; font-size:1.2em; color:#e0e0e0; margin-bottom:1.5em;}
    #status-bar {margin-bottom:1em; color:#ff9800;}
    #chatbot {background: #2c2f34; border-radius: 12px; color: #fff;}
    #user-input {border-radius: 8px; border: 1px solid #ff9800; background: #23272a; color: #fff;}
    #send-btn {
        background: linear-gradient(90deg, #ff9800, #ffb74d); 
        color: #23272a; 
        border-radius: 8px; 
        font-weight:600; 
        border: none;
        position: relative;
        z-index: 1;
        overflow: hidden;
    }
    #send-btn.rotating-border {
        animation: rotate-border 1s linear infinite;
        box-shadow: 0 0 0 3px #ff9800, 0 0 10px 3px #ffb74d;
    }
    @keyframes rotate-border {
        0% { box-shadow: 0 0 0 3px #ff9800, 0 0 10px 3px #ffb74d; }
        50% { box-shadow: 0 0 0 3px #ffb74d, 0 0 10px 3px #ff9800; }
        100% { box-shadow: 0 0 0 3px #ff9800, 0 0 10px 3px #ffb74d; }
    }
    .gr-button:hover, #send-btn:hover {background: linear-gradient(90deg, #ffb74d, #ff9800); color: #23272a;}
    .gr-chat-message {background: #23272a; color: #fff;}
    #error-message {color: #ff5252; font-weight: bold; margin-top: 0.5em; text-align: center;}
    """) as demo:
    
    gr.Markdown("""
    <div id='main-title'>🚗 Vehicle Recommendation System</div>
    <div id='subtitle'>Ask me about vehicles! (e.g., <i>I need a family SUV under $30k</i>)</div>
    """)
    
    status = gr.Markdown(ensure_inventory(), elem_id="status-bar")
    chatbot = gr.Chatbot(elem_id="chatbot", height=400, bubble_full_width=False, avatar_images=(None, "https://img.icons8.com/color/48/000000/car--v2.png"))
    
    with gr.Row():
        user_input = gr.Textbox(placeholder="Type your vehicle query here...", label="Your Query", elem_id="user-input", scale=8)
        with gr.Column(scale=2):
            send_btn = gr.Button("Send", elem_id="send-btn")
            clear_btn = gr.Button("Clear Chat", elem_id="clear-btn")
    error_box = gr.Markdown("", elem_id="error-message")
    loading_box = gr.Markdown("", visible=False)

    def respond(history, user_message):
        if not user_message.strip():
            return history, "", "", ""
        try:
            # Show loading indicator
            loading = "<span style='color:#ff9800;'>Thinking...</span>"
            # No error at start
            error = ""
            # Call agent (this will block, so loading will only show briefly)
            response = agent_response(user_message, history)
            loading = ""  # Hide loading after response
        except Exception as e:
            loading = ""
            response = "Sorry, something went wrong."
            error = f"Error: {str(e)}"
        history = history or []
        history.append((user_message, response))
        return history, "", loading, error

    def clear_chat():
        return [], "", "", ""

    send_btn.click(respond, inputs=[chatbot, user_input], outputs=[chatbot, user_input, loading_box, error_box])
    user_input.submit(respond, inputs=[chatbot, user_input], outputs=[chatbot, user_input, loading_box, error_box])
    clear_btn.click(clear_chat, outputs=[chatbot, user_input, loading_box, error_box])

    gr.Markdown("""
    <hr>
    <div style='color:#ff9800; font-size:1.1em; font-weight:600; margin-top:1.5em;'>💡 Example Questions</div>
    <ul style='color:#fff; font-size:1em; line-height:1.7;'>
      <li>I need a reliable family SUV under $40,000 with good safety ratings.</li>
      <li>Show me all electric vehicles available in your inventory.</li>
      <li>Which vehicles do you recommend for a daily city commute with great fuel efficiency?</li>
      <li>List all luxury SUVs you have in stock.</li>
      <li>What is the most affordable car with advanced safety features?</li>
      <li>How many Toyota vehicles are currently available?</li>
      <li>Do you have any 7-seater vehicles suitable for large families?</li>
      <li>Show me vehicles available in red color.</li>
      <li>Which cars have both sunroof and leather seats?</li>
      <li>Can you summarize your current vehicle inventory?</li>
      <li>Which electric vehicles are available in blue or white color?</li>
      <li>List all hybrid vehicles with a budget below $35,000.</li>
      <li>Are there any vehicles with adaptive cruise control?</li>
      <li>What are the available colors for the Honda Accord?</li>
      <li>List all 7-seater vehicles with a 5-star safety rating.</li>
    </ul>
    <div style='text-align:center; color:#ff9800; font-size:1em; margin-top:2em;'>Developed by Darshan Ramani</div>
    """)

demo.launch()
