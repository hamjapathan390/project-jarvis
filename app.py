import streamlit as st
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Project JARVIS: AI Vault & Sentinel", page_icon="🛡️", layout="wide")

# Stark-Grade Header & Cinematic Aura
st.title("🛡️ Project JARVIS: Autonomous Vault & Advanced AI Assistant")
st.markdown("### *Digilocker-Class Security, Autonomous Reminders & Next-Gen Conversational Sentinel.*")
st.markdown("---")

# Initialize Session State
if "vault" not in st.session_state:
    st.session_state.vault = []

if "student_tasks" not in st.session_state:
    st.session_state.student_tasks = []

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello Boss! JARVIS systems online at 100% capacity. Autonomous notification matrix and priority monitoring are active."}
    ]

# Combine all records for global notification checks
all_active_records = st.session_state.vault + st.session_state.student_tasks

# --- TONY STARK AURA: LIVE URGENT NOTIFICATION BANNER ---
if len(all_active_records) > 0:
    urgent_items = [item for item in all_active_records if item.get('urgency_score', 0) >= 70.0]
    if len(urgent_items) > 0:
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #ff4b4b, #ff9900); padding: 14px 20px; border-radius: 10px; color: white; font-weight: bold; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(255,75,75,0.4);">
            🚨 STARK SECURITY ALERT: {len(urgent_items)} Critical Deadlines Require Immediate Boss Attention! Check Priority Matrix below.
        </div>
        """, unsafe_allow_html=True)

# Sidebar for System Diagnostics & Autonomous Notification Hub
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/iron-man.png", width=80)
    st.markdown("### JARVIS Command Hub")
    st.info("Status: Online & Autonomous [Mark VII Ready]")
    st.markdown(f"**Vault Records:** {len(st.session_state.vault)}")
    st.markdown(f"**Student Tasks:** {len(st.session_state.student_tasks)}")
    st.markdown("---")
    
    st.markdown("### 🔔 Autonomous Notification Stream")
    if len(all_active_records) > 0:
        notif_sorted = sorted(all_active_records, key=lambda x: x['urgency_score'], reverse=True)[:3]
        for n_item in notif_sorted:
            n_name = n_item.get('name', n_item.get('title'))
            st.warning(f"⚠️ **{n_name}**\nDue: {n_item['deadline']}")
    else:
        st.success("All systems clear. No pending threat alerts.")

    st.markdown("---")
    st.markdown("### 💬 JARVIS AI Intelligence")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
                
    if user_query := st.chat_input("Ask JARVIS anything..."):
        st.session_state.messages.append({"role": "user", "content": user_query})
        q_lower = user_query.lower()
        
        if "urgent" in q_lower or "deadline" in q_lower or "notify" in q_lower:
            if len(all_active_records) > 0:
                top_item = max(all_active_records, key=lambda x: x.get('urgency_score', 0))
                name_key = top_item.get('name', top_item.get('title'))
                bot_reply = f"Boss, your most urgent notification is for **{name_key}** due on **{top_item['deadline']}**."
            else:
                bot_reply = "Boss, no active notifications or deadlines registered in the system."
        else:
            bot_reply = f"I processed your query: '{user_query}'. All notification radars are actively scanning your schedules."
            
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

            # Format 12-hour time correctly
            base_time_str = dl_time.strftime("%I:%M")
            time_formatted = f"{base_time_str} {ampm_choice}"
            deadline_str = f"{dl_date} at {time_formatted}"
            
            # Convert to 24-hour for accurate urgency calculation
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
                urgency_label = "🚨 EXPIRED"
            else:
                max_window = 604800.0
                urgency_score = round(max(0.0, min(100.0, (1.0 - (total_sec / max_window)) * 100.0)), 1)
                if total_sec < 86400:
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
            st.markdown(f"""
            <div style="background-color: #1e1e2f; padding: 18px; border-radius: 12px; border-left: 6px solid #00ffcc; margin-bottom: 18px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                <h4 style="color: #ffffff; margin-top: 0;">📁 {doc['name']}</h4>
                <p style="color: #a0a0a0; font-size: 13px; margin: 4px 0;"><b>Ingested:</b> {doc['upload_time']}</p>
                <hr style="border-color: #33334d; margin: 8px 0;">
                <p style="color: #ffcc00; margin: 4px 0;"><b>🎯 Deadline:</b> {doc['deadline']}</p>
                <p style="color: #00ffcc; margin: 4px 0;"><b>⚡ Urgency Rating:</b> {doc['urgency_score']}% ({doc['urgency_label']})</p>
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
                t_label = "🚨 EXPIRED"
            else:
                t_score = round(max(0.0, min(100.0, (1.0 - (sec_diff / 604800.0)) * 100.0)), 1)
                t_label = "🔥 High Priority" if sec_diff < 86400 else "✅ Safe Priority"

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
            st.markdown(f"""
            <div style="background-color: #1e1e2f; padding: 18px; border-radius: 12px; border-left: 6px solid #ffcc00; margin-bottom: 18px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                <h4 style="color: #ffffff; margin-top: 0;">📌 {task['title']}</h4>
                <p style="color: #a0a0a0; font-size: 13px; margin: 4px 0;"><b>Logged:</b> {task['created']}</p>
                <p style="color: #ffffff; margin: 6px 0;">{task['desc']}</p>
                <hr style="border-color: #33334d; margin: 8px 0;">
                <p style="color: #ffcc00; margin: 4px 0;"><b>🎯 Deadline:</b> {task['deadline']}</p>
                <p style="color: #00ffcc; margin: 4px 0;"><b>⚡ Urgency Rating:</b> {task['urgency_score']}% ({task['urgency_label']})</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("❌ Mark Completed / Remove", key=f"del_st_{s_idx}"):
                st.session_state.student_tasks.remove(task)
                st.rerun()
    else:
        st.info("No active student reminders or notifications logged yet.")
