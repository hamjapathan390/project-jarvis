import streamlit as st
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Project JARVIS: Stark Enterprise Vault", page_icon="🛡️", layout="wide")

# Initialize Authentication & Session State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "registered_users" not in st.session_state:
    # Pre-loaded default Stark credential for instant hackathon demo access!
    st.session_state.registered_users = {
        "boss@stark.com": {"password": "jarvis3000", "pattern": "3000"}
    }

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "vault" not in st.session_state:
    st.session_state.vault = []

if "student_tasks" not in st.session_state:
    st.session_state.student_tasks = []

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello Boss! JARVIS defense grid active. Authenticated under Tony Stark protocols."}
    ]

# --- TONY STARK BRANDED SECURE AUTH GATEWAY ---
if not st.session_state.authenticated:
    col_logo1, col_logo2, col_logo3 = st.columns([1, 1, 1])
    with col_logo2:
        st.image("https://img.icons8.com/fluency/96/iron-man.png", width=100)
    
    st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>STARK INDUSTRIES : PROJECT JARVIS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #00ffcc; font-size: 16px;'><b>Creator & Architect: Tony Stark</b> | Digilocker-Class Enterprise Privacy Gate</p>", unsafe_allow_html=True)
    st.markdown("---")

    col_a1, col_a2, col_a3 = st.columns([1, 2, 1])
    with col_a2:
        st.info("💡 **Hackathon Demo Hint:** You can login instantly using Demo Credentials -> Email: `boss@stark.com` | Password: `jarvis3000` | Passcode: `3000`")
        
        auth_mode = st.radio("Select Access Protocol:", ["🔑 Login Existing Account", "✨ Create New Stark ID"], horizontal=True)
        
        with st.form("stark_auth_form"):
            email_input = st.text_input("📧 Stark Enterprise Email / ID", value="boss@stark.com")
            pwd_input = st.text_input("🔒 Secure Password", type="password", value="jarvis3000")
            
            st.markdown("#### 📱 Mobile-Style Security Passcode / Pattern")
            pattern_input = st.text_input("Enter 4-Digit Security Passcode (e.g., 3000)", type="password", max_chars=4, value="3000")
            
            btn_label = "🔓 Bypass Security & Access Vault" if auth_mode == "🔑 Login Existing Account" else "🚀 Initialize New Stark Account"
            submitted = st.form_submit_button(btn_label, use_container_width=True)
            
            if submitted:
                if not email_input or not pwd_input or not pattern_input:
                    st.error("Boss, all security vectors (Email, Password, & Passcode) are mandatory!")
                elif auth_mode == "✨ Create New Stark ID":
                    if email_input in st.session_state.registered_users:
                        st.warning("Account already exists in Stark Database! Please switch to 'Login Existing Account'.")
                    else:
                        st.session_state.registered_users[email_input] = {
                            "password": pwd_input,
                            "pattern": pattern_input
                        }
                        st.session_state.authenticated = True
                        st.session_state.current_user = email_input
                        st.success("New Stark ID generated successfully! Initializing Mark VII Matrix...")
                        st.rerun()
                else:  # Login Mode
                    if email_input in st.session_state.registered_users:
                        user_data = st.session_state.registered_users[email_input]
                        if user_data["password"] == pwd_input and user_data["pattern"] == pattern_input:
                            st.session_state.authenticated = True
                            st.session_state.current_user = email_input
                            st.success(f"Authentication Verified. Welcome back, Boss ({email_input}).")
                            st.rerun()
                        else:
                            st.error("Security Breach Alert: Incorrect Password or 4-Digit Passcode!")
                    else:
                        st.error("Stark ID not recognized in database! Please create a new account.")
    st.stop()

# --- MAIN APP (Runs only after secure authentication) ---

