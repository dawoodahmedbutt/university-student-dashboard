import streamlit as st
from data import dashboard_api as api
import pandas as pd


def render_course_table(table_placeholder):
    """Render the course table with CRUD operations."""
    with st.spinner("Loading courses..."):
        courses_df = api.list_courses()

    # Add search bar for filtering courses
    search_query = st.text_input("🔍 Search courses", value="", help="Type part of a course name, director, or ID to filter the table.")
    
    # Create placeholder for table after search bar
    table_placeholder = st.empty()
    
    filtered_df = courses_df.copy()
    if search_query and not courses_df.empty:
        q = search_query.strip().lower()
        # Filter by name, director, education level, or ID
        mask = (
            filtered_df.get('course_name','').astype(str).str.lower().str.contains(q)
            | filtered_df.get('course_director','').astype(str).str.lower().str.contains(q)
            | filtered_df.get('education_level','').astype(str).str.lower().str.contains(q)
            | filtered_df.get('course_id','').astype(str).str.contains(q)
        )
        filtered_df = filtered_df[mask]

    if not filtered_df.empty:
        display_cols = ['course_id', 'course_name', 'course_director', 'education_level']
        available_cols = [col for col in display_cols if col in filtered_df.columns]
        table_placeholder.dataframe(filtered_df[available_cols], use_container_width=True, height=400, hide_index=True)

        # Delete, Update, Create operations
        render_delete_course(courses_df, table_placeholder, display_cols, search_query)
        render_update_course(courses_df, table_placeholder, display_cols, search_query)
    else:
        table_placeholder.info("No courses found")

    render_create_course(table_placeholder, search_query)


def render_delete_course(courses_df, table_placeholder, display_cols, search_query):
    """Render delete form for courses."""
    st.markdown("### Delete course by ID")
    with st.form("delete_course_form"):
        id_input = st.text_input("Course ID to delete", value="", help="Type the numeric course id and press Delete")
        course_row = None
        if id_input and id_input.strip():
            try:
                cid_search = int(id_input.strip())
                matches = courses_df[courses_df.get('course_id') == cid_search]
                if not matches.empty:
                    course_row = matches.iloc[0]
                    st.write(f"Found: **{course_row.get('course_name')}** (ID: {cid_search})")
                else:
                    st.warning("No course found with that ID")
            except Exception:
                st.error("Please enter a valid numeric course ID")

        confirm = st.checkbox("I confirm deletion of the above course")
        submitted_del = st.form_submit_button("Delete by ID")
        if submitted_del:
            if course_row is None:
                st.error("Enter a valid course ID before deleting.")
            elif not confirm:
                st.error("Please confirm deletion by checking the box.")
            else:
                cid = int(course_row.get('course_id'))
                with st.spinner("Deleting course..."):
                    res = api.delete_course(cid)

                if res is True:
                    try:
                        st.cache_data.clear()
                    except Exception:
                        pass
                    st.success(f"Course {cid} deleted")
                    refresh_course_table(table_placeholder, display_cols, search_query)
                else:
                    st.error("Failed to delete course.")


