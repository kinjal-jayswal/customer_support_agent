"""
Customer Support Agent — JK Data Lab
Multi-turn conversational AI agent for customer support with escalation
Author: Kinjal Jayswal | JK Data Lab | www.jkdatalab.com
"""
import streamlit as st
import requests
import time
import random
from datetime import datetime

st.set_page_config(page_title="Customer Support Agent | JK Data Lab", page_icon="🎧", layout="wide")
st.markdown("""<style>
.stApp{background-color:#0A1628;color:#fff}h1,h2,h3{color:#00FFD4}
.user-msg{background:#0d1f3a;border-left:3px solid #4d9fff;border-radius:10px;padding:12px;margin:6px 0}
.agent-msg{background:#0d2a2a;border-left:3px solid #00FFD4;border-radius:10px;padding:12px;margin:6px 0}
.escalate{background:#2a1a0d;border-left:3px solid #ffd93d;border-radius:10px;padding:12px;margin:6px 0}
.stButton>button{background:linear-gradient(135deg,#00FFD4,#00aa88);color:#0A1628;font-weight:bold}
</style>""", unsafe_allow_html=True)

KNOWLEDGE_BASE = {
    "pricing": "JK Data Lab pricing: AI Consulting from $500, ML Models from $1000, Dashboards from $300, Automation from $400. Custom quotes available.",
    "services": "We offer: Data Science & Analytics, AI/ML Development, NLP Solutions, RAG Chatbots, Python Automation, Interactive Dashboards.",
    "timeline": "Typical project timelines: Small projects 1-2 weeks, Medium projects 2-4 weeks, Large projects 1-3 months.",
    "contact": "Contact us: kinjal@jkdatalab.com | +91-9157938887 | www.jkdatalab.com | Ahmedabad, Gujarat, India",
    "refund": "We offer a satisfaction guarantee. If deliverables don't meet agreed specifications, we revise at no extra cost.",
    "technology": "We use Python, TensorFlow, PyTorch, LangChain, OpenAI, Streamlit, Power BI, PostgreSQL, Docker, AWS, GCP.",
}

DEMO_RESPONSES = {
    "pricing": "Our pricing is flexible and project-based! Here's a quick overview:\n\n💰 **AI Consulting**: Starting $500\n🤖 **ML Model Development**: Starting $1,000\n📊 **Dashboards**: Starting $300\n⚙️ **Automation**: Starting $400\n\nWould you like a custom quote for your specific needs?",
    "services": "JK Data Lab offers comprehensive AI & Data Science services:\n\n🔬 Data Science & Analytics\n🤖 AI & Machine Learning\n🗣️ Natural Language Processing (NLP)\n🔍 RAG Chatbot Development\n⚙️ Python Automation\n📊 Interactive Dashboards\n\nWhich service interests you most?",
    "timeline": "Project timelines vary based on complexity:\n\n⚡ **Quick projects** (dashboards, reports): 1-2 weeks\n🔄 **Standard projects** (ML models, chatbots): 2-4 weeks\n🏗️ **Large projects** (enterprise solutions): 1-3 months\n\nWe always provide detailed timelines in our proposals.",
    "contact": "You can reach us through multiple channels:\n\n📧 Email: kinjal@jkdatalab.com\n📱 Phone: +91-9157938887\n🌐 Website: www.jkdatalab.com\n📍 Location: Ahmedabad, Gujarat, India\n\nWe typically respond within 24 hours!",
    "default": "Thank you for your question! I'm your JK Data Lab support agent. I can help you with:\n\n• **Pricing** information\n• **Services** we offer\n• **Project timelines**\n• **Contact** details\n• **Technology** stack\n\nWhat would you like to know more about?"
}

def get_intent(message: str) -> str:
    msg = message.lower()
    if any(w in msg for w in ["price", "cost", "rate", "charge", "fee", "budget"]): return "pricing"
    if any(w in msg for w in ["service", "offer", "provide", "do you", "capability"]): return "services"
    if any(w in msg for w in ["time", "duration", "long", "deadline", "when"]): return "timeline"
    if any(w in msg for w in ["contact", "email", "phone", "reach", "location"]): return "contact"
    if any(w in msg for w in ["technology", "tech", "tools", "framework", "stack"]): return "technology"
    if any(w in msg for w in ["human", "person", "agent", "escalate", "manager"]): return "escalate"
    return "default"

def get_sentiment(message: str) -> str:
    negative = ["angry", "frustrated", "terrible", "awful", "worst", "hate", "useless", "refund"]
    positive = ["great", "thanks", "good", "excellent", "love", "perfect", "awesome"]
    msg = message.lower()
    if any(w in msg for w in negative): return "negative"
    if any(w in msg for w in positive): return "positive"
    return "neutral"

st.title("🎧 Customer Support Agent")
st.markdown("**AI-powered customer support** with intent detection, knowledge base, and human escalation")
st.markdown("---")

with st.sidebar:
    st.markdown("### ⚙️ Agent Settings")
    use_demo = st.checkbox("Demo Mode", value=True)
    agent_name = st.text_input("Agent Name", value="Aria")
    company = st.text_input("Company", value="JK Data Lab")
    auto_escalate = st.checkbox("Auto-escalate negative sentiment", value=True)
    st.markdown("---")
    st.markdown("### 📊 Session Stats")
    if "messages" in st.session_state:
        st.metric("Messages", len(st.session_state.messages))
        sentiments = [m.get("sentiment", "neutral") for m in st.session_state.messages if m["role"] == "user"]
        negative_count = sentiments.count("negative")
        st.metric("Negative Sentiment", negative_count)
    st.markdown("---")
    if st.button("🔄 New Session"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("**🌐 [JK Data Lab](https://www.jkdatalab.com)**")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "agent",
        "content": f"👋 Hello! I'm **{agent_name}**, your AI support agent for {company}.\n\nI can help you with pricing, services, timelines, and more. How can I assist you today?",
        "intent": "greeting",
        "sentiment": "positive"
    })

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">👤 <strong>You:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        css = "escalate" if msg.get("intent") == "escalate" else "agent-msg"
        st.markdown(f'<div class="{css}">🎧 <strong>{agent_name}:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)

user_input = st.chat_input(f"Ask {agent_name} anything...")

if user_input:
    intent = get_intent(user_input)
    sentiment = get_sentiment(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input, "intent": intent, "sentiment": sentiment})

    with st.spinner(f"{agent_name} is typing..."):
        time.sleep(0.8)

    if sentiment == "negative" and auto_escalate:
        response = f"I'm sorry to hear you're having a difficult experience! 😟\n\nI'm escalating your concern to our senior support team immediately. A human agent will contact you within 2 hours at your registered email.\n\n📧 You can also reach us directly: kinjal@jkdatalab.com\n\nYour satisfaction is our top priority!"
        intent = "escalate"
    elif intent == "escalate":
        response = f"Of course! I'll connect you with a human agent right away.\n\n📞 **Direct contact:**\n• Email: kinjal@jkdatalab.com\n• Phone: +91-9157938887\n\nExpected response time: Within 2-4 business hours."
    else:
        response = DEMO_RESPONSES.get(intent, DEMO_RESPONSES["default"])

    st.session_state.messages.append({"role": "agent", "content": response, "intent": intent, "sentiment": "positive"})
    st.rerun()

st.markdown("---")
st.markdown("Built with ❤️ by **[JK Data Lab](https://www.jkdatalab.com)** | AI Customer Support")
