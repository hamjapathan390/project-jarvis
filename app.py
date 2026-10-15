import streamlit as st
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Project JARVIS: AI Vault & Sentinel", page_icon="🛡️", layout="wide")

# Stark-Grade Header
st.title("🛡️ Project JARVIS: Autonomous Vault & Advanced AI Assistant")
st.markdown("### *Digilocker-Class Security, Priority Sorting & Next-Gen Conversational Sentinel.*")
st.markdown("---")

# Initialize Session State
if "vault" not in st.session_state:
    st.session_state.vault = []

if "student_tasks" not in st.session_state:
    st.session_state.student_tasks = []

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello Sir! JARVIS systems online at 100% capacity. Voice command simulation and priority matrix are fully operational."}
    ]

# Sidebar for System Diagnostics & Voice Command Hub
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/iron-man.png", width=80)
    st.markdown("### JARVIS Command Hub")
    st.info("Status: Online & Autonomous [Mark VII Ready]")
    st.markdown(f"**Vault Records:** {len(st.session_state.vault)}")
    st.markdown(f"**Student Tasks:** {len(st.session_state.student_tasks)}")
    st.markdown("---")
    
    st.markdown("### 🎙️ Stark Neural Voice Simulator")
    st.markdown("Simulate voice commands for live hackathon demonstration:")
    
    voice_cmd = st.selectbox(
        "Select Voice Protocol:",
        [
            "-- Select Command --",
            "🗣️ 'JARVIS, run full system diagnostics'",
            "🗣️ 'JARVIS, what is my most urgent deadline?'",
            "🗣️ 'JARVIS, execute security lockdown scan'",
            "🗣️ 'JARVIS, give me a morning briefing'"
        ]
    )
    
    if st.button("🔊 Execute Voice Command"):
        if voice_cmd != "-- Select Command --":
            all_records = st.session_state.vault + st.session_state.student_tasks
            if "diagnostics" in voice_cmd:
                resp = f"Diagnostics Report: Core temp optimal. Vault records: {len(st.session_state.vault)}. Student tasks: {len(st.session_state.student_tasks)}. All security protocols green."
            elif "urgent" in voice_cmd:
                if len(all_records) > 0:
                    top_item = max(all_records, key=lambda x: x.get('urgency_score', 0))
                    name_key = top_item.get('name', top_item.get('title'))
                    resp = f"Sir, most urgent item is **{name_key}** due on **{top_item['deadline']}**."
                else:
                    resp = "Sir, no active records or deadlines found in the database."
            elif "lockdown" in voice_cmd:
                resp = "Security lockdown initiated. Digilocker-class encryption active. Zero vulnerabilities detected."
            else:
                resp = "All systems are running at peak efficiency, Boss. Ready for KRYPTA 2026 presentation."
            
            st.session_state.messages.append({"role": "user", "content": voice_cmd})
            st.session_state.messages.append({"role": "assistant", "content": resp})
            st.rerun()

    st.markdown("---")
    st.markdown("### 💬 JARVIS AI Intelligence")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
                
    if user_query := st.chat_input("Ask JARVIS anything..."):
        st.session_state.messages.append({"role": "user", "content": user_query})
        bot_reply = f"I processed your query: '{user_query}'. All security parameters are stable."
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
    st.markdown("Upload PDFs, text files, or document snapshots for instant priority sorting.")
    
    with st.form("vault_form", clear_on_submit=True):
        uploaded_file = st.file_uploader("Upload PDF, Text Document, or Image", type=["pdf", "txt", "png", "jpg", "jpeg"])
        
        st.markdown("#### ⏰ Set Deadline Date & Time")
        col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
        with col_f1:
            dl_date = st.date_input("Deadline Date")
        with col_f2:
            dl_time = st.time_input("Deadline Time")
        with col_f3:
            ampm_choice = st.selectbox("AM / PM", ["AM", "PM"])
            
        submit_vault = st.form_submit_button("🚀 Ingest & Prioritize Asset")
        
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
            
            deadline_dt = datetime.combine(dl_date, dl_time)
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
            st.success(f"Successfully ingested '{uploaded_file.name}' into Enterprise Vault!")

    st.markdown("---")
    st.subheader("📋 Prioritized Vault Archive (Sorted by Urgency)")

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
            
            with st.expander(f"🔍 View File & Controls for {doc['name']}"):
                if "image" in doc['type']:
                    st.image(doc['content'], caption=doc['name'], use_column_width=True)
                else:
                    st.text_area("File Content Preview", str(doc['content']), height=120, key=f"preview_v_{idx}")
                if st.button(f"🗑️ Delete Record", key=f"del_vault_{idx}"):
                    st.session_state.vault.remove(doc)
                    st.rerun()
    else:
        st.info("Vault is empty. Upload documents above to begin sorting.")

with tab2:
    st.subheader("🎓 Student Homework, Project & Exam Hub")
    st.markdown("Designed for students to instantly log college assignments, exams, or registrations and receive autonomous priority alerts.")

    with st.form("student_task_form", clear_on_submit=True):
        t_title = st.text_input("Task / Exam / Assignment Title (e.g., C Programming Practical)")
        t_desc = st.text_area("Task Description & Notes")
        
        tc1, tc2, tc3 = st.columns([2, 1, 1])
        with tc1:
            t_date = st.date_input("Deadline Date", key="st_date")
        with tc2:
            t_time = st.time_input("Deadline Time", key="st_time")
        with tc3:
            t_ampm = st.selectbox("AM / PM", ["AM", "PM"], key="st_ampm")
            
        submit_task = st.form_submit_button("🚀 Log Student Task")
        
        if submit_task and t_title:
            t_base_fmt = t_time.strftime("%I:%M")
            t_time_fmt = f"{t_base_fmt} {t_ampm}"
            t_deadline_str = f"{t_date} at {t_time_fmt}"
            
            t_dt = datetime.combine(t_date, t_time)
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
            st.success("Student task successfully logged into the priority matrix!")

    st.markdown("---")
    st.subheader("📋 Prioritized Student Task Stream")

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
        st.info("No active student reminders logged yet.")
