import streamlit as st
from data import dashboard_api as api
import pandas as pd


def render_student_table(table_placeholder):
    """Render the student table with CRUD operations."""
    with st.spinner("Loading students..."):
        students_df = api.list_students()

    # Add search bar for filtering students
    search_query = st.text_input("🔍 Search students", value="", help="Type part of a name, email, or ID to filter the table.")
    
    # Create placeholder for table after search bar
    table_placeholder = st.empty()
    
    filtered_df = students_df.copy()
    if search_query and not students_df.empty:
        q = search_query.strip().lower()
        # Filter by name, email, or ID
        mask = (
            filtered_df.get('first_name','').astype(str).str.lower().str.contains(q)
            | filtered_df.get('last_name','').astype(str).str.lower().str.contains(q)
            | filtered_df.get('email','').astype(str).str.lower().str.contains(q)
            | filtered_df.get('student_id','').astype(str).str.contains(q)
        )
        filtered_df = filtered_df[mask]

    if not filtered_df.empty:
        display_cols = ['student_id', 'first_name', 'last_name', 'email', 'course_name', 'year_of_study', 'address']
        available_cols = [col for col in display_cols if col in filtered_df.columns]
        table_placeholder.dataframe(filtered_df[available_cols], use_container_width=True, height=400, hide_index=True)

        # Delete, Update, Create operations
        render_delete_student(students_df, table_placeholder, display_cols, search_query)
        render_update_student(students_df, table_placeholder, display_cols, search_query)
    else:
        table_placeholder.info("No students found")

    render_create_student(table_placeholder, search_query)


def render_delete_student(students_df, table_placeholder, display_cols, search_query):
    """Render delete form for students."""
    st.markdown("### Delete student by ID")
    with st.form("delete_student_form"):
        id_input = st.text_input("Student ID to delete", value="", help="Type the numeric student id and press Delete")
        student_row = None
        if id_input and id_input.strip():
            try:
                sid_search = int(id_input.strip())
                matches = students_df[(students_df.get('student_id') == sid_search) | (students_df.get('id') == sid_search)]
                if not matches.empty:
                    student_row = matches.iloc[0]
                    st.write(f"Found: **{student_row.get('first_name')} {student_row.get('last_name')}** ({student_row.get('email')})")
                else:
                    st.warning("No student found with that ID")
            except Exception:
                st.error("Please enter a valid numeric student ID")

        confirm = st.checkbox("I confirm deletion of the above student")
        submitted_del = st.form_submit_button("Delete by ID")
        if submitted_del:
            if student_row is None:
                st.error("Enter a valid student ID before deleting.")
            elif not confirm:
                st.error("Please confirm deletion by checking the box.")
            else:
                sid = int(student_row.get('student_id') or student_row.get('id'))
                with st.spinner("Deleting student..."):
                    res = api.delete_student_crud(sid)

                if res is True:
                    try:
                        st.cache_data.clear()
                    except Exception:
                        pass
                    st.success(f"Student {sid} deleted")
                    # refresh table
                    refresh_student_table(table_placeholder, display_cols, search_query)
                else:
                    st.error("Failed to delete student.")


