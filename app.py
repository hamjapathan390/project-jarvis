import streamlit as st
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Project JARVIS: Stark Enterprise Vault", page_icon="🛡️", layout="wide")

# Initialize Authentication State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "vault" not in st.session_state:
    st.session_state.vault = []

if "student_tasks" not in st.session_state:
    st.session_state.student_tasks = []

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello Boss! JARVIS defense grid active. Authenticated under Tony Stark protocols."}
    ]

# --- TONY STARK SECURE GATEWAY ---
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://img.icons8.com/fluency/96/iron-man.png", width=90)
        st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>STARK INDUSTRIES : JARVIS</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #00ffcc;'><b>Creator: Tony Stark</b> | Digilocker Privacy Vault</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.info("💡 **Demo Access:** Email: `boss@stark.com` | Security Key: `3000`")
        
        with st.form("login_form"):
            user_email = st.text_input("Stark Enterprise Email", value="boss@stark.com")
            security_key = st.text_input("Security Passkey / Pattern Code", type="password", value="3000")
            
            login_btn = st.form_submit_button("🔓 Authorize & Access Vault", use_container_width=True)
            
            if login_btn:
                if user_email == "boss@stark.com" and security_key == "3000":
                    st.session_state.authenticated = True
                    st.success("Authorization Verified! Launching JARVIS...")
                    st.rerun()
                else:
                    st.error("Access Denied: Incorrect Stark credentials!")
        st.stop()

# --- MAIN APP ---

st.title("🛡️ Project JARVIS: Autonomous Vault & Advanced AI Assistant")
st.markdown("### *Architect: Tony Stark | Digilocker-Class Security Active*")
st.markdown("---")

all_active_records = st.session_state.vault + st.session_state.student_tasks

# OMEGA 90%+ ALERT BANNER
if len(all_active_records) > 0:
    omega_threats = [item for item in all_active_records if item.get('urgency_score', 0) >= 90.0]
    if len(omega_threats) > 0:
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #ff0000, #ff4b4b); padding: 16px 22px; border-radius: 12px; color: white; font-weight: bold; margin-bottom: 20px; box-shadow: 0 0 20px rgba(255,0,0,0.6);">
            🔥 OMEGA-LEVEL ALERT: {len(omega_threats)} critical assets have exceeded 90% urgency rating! Immediate attention required, Boss!
        </div>
        """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/iron-man.png", width=80)
    st.markdown("### Stark Command Hub")
    st.markdown(f"**Vault Records:** {len(st.session_state.vault)}")
    st.markdown(f"**Student Tasks:** {len(st.session_state.student_tasks)}")
    st.markdown("---")
    
    if st.button("🚪 Secure Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

    st.markdown("---")
    st.markdown("### 🤖 Stark File Intelligence Bot")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
                
    if user_query := st.chat_input("Ask JARVIS about any file..."):
        st.session_state.messages.append({"role": "user", "content": user_query})
        q_lower = user_query.lower()
        matched = [i for i in all_active_records if q_lower in i.get('name', '').lower() or q_lower in i.get('title', '').lower()]
        
        if matched:
            bot_reply = f"Boss, found {len(matched)} matching record(s):"
            for m in matched:
                bot_reply += f"\n- **{m.get('name', m.get('title'))}** | Due: *{m['deadline']}* | Urgency: **{m['urgency_score']}%**"
        else:
            bot_reply = f"I scanned the vault for '{user_query}', but no exact file match was found."
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.rerun()

    st.markdown("---")
    if st.button("🗑️ Purge All Data"):
        st.session_state.vault = []
        st.session_state.student_tasks = []
        st.rerun()

# Tabs
tab1, tab2 = st.tabs(["📁 Enterprise / General Vault", "🎓 Student Homework & Exam Hub"])

with tab1:
    st.subheader("📥 Secure Document & File Ingestion Portal")
    with st.form("vault_form", clear_on_submit=True):
        uploaded_file = st.file_uploader("Upload PDF, Text Document, or Image", type=["pdf", "txt", "png", "jpg", "jpeg"])
        
        col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
        with col_f1:
            dl_date = st.date_input("Deadline Date")
        with col_f2:
            dl_time = st.time_input("Deadline Time", value=datetime.strptime("12:00 PM", "%I:%M %p").time())
        with col_f3:
            ampm_choice = st.selectbox("AM / PM", ["AM", "PM"])
            
        submit_vault = st.form_submit_button("🚀 Ingest & Activate Notifications")
        
        if submit_vault and uploaded_file is not None:
            try:
                file_content = uploaded_file if "image" in uploaded_file.type else uploaded_file.getvalue().decode("utf-8", errors="ignore")
            except Exception:
                file_content = "Encrypted payload."

            time_formatted = f"{dl_time.strftime('%I:%M')} {ampm_choice}"
            deadline_str = f"{dl_date} at {time_formatted}"
            
            hour_val = dl_time.hour
            if ampm_choice == "PM" and hour_val < 12: hour_val += 12
            elif ampm_choice == "AM" and hour_val == 12: hour_val = 0
            
            deadline_dt = datetime.combine(dl_date, dl_time.replace(hour=hour_val))
            sec_diff = (deadline_dt - datetime.now()).total_seconds()
            
            if sec_diff <= 0:
                urgency_score, urgency_label = 100.0, "🚨 OMEGA EXPIRED"
            else:
                urgency_score = round(max(0.0, min(100.0, (1.0 - (sec_diff / 604800.0)) * 100.0)), 1)
                urgency_label = "🔥 OMEGA 90%+ CRITICAL" if urgency_score >= 90.0 else ("🔥 High Priority" if sec_diff < 86400 else "✅ Safe Priority")

            st.session_state.vault.append({
                "name": uploaded_file.name, "type": uploaded_file.type, "content": file_content,
                "deadline": deadline_str, "urgency_score": urgency_score, "urgency_label": urgency_label,
                "upload_time": datetime.now().strftime("%Y-%m-%d %I:%M %p")
            })
            st.success(f"Successfully ingested '{uploaded_file.name}'!")

    st.markdown("---")
    st.subheader("📋 Prioritized Vault Archive")
    if len(st.session_state.vault) > 0:
        for idx, doc in enumerate(sorted(st.session_state.vault, key=lambda x: x['urgency_score'], reverse=True)):
            border_col = "#ff0000" if doc['urgency_score'] >= 90.0 else "#00ffcc"
            st.markdown(f"""
            <div style="background-color: #1e1e2f; padding: 18px; border-radius: 12px; border-left: 6px solid {border_col}; margin-bottom: 18px;">
                <h4 style="color: #ffffff; margin-top: 0;">📁 {doc['name']}</h4>
                <p style="color: #ffcc00; margin: 4px 0;"><b>🎯 Deadline:</b> {doc['deadline']}</p>
                <p style="color: {'#ff4b4b' if doc['urgency_score'] >= 90.0 else '#00ffcc'}; margin: 4px 0;"><b>⚡ Urgency:</b> {doc['urgency_score']}% ({doc['urgency_label']})</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🗑️ Delete", key=f"del_v_{idx}"):
                st.session_state.vault.remove(doc)
                st.rerun()

