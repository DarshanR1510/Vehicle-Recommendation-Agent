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
#send-btn {background: linear-gradient(90deg, #ff9800, #ffb74d); color: #23272a; border-radius: 8px; font-weight:600; border: none;}
.gr-button:hover, #send-btn:hover {background: linear-gradient(90deg, #ffb74d, #ff9800); color: #23272a;}
.gr-chat-message {background: #23272a; color: #fff;}
""") as demo:
    gr.Markdown("""
    <div id='main-title'>🚗 Vehicle Recommendation System</div>
    <div id='subtitle'>Ask me about vehicles! (e.g., <i>I need a family SUV under $30k</i>)</div>
    """)
    status = gr.Markdown(ensure_inventory(), elem_id="status-bar")
    chatbot = gr.Chatbot(elem_id="chatbot", height=400, bubble_full_width=False, avatar_images=(None, "https://img.icons8.com/color/48/000000/car--v2.png"))
    with gr.Row():
        user_input = gr.Textbox(placeholder="Type your vehicle query here...", label="Your Query", elem_id="user-input", scale=8)
        send_btn = gr.Button("Send", elem_id="send-btn", scale=2)

    def respond(history, user_message):
        if not user_message.strip():
            return history, ""
        response = agent_response(user_message, history)
        history = history or []
        history.append((user_message, response))
        return history, ""

    send_btn.click(respond, inputs=[chatbot, user_input], outputs=[chatbot, user_input])
    user_input.submit(respond, inputs=[chatbot, user_input], outputs=[chatbot, user_input])

demo.launch()
