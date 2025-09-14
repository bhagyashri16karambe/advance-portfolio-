import streamlit as st
from jinja2 import Environment, FileSystemLoader
import os
import base64
from io import BytesIO

template_dir = "templates"
template_files = [f for f in os.listdir(template_dir) if f.endswith('.html')]
env = Environment(loader=FileSystemLoader(template_dir))

st.set_page_config(layout="wide")

def reset_form():
    st.session_state.projects = []
    st.session_state.skills = []
    st.session_state.education = []
    st.session_state.certifications = []
    st.rerun()

st.markdown(
    """
    <style>
    /* Dark Mode (Default) */
    .stApp {
        background-color: #0d0c1d;
        background-image:
            radial-gradient(at 0% 0%, hsla(271,76%,65%,0.3) 0, transparent 50%),
            radial-gradient(at 100% 0%, hsla(202,78%,60%,0.3) 0, transparent 50%),
            radial-gradient(at 50% 100%, hsla(339,78%,60%,0.3) 0, transparent 50%);
        background-attachment: fixed;
    }
    
    .st-emotion-cache-18ni4h0, .st-emotion-cache-1j0k8c7, .st-emotion-cache-13k65w4, .st-emotion-cache-n6t363, .st-emotion-cache-z50536 {
        background: rgba(40, 40, 60, 0.4) !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
        color: #e0e0f0;
    }
    
    h1, h2, h3, h4, h5, h6, .st-emotion-cache-1c9j410 {
        color: #a0a0ff;
        text-shadow: 0 0 5px rgba(160, 160, 255, 0.5);
    }
    
    .stButton > button {
        background-color: #6a5acd;
        border: none;
        color: white;
        padding: 10px 24px;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #8a7acd;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(106, 90, 205, 0.4);
    }

    /* Light Mode Specific Styles */
    @media (prefers-color-scheme: light) {
      .stApp {
          background-color: #f0f2f6;
          background-image: none;
      }
      .st-emotion-cache-18ni4h0, .st-emotion-cache-1j0k8c7, .st-emotion-cache-13k65w4, .st-emotion-cache-n6t363, .st-emotion-cache-z50536 {
          background: rgba(40, 40, 60, 0.6) !important;
          border: 1px solid rgba(0, 0, 0, 0.1);
          color: #f0f0f0;
      }
      h1, h2, h3, h4, h5, h6, .st-emotion-cache-1c9j410 {
          color: #333;
          text-shadow: none;
      }
    }
    
    /* Animations (Common for both themes) */
    @keyframes particle-glow {
        0% { transform: scale(1); opacity: 0.7; }
        50% { transform: scale(1.2); opacity: 1; }
        100% { transform: scale(1); opacity: 0.7; }
    }
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, #2a2a4a 0%, transparent 100%);
        opacity: 0.8;
        z-index: -1;
        animation: particle-glow 10s infinite ease-in-out;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.title("Premium Portfolio Generator")
st.markdown("Craft and preview your professional portfolio with a seamless, live-editing experience.")

col_forms, col_preview = st.columns([1, 1.5])

with col_forms:
    st.header("Choose a Website Style")
    selected_template = st.selectbox("Choose a Website Style:", template_files, format_func=lambda x: x.replace('.html', ''))

    st.header("1️ Personal Information")
    col1_1, col1_2 = st.columns(2)
    with col1_1:
        user_name = st.text_input("Full Name", "Enter user name")
        user_title = st.text_input("Title/Tagline", "enter tagline.")
        user_email = st.text_input("Email", "enter email")
        profile_img_file = st.file_uploader("Upload Profile Image", type=["png", "jpg", "jpeg"])
    with col1_2:
        user_description = st.text_area("About Me", "enter about.", height=150)
        user_linkedin = st.text_input("LinkedIn URL", "--e")
        user_github = st.text_input("GitHub URL", "--")

    st.header("2️ Skills")
    if 'skills' not in st.session_state:
        st.session_state.skills = []
    
    with st.expander("Add a New Skill"):
        skill_input = st.text_input("Enter a skill", key="skill_input")
        skill_level = st.slider("Skill Level (%)", 0, 100, 90, key="skill_level")
        if st.button("Add Skill", key="add_skill_btn"):
            if skill_input:
                st.session_state.skills.append({"name": skill_input, "level": f"{skill_level}%"})
                st.success(f"Added skill: '{skill_input}' with level {skill_level}%")
    
    if st.session_state.skills:
        st.write("Current Skills:")
        for skill in st.session_state.skills:
            st.write(f"- {skill['name']} ({skill['level']})")
    
    st.header("3️ Projects")
    if 'projects' not in st.session_state:
        st.session_state.projects = []
    with st.expander(" Add a New Project"):
        project_title = st.text_input("Project Title", key="proj_title")
        project_description = st.text_area("Project Description", key="proj_desc")
        project_link = st.text_input("Project Link (GitHub/Demo)", key="proj_link")
        project_image = st.text_input("Project Image URL (Optional)", key="proj_image")
        if st.button("Add Project", key="add_proj_btn"):
            if project_title and project_description:
                st.session_state.projects.append({
                    "title": project_title,
                    "description": project_description,
                    "link": project_link,
                    "image_url": project_image
                })
    if st.session_state.projects:
        st.write("Current Projects:")
        for idx, project in enumerate(st.session_state.projects):
            st.write(f"**{project['title']}** - {project['link']}")
            st.markdown(f"*{project['description']}*")

    st.header("4️ Education")
    if 'education' not in st.session_state:
        st.session_state.education = []
    with st.expander("🎓 Add New Education"):
        edu_degree = st.text_input("Degree (e.g., B.S. in Computer Science)", key="edu_degree")
        edu_institution = st.text_input("Institution (e.g., University of Tech)", key="edu_institution")
        edu_year = st.text_input("Year of Graduation", key="edu_year")
        if st.button("Add Education", key="add_edu_btn"):
            if edu_degree and edu_institution:
                st.session_state.education.append({
                    "degree": edu_degree,
                    "institution": edu_institution,
                    "year": edu_year
                })
    if st.session_state.education:
        st.write("Current Education:")
        for idx, edu in enumerate(st.session_state.education):
            st.write(f"**{edu['degree']}** from {edu['institution']} ({edu['year']})")
    
    st.header("5️ Certifications")
    if 'certifications' not in st.session_state:
        st.session_state.certifications = []
    with st.expander("Add New Certification"):
        cert_name = st.text_input("Certification Name", key="cert_name")
        if st.button("Add Certification", key="add_cert_btn"):
            if cert_name:
                st.session_state.certifications.append(cert_name)
    if st.session_state.certifications:
        st.write("Current Certifications:", ", ".join(st.session_state.certifications))

    st.header("Generate & Download")
    if st.button("⬇ Download Portfolio", use_container_width=True):
        user_data = {
            'name': user_name,
            'title': user_title,
            'description': user_description,
            'email': user_email,
            'linkedin': user_linkedin,
            'github': user_github,
            'skills': st.session_state.skills,
            'projects': st.session_state.projects,
            'education': st.session_state.education,
            'certifications': st.session_state.certifications,
        }
        
        profile_img_base64 = None
        if profile_img_file:
            img_bytes = profile_img_file.getvalue()
            base64_encoded = base64.b64encode(img_bytes).decode("utf-8")
            mime_type = profile_img_file.type
            profile_img_base64 = f"data:{mime_type};base64,{base64_encoded}"

        user_data['profile_img'] = profile_img_base64
        
        # Adjust skills format based on template
        if selected_template in ['mac.html', 'simple_bell.html']:
            user_data['skills'] = [skill['name'] for skill in st.session_state.skills]
        
        template_to_render = env.get_template(selected_template)
        rendered_html = template_to_render.render(user=user_data, **user_data)
        
        file_path = "portfolio.html"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(rendered_html)
        
        st.success("Your portfolio has been generated! Click the button below to download.")
        
        with open(file_path, "rb") as file:
            st.download_button(
                label="Download portfolio.html",
                data=file,
                file_name="portfolio.html",
                mime="text/html",
                use_container_width=True
            )

    st.header("Actions")
    if st.button(" Reset All Data", help="Clears all form fields", use_container_width=True):
        reset_form()

with col_preview:
    st.header("Live Preview")
    
    user_data = {
        'name': user_name,
        'title': user_title,
        'description': user_description,
        'email': user_email,
        'linkedin': user_linkedin,
        'github': user_github,
        'skills': st.session_state.skills,
        'projects': st.session_state.projects,
        'education': st.session_state.education,
        'certifications': st.session_state.certifications,
    }
    
    profile_img_base64 = None
    if profile_img_file:
        img_bytes = profile_img_file.getvalue()
        base64_encoded = base64.b64encode(img_bytes).decode("utf-8")
        mime_type = profile_img_file.type
        profile_img_base64 = f"data:{mime_type};base64,{base64_encoded}"

    user_data['profile_img'] = profile_img_base64

    # Adjust skills format based on template for live preview
    if selected_template in ['mac.html', 'simple_bell.html']:
        user_data['skills'] = [skill['name'] for skill in st.session_state.skills]
    
    template_to_render = env.get_template(selected_template)
    rendered_html = template_to_render.render(user=user_data, **user_data)
    
    st.components.v1.html(rendered_html, height=800, scrolling=True)