with tab2:
    st.subheader("🎓 Student Homework & Exam Hub")
    with st.form("task_form", clear_on_submit=True):
        t_title = st.text_input("Task / Exam Title")
        t_desc = st.text_area("Description")
        tc1, tc2, tc3 = st.columns([2, 1, 1])
        with tc1: t_date = st.date_input("Date", key="t_d")
        with tc2: t_time = st.time_input("Time", value=datetime.strptime("12:00 PM", "%I:%M %p").time(), key="t_t")
        with tc3: t_ampm = st.selectbox("AM/PM", ["AM", "PM"], key="t_a")
        
        if st.form_submit_button("🚀 Log Task") and t_title:
            time_fmt = f"{t_time.strftime('%I:%M')} {t_ampm}"
            h_val = t_time.hour
            if t_ampm == "PM" and h_val < 12: h_val += 12
            elif t_ampm == "AM" and h_val == 12: h_val = 0
            
            t_dt = datetime.combine(t_date, t_time.replace(hour=h_val))
            s_diff = (t_dt - datetime.now()).total_seconds()
            
            t_score = 100.0 if s_diff <= 0 else round(max(0.0, min(100.0, (1.0 - (s_diff / 604800.0)) * 100.0)), 1)
            t_label = "🔥 OMEGA 90%+ CRITICAL" if t_score >= 90.0 else ("🔥 High Priority" if s_diff < 86400 else "✅ Safe Priority")
            
            st.session_state.student_tasks.append({
                "title": t_title, "desc": t_desc, "deadline": f"{t_date} at {time_fmt}",
                "urgency_score": t_score, "urgency_label": t_label, "created": datetime.now().strftime("%Y-%m-%d %I:%M %p")
            })
            st.success("Task logged successfully!")

    st.markdown("---")
    if len(st.session_state.student_tasks) > 0:
        for s_idx, task in enumerate(sorted(st.session_state.student_tasks, key=lambda x: x['urgency_score'], reverse=True)):
            t_col = "#ff0000" if task['urgency_score'] >= 90.0 else "#ffcc00"
            st.markdown(f"""
            <div style="background-color: #1e1e2f; padding: 18px; border-radius: 12px; border-left: 6px solid {t_col}; margin-bottom: 18px;">
                <h4 style="color: #ffffff; margin-top: 0;">📌 {task['title']}</h4>
                <p style="color: #ffffff;">{task['desc']}</p>
                <p style="color: #ffcc00; margin: 4px 0;"><b>🎯 Deadline:</b> {task['deadline']}</p>
                <p style="color: {'#ff4b4b' if task['urgency_score'] >= 90.0 else '#00ffcc'}; margin: 4px 0;"><b>⚡ Urgency:</b> {task['urgency_score']}% ({task['urgency_label']})</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("❌ Remove", key=f"del_t_{s_idx}"):
                st.session_state.student_tasks.remove(task)
                st.rerun()