# Stark-Grade Header & Cinematic Aura
st.title("🛡️ Project JARVIS: Autonomous Vault & Advanced AI Assistant")
st.markdown(f"### *Architect: Tony Stark | Authenticated User: **{st.session_state.current_user}** | Privacy Protocol Active*")
st.markdown("---")

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

# Sidebar for System Diagnostics & File-Aware AI Query Bot
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/iron-man.png", width=80)
    st.markdown("### Stark Command Hub")
    st.info(f"User: {st.session_state.current_user}")
    st.markdown(f"**Vault Records:** {len(st.session_state.vault)}")
    st.markdown(f"**Student Tasks:** {len(st.session_state.student_tasks)}")
    st.markdown("---")
    
    # Secure Logout Button
    if st.button("🚪 Secure Session Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.current_user = None
        st.success("Session locked securely under Stark protocols.")
        st.rerun()

    st.markdown("---")
    st.markdown("### 🤖 Stark File Intelligence Bot")
    st.markdown("Type any uploaded file name or task keyword below to find its live status:")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
                
    if user_query := st.chat_input("Enter file name or query..."):
        st.session_state.messages.append({"role": "user", "content": user_query})
        q_lower = user_query.lower()
        
        matched_items = [
            item for item in all_active_records 
            if q_lower in item.get('name', '').lower() or q_lower in item.get('title', '').lower() or q_lower in item.get('desc', '').lower()
        ]
        
        if len(matched_items) > 0:
            bot_reply = f"Boss, found {len(matched_items)} matching record(s) in the Stark database:\n"
            for m in matched_items:
                m_name = m.get('name', m.get('title'))
                bot_reply += f"\n- **{m_name}** | Deadline: *{m['deadline']}* | Urgency: **{m['urgency_score']}% ({m['urgency_label']})**"
        elif "urgent" in q_lower or "deadline" in q_lower or "omega" in q_lower:
            if len(all_active_records) > 0:
                top_item = max(all_active_records, key=lambda x: x.get('urgency_score', 0))
                name_key = top_item.get('name', top_item.get('title'))
                bot_reply = f"Boss, your most urgent asset is **{name_key}** with an urgency rating of **{top_item['urgency_score']}%** due on **{top_item['deadline']}**."
            else:
                bot_reply = "Boss, no active files or deadlines registered in the system."
        else:
            bot_reply = f"I scanned all vault records and tasks for '{user_query}', but no exact name match was found. Try entering the exact file name!"
            
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.rerun()

    st.markdown("---")
    if st.button("🗑️ Purge All Data"):
        st.session_state.vault = []
        st.session_state.student_tasks = []
        st.rerun()

# Dual Tabs: Enterprise Vault vs Student Hub
tab1, tab2 = st.tabs(["📁 Enterprise / General Vault", "🎓 Student Homework & Exam Hub"])

with tab1:
    st.subheader("📥 Secure Document & File Ingestion Portal")
    st.markdown("Upload PDFs or documents to trigger autonomous deadline tracking and real-time notifications.")
    
    with st.form("vault_form", clear_on_submit=True):
        uploaded_file = st.file_uploader("Upload PDF, Text Document, or Image", type=["pdf", "txt", "png", "jpg", "jpeg"])
        
        st.markdown("#### ⏰ Set Deadline Date & Time")
        col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
        with col_f1:
            dl_date = st.date_input("Deadline Date")
        with col_f2:
            dl_time = st.time_input("Deadline Time (12-Hour)", value=datetime.strptime("12:00 PM", "%I:%M %p").time())
        with col_f3:
            ampm_choice = st.selectbox("AM / PM", ["AM", "PM"])
            
        submit_vault = st.form_submit_button("🚀 Ingest & Activate Notifications")
        
        if submit_vault and uploaded_file is not None:
            try:
                if uploaded_file.type in ["image/png", "image/jpg", "image/jpeg"]:
                    file_content = uploaded_file
                elif uploaded_file.type == "text/plain" or uploaded_file.name.endswith('.txt'):
                    file_content = uploaded_file.getvalue().decode("utf-8", errors="ignore")
                else:
                    file_content = f"Binary payload for {uploaded_file.name}"
            except Exception:
                file_content = "Encrypted payload."

            base_time_str = dl_time.strftime("%I:%M")
            time_formatted = f"{base_time_str} {ampm_choice}"
            deadline_str = f"{dl_date} at {time_formatted}"
            
            hour_val = dl_time.hour
            if ampm_choice == "PM" and hour_val < 12:
                hour_val += 12
            elif ampm_choice == "AM" and hour_val == 12:
                hour_val = 0
            
            adjusted_time = dl_time.replace(hour=hour_val)
            deadline_dt = datetime.combine(dl_date, adjusted_time)
            current_dt = datetime.now()
            total_sec = (deadline_dt - current_dt).total_seconds()
            
            if total_sec <= 0:
                urgency_score = 100.0
                urgency_label = "🚨 OMEGA EXPIRED"
            else:
                max_window = 604800.0
                urgency_score = round(max(0.0, min(100.0, (1.0 - (total_sec / max_window)) * 100.0)), 1)
                if urgency_score >= 90.0:
                    urgency_label = "🔥 OMEGA 90%+ CRITICAL"
                elif total_sec < 86400:
                    urgency_label = "🔥 High Priority"
                elif total_sec < 259200:
                    urgency_label = "⚠️ Moderate Priority"
                else:
                    urgency_label = "✅ Safe Priority"

            doc_record = {
                "name": uploaded_file.name,
                "type": uploaded_file.type,
                "content": file_content,
                "deadline": deadline_str,
                "urgency_score": urgency_score,
                "urgency_label": urgency_label,
                "upload_time": current_dt.strftime("%Y-%m-%d %I:%M %p")
            }
            st.session_state.vault.append(doc_record)
            st.success(f"Successfully ingested '{uploaded_file.name}' and scheduled active notifications!")

    st.markdown("---")
    st.subheader("📋 Prioritized Vault Archive & Notification Matrix")

    if len(st.session_state.vault) > 0:
        sorted_vault = sorted(st.session_state.vault, key=lambda x: x['urgency_score'], reverse=True)
        for idx, doc in enumerate(sorted_vault):
            border_col = "#ff0000" if doc['urgency_score'] >= 90.0 else "#00ffcc"
            st.markdown(f"""
            <div style="background-color: #1e1e2f; padding: 18px; border-radius: 12px; border-left: 6px solid {border_col}; margin-bottom: 18px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                <h4 style="color: #ffffff; margin-top: 0;">📁 {doc['name']}</h4>
                <p style="color: #a0a0a0; font-size: 13px; margin: 4px 0;"><b>Ingested:</b> {doc['upload_time']}</p>
                <hr style="border-color: #33334d; margin: 8px 0;">
                <p style="color: #ffcc00; margin: 4px 0;"><b>🎯 Deadline:</b> {doc['deadline']}</p>
                <p style="color: {'#ff4b4b' if doc['urgency_score'] >= 90.0 else '#00ffcc'}; margin: 4px 0;"><b>⚡ Urgency Rating:</b> {doc['urgency_score']}% ({doc['urgency_label']})</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander(f"🔍 View File & Notification Controls for {doc['name']}"):
                if "image" in doc['type']:
                    st.image(doc['content'], caption=doc['name'], use_column_width=True)
                else:
                    st.text_area("File Content Preview", str(doc['content']), height=120, key=f"preview_v_{idx}")
                if st.button(f"🗑️ Delete Record", key=f"del_vault_{idx}"):
                    st.session_state.vault.remove(doc)
                    st.rerun()
    else:
        st.info("Vault is empty. Upload documents above to initialize notification streams.")

with tab2:
    st.subheader("🎓 Student Homework, Project & Exam Hub")
    st.markdown("Log exams or assignments to receive real-time Stark notifications and priority alerts.")

    with st.form("student_task_form", clear_on_submit=True):
        t_title = st.text_input("Task / Exam / Assignment Title (e.g., C Programming Practical)")
        t_desc = st.text_area("Task Description & Notes")
        
        tc1, tc2, tc3 = st.columns([2, 1, 1])
        with tc1:
            t_date = st.date_input("Deadline Date", key="st_date")
        with tc2:
            t_time = st.time_input("Deadline Time (12-Hour)", value=datetime.strptime("12:00 PM", "%I:%M %p").time(), key="st_time")
        with tc3:
            t_ampm = st.selectbox("AM / PM", ["AM", "PM"], key="st_ampm")
            
        submit_task = st.form_submit_button("🚀 Log Task & Enable Reminders")
        
        if submit_task and t_title:
            t_base_fmt = t_time.strftime("%I:%M")
            t_time_fmt = f"{t_base_fmt} {t_ampm}"
            t_deadline_str = f"{t_date} at {t_time_fmt}"
            
            t_hour_val = t_time.hour
            if t_ampm == "PM" and t_hour_val < 12:
                t_hour_val += 12
            elif t_ampm == "AM" and t_hour_val == 12:
                t_hour_val = 0
            
            t_adjusted_time = t_time.replace(hour=t_hour_val)
            t_dt = datetime.combine(t_date, t_adjusted_time)
            cur_dt = datetime.now()
            sec_diff = (t_dt - cur_dt).total_seconds()
            
            if sec_diff <= 0:
                t_score = 100.0
                t_label = "🚨 OMEGA EXPIRED"
            else:
                t_score = round(max(0.0, min(100.0, (1.0 - (sec_diff / 604800.0)) * 100.0)), 1)
                if t_score >= 90.0:
                    t_label = "🔥 OMEGA 90%+ CRITICAL"
                elif sec_diff < 86400:
                    t_label = "🔥 High Priority"
                else:
                    t_label = "✅ Safe Priority"

            task_record = {
                "title": t_title,
                "desc": t_desc,
                "deadline": t_deadline_str,
                "urgency_score": t_score,
                "urgency_label": t_label,
                "created": cur_dt.strftime("%Y-%m-%d %I:%M %p")
            }
            st.session_state.student_tasks.append(task_record)
            st.success("Student task logged! Autonomous notification stream updated.")

    st.markdown("---")
    st.subheader("📋 Prioritized Student Task & Notification Stream")

    if len(st.session_state.student_tasks) > 0:
        sorted_tasks = sorted(st.session_state.student_tasks, key=lambda x: x['urgency_score'], reverse=True)
        for s_idx, task in enumerate(sorted_tasks):
            t_border_col = "#ff0000" if task['urgency_score'] >= 90.0 else "#ffcc00"
            st.markdown(f"""
            <div style="background-color: #1e1e2f; padding: 18px; border-radius: 12px; border-left: 6px solid {t_border_col}; margin-bottom: 18px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                <h4 style="color: #ffffff; margin-top: 0;">📌 {task['title']}</h4>
                <p style="color: #a0a0a0; font-size: 13px; margin: 4px 0;"><b>Logged:</b> {task['created']}</p>
                <p style="color: #ffffff; margin: 6px 0;">{task['desc']}</p>
                <hr style="border-color: #33334d; margin: 8px 0;">
                <p style="color: #ffcc00; margin: 4px 0;"><b>🎯 Deadline:</b> {task['deadline']}</p>
                <p style="color: {'#ff4b4b' if task['urgency_score'] >= 90.0 else '#00ffcc'}; margin: 4px 0;"><b>⚡ Urgency Rating:</b> {task['urgency_score']}% ({task['urgency_label']})</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("❌ Mark Completed / Remove", key=f"del_st_{s_idx}"):
                st.session_state.student_tasks.remove(task)
                st.rerun()
    else:
        st.info("No active student reminders or notifications logged yet.")
