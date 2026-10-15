import streamlit as st
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Project JARVIS: AI Vault & Sentinel", page_icon="🛡️", layout="wide")

# Stark-Grade Header & Cinematic Aura
st.title("🛡️ Project JARVIS: Autonomous Vault & Advanced AI Assistant")
st.markdown("### *Digilocker-Class Security, Autonomous Reminders & Next-Gen Document Intelligence.*")
st.markdown("---")

# Initialize Session State
if "vault" not in st.session_state:
    st.session_state.vault = []

if "student_tasks" not in st.session_state:
    st.session_state.student_tasks = []

if "bot_logs" not in st.session_state:
    st.session_state.bot_logs = [
        {"role": "assistant", "content": "JARVIS Sentinel online, Boss. Ready to analyze uploaded assets and task statuses for KRYPTA 2026."}
    ]

# Combine all records for global checks
all_active_records = st.session_state.vault + st.session_state.student_tasks

# --- TONY STARK AURA: OMEGA 90%+ CRITICAL ALERT BANNER ---
if len(all_active_records) > 0:
    omega_threats = [item for item in all_active_records if item.get('urgency_score', 0) >= 90.0]
    if len(omega_threats) > 0:
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #ff0000, #ff4b4b); padding: 16px 22px; border-radius: 12px; color: white; font-weight: bold; margin-bottom: 20px; box-shadow: 0 0 20px rgba(255,0,0,0.6); border: 2px solid #ffcc00;">
            🔥 OMEGA-LEVEL ALERT: {len(omega_threats)} critical assets have exceeded 90% urgency rating! Immediate intervention required, Boss!
        </div>
        """, unsafe_allow_html=True)

# Sidebar for System Diagnostics & Document Intelligence Bot
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/iron-man.png", width=80)
    st.markdown("### JARVIS Command Hub")
    st.info("Status: Online & Autonomous [Mark VII Ready]")
    st.markdown(f"**Vault Records:** {len(st.session_state.vault)}")
    st.markdown(f"**Student Tasks:** {len(st.session_state.student_tasks)}")
    st.markdown("---")
    
    st.markdown("### 🤖 Document & Task Status Intelligence")
    st.markdown("Ask JARVIS to find status by entering an asset/task name or keyword:")
    
    # Display conversation logs
    for log in st.session_state.bot_logs:
        with st.chat_message(log["role"]):
            st.markdown(log["content"])
                
    # Targeted Status Query Input
    if file_query := st.chat_input("Enter filename or task keyword..."):
        st.session_state.bot_logs.append({"role": "user", "content": file_query})
        q_lower = file_query.lower()
        
        matched_items = [
            item for item in all_active_records 
            if q_lower in item.get('name', '').lower() or q_lower in item.get('title', '').lower() or q_lower in item.get('desc', '').lower()
        ]
        
        if len(matched_
