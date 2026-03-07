import streamlit as st
import requests
import os

st.set_page_config(
    page_title="Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for premium look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    .stApp {
        font-family: 'Inter', sans-serif;
    }
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #888;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    .badge-academic { background: #e8f5e9; color: #2e7d32; }
    .badge-web { background: #e3f2fd; color: #1565c0; }
    .badge-mixed { background: #fff3e0; color: #e65100; }
    .badge-general { background: #f3e5f5; color: #6a1b9a; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">Research Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Multi-Agent AI Research Pipeline</div>', unsafe_allow_html=True)

API_URL = os.environ.get("API_URL", "http://localhost:8000")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


def render_response(data, msg_index):
    """Render an assistant response. Used for both history and new messages."""
    route = data.get("route", "mixed")
    badge_class = f"badge-{route}"
    st.markdown(
        f'<span class="status-badge {badge_class}">{route.upper()} search</span>',
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown(data["report"])

    # Download button only for actual research reports
    if route != "general":
        st.download_button(
            "📥 Download Report",
            data["report"],
            file_name=f"research_report_{msg_index}.md",
            mime="text/markdown",
            key=f"download_btn_{msg_index}"
        )

    # Only show fact-check and citations if they have content
    fact_check = data.get("fact_check", {})
    citations = data.get("citations", [])

    if fact_check:
        with st.expander(f"✅ Fact-Check Scores ({len(fact_check)} claims)", expanded=False):
            for claim, score in fact_check.items():
                score = float(score)  # ensure numeric
                if score >= 0.8:
                    emoji = "🟢"
                elif score >= 0.6:
                    emoji = "🟡"
                else:
                    emoji = "🔴"
                st.markdown(f"{emoji} **{score:.0%}** — {claim}")

    if citations:
        with st.expander(f"📚 Citations ({len(citations)})", expanded=False):
            for i, url in enumerate(citations, 1):
                st.markdown(f"**[{i}]** [{url}]({url})")


# Display full chat history
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.markdown(msg["content"])
        else:
            render_response(msg["data"], idx)

# Chat input
if query := st.chat_input("Ask a research question..."):
    # 1. Add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # 2. Call API and display response
    with st.chat_message("assistant"):
        with st.spinner("� Thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/research",
                    json={"query": query},
                    timeout=300
                )

                # Handle API errors (rate limit, server errors)
                if response.status_code != 200:
                    error_data = response.json()
                    if response.status_code == 429:
                        st.warning("⏳ **Rate limit reached.** The free Groq tier allows 100K tokens/day. Please wait a few minutes and try again.")
                    else:
                        st.error(f"❌ {error_data.get('message', 'Something went wrong')}")
                    st.stop()

                data = response.json()

                # Add assistant message to history FIRST
                msg_index = len(st.session_state.messages)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": data["report"],
                    "data": data,
                })

                # Then render it
                render_response(data, msg_index)

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to API. Make sure the backend is running.")
            except Exception as e:
                st.error(f"❌ Error: {e}")

