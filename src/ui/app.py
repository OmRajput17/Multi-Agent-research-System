import streamlit as st
import requests

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
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">Research Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Multi-Agent AI Research Pipeline</div>', unsafe_allow_html=True)

API_URL = "http://localhost:8000"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.markdown(msg["content"])
        else:
            data = msg["data"]

            route = data.get("route", "mixed")
            badge_class = f"badge-{route}"
            st.markdown(
                f'<span class="status-badge {badge_class}">{route.upper()} search</span>',
                unsafe_allow_html=True
            )

            st.markdown("---")
            st.markdown(data["report"])

            st.download_button(
                "Download Report",
                data["report"],
                file_name="research_report.md",
                mime="text/markdown",
                key=f"dl_{msg.get('id', 0)}"
            )

            with st.expander("Fact-Check Scores"):
                for claim, score in data["fact_check"].items():
                    if score >= 0.8:
                        emoji = "🟢"
                    elif score >= 0.6:
                        emoji = "🟡"
                    else:
                        emoji = "🔴"
                    st.markdown(f"{emoji} **{score:.0%}** - {claim}")

            with st.expander(f"Citations ({len(data['citations'])})"):
                for i, url in enumerate(data["citations"], 1):
                    st.markdown(f"**[{i}]** [{url}]({url})")

# Chat input
if query := st.chat_input("Ask a research question..."):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Running research pipeline... This may take 1-2 minutes."):
            try:
                response = requests.post(
                    f"{API_URL}/research",
                    json={"query": query},
                    timeout=300
                )
                data = response.json()

                route = data.get("route", "mixed")
                badge_class = f"badge-{route}"
                st.markdown(
                    f'<span class="status-badge {badge_class}">{route.upper()} search</span>',
                    unsafe_allow_html=True
                )

                st.markdown("---")
                st.markdown(data["report"])

                st.download_button(
                    "Download Report",
                    data["report"],
                    file_name="research_report.md",
                    mime="text/markdown",
                    key="dl_latest"
                )

                with st.expander("Fact-Check Scores"):
                    for claim, score in data["fact_check"].items():
                        if score >= 0.8:
                            emoji = "🟢"
                        elif score >= 0.6:
                            emoji = "🟡"
                        else:
                            emoji = "🔴"
                        st.markdown(f"{emoji} **{score:.0%}** - {claim}")

                with st.expander(f"Citations ({len(data['citations'])})"):
                    for i, url in enumerate(data["citations"], 1):
                        st.markdown(f"**[{i}]** [{url}]({url})")

                msg_id = len(st.session_state.messages)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": data["report"],
                    "data": data,
                    "id": msg_id
                })

            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to API. Start it with: python -m uvicorn src.api.main:app --reload --port 8000")
            except Exception as e:
                st.error(f"Error: {e}")
