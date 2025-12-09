import streamlit as st
from data import dashboard_api as api
from utils import to_df


def render():
    st.header("🔎 Explorer")
    st.info("Explorer tools for drilling into sessions, assignments and students.")
    with st.spinner("Loading courses..."):
        courses = api.get_courses()
        course_options = [c['name'] for c in courses]
    sel = st.selectbox("Select Course", ["All Courses"] + course_options)

    st.markdown("---")
    st.subheader("Sessions (example)")
    if sel != "All Courses":
        course_id = next((c['id'] for c in courses if c['name'] == sel), None)
        with st.spinner("Loading sessions..."):
            modules = api.get_modules_for_course(course_id)
            if modules:
                session_df = api.get_sessions_for_module(course_id, modules[0]['id'])
                st.dataframe(session_df)
            else:
                st.info("No modules for course")
    else:
        st.info("Select a course to view sessions")