def render_update_student(students_df, table_placeholder, display_cols, search_query):
    """Render update form for students."""
    st.markdown("### Update student by ID")
    st.info("Update feature: Enter student ID, load fields, modify, and submit.")
    with st.form("update_student_form"):
        update_id_input = st.text_input("Student ID to update", value="", help="Type numeric student id and press Load")
        load_clicked = st.form_submit_button("Load Student")

        loaded_row = None
        if load_clicked:
            if not update_id_input or not update_id_input.strip():
                st.error("Enter a numeric student ID to load.")
            else:
                try:
                    sid_lookup = int(update_id_input.strip())
                    matches = students_df[(students_df.get('student_id') == sid_lookup) | (students_df.get('id') == sid_lookup)]
                    if matches.empty:
                        st.warning("No student found with that ID")
                    else:
                        loaded_row = matches.iloc[0]
                except Exception:
                    st.error("Please enter a valid numeric student ID")

        if loaded_row is not None:
            st.session_state['update_first'] = loaded_row.get('first_name', '')
            st.session_state['update_last'] = loaded_row.get('last_name', '')
            st.session_state['update_email'] = loaded_row.get('email', '')
            st.session_state['update_address'] = loaded_row.get('address', '')
            st.session_state['update_year'] = int(loaded_row.get('year_of_study', 1))
            
            courses = api.get_courses()
            course_options = {c['name']: c['id'] for c in courses}
            current_course_name = loaded_row.get('course_name', '')
            if current_course_name not in course_options:
                current_course_id = loaded_row.get('course_id')
                if current_course_id is not None:
                    for k, v in course_options.items():
                        if v == current_course_id:
                            current_course_name = k
                            break
            st.session_state['update_course_name'] = current_course_name

        # Editable inputs
        upd_first = st.text_input("First Name *", value=st.session_state.get('update_first', ''), help="Required")
        upd_last = st.text_input("Last Name *", value=st.session_state.get('update_last', ''), help="Required")
        upd_email = st.text_input("Email *", value=st.session_state.get('update_email', ''), help="Required")
        upd_address = st.text_input("Address *", value=st.session_state.get('update_address', ''), help="Required")
        upd_year = st.number_input("Year of Study *", min_value=1, max_value=4, value=st.session_state.get('update_year', 1), help="Required")
        
        course_options = {c['name']: c['id'] for c in api.get_courses()}
        course_names = list(course_options.keys())
        if not course_names:
            st.warning("No courses available to assign.")
            selected_course_name = ''
        else:
            default_course = st.session_state.get('update_course_name', course_names[0])
            if default_course not in course_names:
                default_course = course_names[0]
            selected_course_name = st.selectbox("Course *", course_names, index=course_names.index(default_course), help="Required")

        submit_update = st.form_submit_button("Submit Update")
        if submit_update:
            try:
                sid = int(update_id_input.strip())
            except Exception:
                st.error("Enter a valid numeric student ID in the top field before submitting updates.")
                sid = None

            if sid is not None:
                if not upd_first or not upd_last or not upd_email or not upd_address:
                    st.error("All fields marked with * are required.")
                    sid = None

            if sid is not None:
                updates = {
                    "first_name": upd_first,
                    "last_name": upd_last,
                    "email": upd_email,
                    "address": upd_address,
                    "year_of_study": int(upd_year),
                    "course_id": course_options.get(selected_course_name)
                }
                with st.spinner("Updating student..."):
                    res = api.update_student(sid, updates)

                success = bool(res)
                if success:
                    try:
                        st.cache_data.clear()
                    except Exception:
                        pass
                    # Clear form fields
                    st.session_state['update_first'] = ''
                    st.session_state['update_last'] = ''
                    st.session_state['update_email'] = ''
                    st.session_state['update_address'] = ''
                    st.session_state['update_year'] = 1
                    st.session_state['update_course_name'] = ''
                    st.success(f"Student {sid} updated")
                    refresh_student_table(table_placeholder, display_cols, search_query)
                else:
                    err_msg = ''
                    if isinstance(res, dict):
                        err_msg = res.get('message') or res.get('error') or ''
                    st.error(f"Failed to update student. {err_msg}")


def render_create_student(table_placeholder, search_query):
    """Render create form for students."""
    st.markdown("---")
    st.subheader("Create New Student")
    with st.form("create_student"):
        first = st.text_input("First Name *", help="Required")
        last = st.text_input("Last Name *", help="Required")
        email = st.text_input("Email *", help="Required")
        address = st.text_input("Address *", help="Required")
        year = st.number_input("Year of Study *", min_value=1, max_value=4, value=1, help="Required")
        courses = api.get_courses()
        course_options = {c['name']: c['id'] for c in courses}
        selected_course = st.selectbox("Course *", list(course_options.keys()), help="Required")
        course_id = course_options[selected_course]
        
        submitted = st.form_submit_button("Create")
        if submitted:
            if not first or not last or not email or not address:
                st.error("All fields marked with * are required.")
            else:
                new = {
                    "first_name": first,
                    "last_name": last,
                    "email": email,
                    "address": address,
                    "year_of_study": year,
                    "course_id": course_id
                }
                result = api.create_student(new)

                created = False
                sid = None
                if isinstance(result, dict):
                    succ = result.get("success")
                    if succ is True or (isinstance(succ, str) and succ.lower() == "true"):
                        created = True
                    if result.get("student"):
                        created = True
                        sid = result["student"].get("student_id")

                if created:
                    msg = "Student created successfully!"
                    try:
                        st.cache_data.clear()
                    except Exception:
                        pass
                    st.success(msg)
                    
                    display_cols = ['student_id', 'first_name', 'last_name', 'email', 'course_name', 'year_of_study', 'address']
                    refresh_student_table(table_placeholder, display_cols, search_query)
                else:
                    err_msg = ""
                    if isinstance(result, dict):
                        err_msg = result.get("message") or result.get("error") or ""
                    st.error(f"Failed to create student. {err_msg}")


def refresh_student_table(table_placeholder, display_cols, search_query):
    """Helper to refresh student table."""
    students_df = api.list_students()
    filtered_df = students_df.copy()
    
    if search_query and not students_df.empty:
        q = search_query.strip().lower()
        mask = (
            filtered_df.get('first_name','').astype(str).str.lower().str.contains(q)
            | filtered_df.get('last_name','').astype(str).str.lower().str.contains(q)
            | filtered_df.get('email','').astype(str).str.lower().str.contains(q)
            | filtered_df.get('student_id','').astype(str).str.contains(q)
        )
        filtered_df = filtered_df[mask]
    
    if not filtered_df.empty:
        available_cols = [col for col in display_cols if col in students_df.columns]
        table_placeholder.dataframe(filtered_df[available_cols], use_container_width=True, height=400, hide_index=True)
    else:
        table_placeholder.info("No students found")