def render_update_course(courses_df, table_placeholder, display_cols, search_query):
    """Render update form for courses."""
    st.markdown("### Update course by ID")
    st.info("Update feature: Enter course ID, load fields, modify, and submit.")
    with st.form("update_course_form"):
        update_id_input = st.text_input("Course ID to update", value="", help="Type numeric course id and press Load")
        load_clicked = st.form_submit_button("Load Course")

        loaded_row = None
        if load_clicked:
            if not update_id_input or not update_id_input.strip():
                st.error("Enter a numeric course ID to load.")
            else:
                try:
                    cid_lookup = int(update_id_input.strip())
                    matches = courses_df[courses_df.get('course_id') == cid_lookup]
                    if matches.empty:
                        st.warning("No course found with that ID")
                    else:
                        loaded_row = matches.iloc[0]
                except Exception:
                    st.error("Please enter a valid numeric course ID")

        if loaded_row is not None:
            st.session_state['update_course_name_field'] = loaded_row.get('course_name', '')
            st.session_state['update_course_director_field'] = loaded_row.get('course_director', '')
            st.session_state['update_education_level_field'] = loaded_row.get('education_level', '')

        # Editable inputs
        upd_name = st.text_input("Course Name *", value=st.session_state.get('update_course_name_field', ''), help="Required")
        upd_director = st.text_input("Course Director *", value=st.session_state.get('update_course_director_field', ''), help="Required")
        upd_level = st.text_input("Education Level *", value=st.session_state.get('update_education_level_field', ''), help="Required")

        submit_update = st.form_submit_button("Submit Update")
        if submit_update:
            try:
                cid = int(update_id_input.strip())
            except Exception:
                st.error("Enter a valid numeric course ID in the top field before submitting updates.")
                cid = None

            if cid is not None:
                if not upd_name or not upd_director or not upd_level:
                    st.error("All fields are required.")
                    cid = None

            if cid is not None:
                updates = {
                    "course_name": upd_name,
                    "course_director": upd_director,
                    "education_level": upd_level
                }
                with st.spinner("Updating course..."):
                    res = api.update_course(cid, updates)

                success = bool(res)
                if success:
                    try:
                        st.cache_data.clear()
                    except Exception:
                        pass
                    st.session_state['update_course_name_field'] = ''
                    st.session_state['update_course_director_field'] = ''
                    st.session_state['update_education_level_field'] = ''
                    st.success(f"Course {cid} updated")
                    refresh_course_table(table_placeholder, display_cols, search_query)
                else:
                    err_msg = ''
                    if isinstance(res, dict):
                        err_msg = res.get('message') or res.get('error') or ''
                    st.error(f"Failed to update course. {err_msg}")


def render_create_course(table_placeholder, search_query):
    """Render create form for courses."""
    st.markdown("---")
    st.subheader("Create New Course")
    with st.form("create_course"):
        name = st.text_input("Course Name *", help="Required")
        director = st.text_input("Course Director *", help="Required")
        level = st.text_input("Education Level *", help="Required (e.g., Undergraduate, Postgraduate)")
        
        submitted = st.form_submit_button("Create")
        if submitted:
            if not name or not director or not level:
                st.error("All fields are required.")
            else:
                new = {
                    "course_name": name,
                    "course_director": director,
                    "education_level": level
                }
                result = api.create_course(new)

                created = False
                if isinstance(result, dict):
                    succ = result.get("success")
                    if succ is True or (isinstance(succ, str) and succ.lower() == "true"):
                        created = True
                    if result.get("course"):
                        created = True

                if created:
                    try:
                        st.cache_data.clear()
                    except Exception:
                        pass
                    st.success("Course created successfully!")
                    
                    display_cols = ['course_id', 'course_name', 'course_director', 'education_level']
                    refresh_course_table(table_placeholder, display_cols, search_query)
                else:
                    err_msg = ""
                    if isinstance(result, dict):
                        err_msg = result.get("message") or result.get("error") or ""
                    st.error(f"Failed to create course. {err_msg}")


def refresh_course_table(table_placeholder, display_cols, search_query):
    """Helper to refresh course table."""
    courses_df = api.list_courses()
    filtered_df = courses_df.copy()
    
    if search_query and not courses_df.empty:
        q = search_query.strip().lower()
        mask = (
            filtered_df.get('course_name','').astype(str).str.lower().str.contains(q)
            | filtered_df.get('course_director','').astype(str).str.lower().str.contains(q)
            | filtered_df.get('education_level','').astype(str).str.lower().str.contains(q)
            | filtered_df.get('course_id','').astype(str).str.contains(q)
        )
        filtered_df = filtered_df[mask]
    
    if not filtered_df.empty:
        available_cols = [col for col in display_cols if col in courses_df.columns]
        table_placeholder.dataframe(filtered_df[available_cols], use_container_width=True, height=400, hide_index=True)
    else:
        table_placeholder.info("No courses found")
