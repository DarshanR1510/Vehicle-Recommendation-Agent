# 🚗 Vehicle Recommendation Agent

A production-ready, multi-agent vehicle recommendation system with a beautiful Gradio-powered chat UI. Get personalized car suggestions based on your needs, budget, and preferences—powered by specialist agents and robust error handling.

---

## ✨ Features

- **Conversational Chatbot UI**: Modern, dark-themed Gradio interface with orange highlights.
- **Multi-Agent Intelligence**: Specialist agents for budget, family, luxury, and eco-friendly vehicles.
- **Smart Query Routing**: Automatic selection of the best agent(s) for each user query.
- **Robust Error Handling**: Retries, timeouts, and graceful fallback responses.
- **Production-Ready**: Includes caching, rate limiting, monitoring hooks, and scalable architecture.
- **Easy Deployment**: Ready for Hugging Face Spaces, local, or cloud deployment.

---

## 🚀 Quick Start

### 1. Clone the Repo
```sh
git clone https://github.com/yourusername/vehicle-recommendation-agent.git
cd vehicle-recommendation-agent
```

- Make sure you have UV installed
- Create an `.env` file with your API keys and configuration.
- Make sure to add `OPENAI_API_KEY=your_openai_key` to your `.env` file.
### 2. Sync Requirements
```sh
    uv sync
```

### 3. Run the App
```sh
uv run app/app.py
```

The Gradio UI will open in your browser. Ask anything about vehicles!

---

## 🛠️ Project Structure

```
app/
  ├── app.py                # Gradio UI entry point
  ├── tools.py              # Specialist search tools
  ├── vehicle_agents.py     # Agent definitions
  ├── inventory_cache.py    # Inventory caching system
  ├── error_handling.py     # Robust error handling
  ├── data/                 # Data and config files
  └── ...
pyproject.toml
README.md
```

---

## 🤖 How It Works

- **User** enters a query (e.g., "I need a family SUV under $30k").
- **vehicle_recommendation_agent** analyzes the query and routes it to the most relevant specialist agents.
- **Specialist agents** (budget, family, luxury, eco) search the inventory and return recommendations.
- **Chatbot** displays the best results with a friendly, interactive UI.

---

## 🌐 Deploy on Hugging Face Spaces

1. Push your code to GitHub.
2. Create a new Space on [Hugging Face Spaces](https://huggingface.co/spaces) (choose Gradio SDK).
3. Upload your code or link your repo.
4. Add any required secrets in the Space settings.
5. Enjoy your public vehicle recommendation chatbot!

---

## 📸 Demo

![Vehicle Recommendation Agent Chatbot](vehicle_recommendation_agent_chatbot.png)

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [Gradio](https://gradio.app/)
- [Hugging Face Spaces](https://huggingface.co/spaces)
- All open-source contributors
