import streamlit as st
from data import dashboard_api as api
import pandas as pd


def render_module_table(table_placeholder):
    """Render the module table with CRUD operations."""
    # First, show course dropdown
    courses = api.get_courses()
    if not courses:
        st.warning("No courses available. Please create a course first.")
        return
    
    course_options = {c['name']: c['id'] for c in courses}
    selected_course_name = st.selectbox(
        "📚 Select Course",
        list(course_options.keys()),
        help="Choose a course to view its modules"
    )
    selected_course_id = course_options[selected_course_name]
    
    # Add search bar for filtering modules
    search_query = st.text_input("🔍 Search modules", value="", help="Type part of a module name, leader, or ID to filter the table.")
    
    # Create new placeholder for table after course dropdown and search bar
    table_placeholder = st.empty()
    
    st.markdown("---")
    
    # Load modules for selected course
    with st.spinner(f"Loading modules for {selected_course_name}..."):
        modules_df = api.list_modules(selected_course_id)
    
    filtered_df = modules_df.copy()
    if search_query and not modules_df.empty:
        q = search_query.strip().lower()
        # Filter by name, leader, credits, or ID
        mask = (
            filtered_df.get('name','').astype(str).str.lower().str.contains(q)
            | filtered_df.get('leader','').astype(str).str.lower().str.contains(q)
            | filtered_df.get('credits','').astype(str).str.contains(q)
            | filtered_df.get('id','').astype(str).str.contains(q)
        )
        filtered_df = filtered_df[mask]

    if not filtered_df.empty:
        display_cols = ['id', 'name', 'credits', 'leader']
        available_cols = [col for col in display_cols if col in filtered_df.columns]
        table_placeholder.dataframe(filtered_df[available_cols], use_container_width=True, height=400, hide_index=True)

        # Delete, Update, Create operations
        render_delete_module(modules_df, table_placeholder, display_cols, search_query, selected_course_id)
        render_update_module(modules_df, table_placeholder, display_cols, search_query, selected_course_id)
    else:
        table_placeholder.info("No modules found for this course")

    render_create_module(table_placeholder, search_query, selected_course_id)


def render_delete_module(modules_df, table_placeholder, display_cols, search_query, course_id):
    """Render delete form for modules."""
    st.markdown("### Delete module by ID")
    with st.form("delete_module_form"):
        id_input = st.text_input("Module ID to delete", value="", help="Type the numeric module id and press Delete")
        module_row = None
        if id_input and id_input.strip():
            try:
                mid_search = int(id_input.strip())
                matches = modules_df[modules_df.get('id') == mid_search]
                if not matches.empty:
                    module_row = matches.iloc[0]
                    st.write(f"Found: **{module_row.get('name')}** (ID: {mid_search}, Leader: {module_row.get('leader')})")
                else:
                    st.warning("No module found with that ID")
            except Exception:
                st.error("Please enter a valid numeric module ID")

        confirm = st.checkbox("I confirm deletion of the above module")
        submitted_del = st.form_submit_button("Delete by ID")
        if submitted_del:
            if module_row is None:
                st.error("Enter a valid module ID before deleting.")
            elif not confirm:
                st.error("Please confirm deletion by checking the box.")
            else:
                mid = int(module_row.get('id'))
                with st.spinner("Deleting module..."):
                    res = api.delete_module(mid)

                if res is True:
                    try:
                        st.cache_data.clear()
                    except Exception:
                        pass
                    st.success(f"Module {mid} deleted")
                    refresh_module_table(table_placeholder, display_cols, search_query, course_id)
                else:
                    st.error("Failed to delete module.")


def render_update_module(modules_df, table_placeholder, display_cols, search_query, course_id):
    """Render update form for modules."""
    st.markdown("### Update module by ID")
    st.info("Update feature: Enter module ID, load fields, modify, and submit.")
    with st.form("update_module_form"):
        update_id_input = st.text_input("Module ID to update", value="", help="Type numeric module id and press Load")
        load_clicked = st.form_submit_button("Load Module")

        loaded_row = None
        if load_clicked:
            if not update_id_input or not update_id_input.strip():
                st.error("Enter a numeric module ID to load.")
            else:
                try:
                    mid_lookup = int(update_id_input.strip())
                    matches = modules_df[modules_df.get('id') == mid_lookup]
                    if matches.empty:
                        st.warning("No module found with that ID")
                    else:
                        loaded_row = matches.iloc[0]
                except Exception:
                    st.error("Please enter a valid numeric module ID")

        if loaded_row is not None:
            st.session_state['update_module_name_field'] = loaded_row.get('name', '')
            st.session_state['update_module_credits_field'] = int(loaded_row.get('credits', 0))
            st.session_state['update_module_leader_field'] = loaded_row.get('leader', '')

        # Editable inputs
        upd_name = st.text_input("Module Name *", value=st.session_state.get('update_module_name_field', ''), help="Required")
        upd_credits = st.number_input("Credits *", min_value=0, max_value=100, value=st.session_state.get('update_module_credits_field', 0), help="Required")
        upd_leader = st.text_input("Module Leader *", value=st.session_state.get('update_module_leader_field', ''), help="Required")

        submit_update = st.form_submit_button("Submit Update")
        if submit_update:
            try:
                mid = int(update_id_input.strip())
            except Exception:
                st.error("Enter a valid numeric module ID in the top field before submitting updates.")
                mid = None

            if mid is not None:
                if not upd_name or not upd_leader:
                    st.error("All fields are required.")
                    mid = None

            if mid is not None:
                updates = {
                    "module_name": upd_name,
                    "credits": int(upd_credits),
                    "module_leader": upd_leader
                }
                with st.spinner("Updating module..."):
                    res = api.update_module(mid, updates)

                success = bool(res)
                if success:
                    try:
                        st.cache_data.clear()
                    except Exception:
                        pass
                    st.session_state['update_module_name_field'] = ''
                    st.session_state['update_module_credits_field'] = 0
                    st.session_state['update_module_leader_field'] = ''
                    st.success(f"Module {mid} updated")
                    refresh_module_table(table_placeholder, display_cols, search_query, course_id)
                else:
                    err_msg = ''
                    if isinstance(res, dict):
                        err_msg = res.get('message') or res.get('error') or ''
                    st.error(f"Failed to update module. {err_msg}")


def render_create_module(table_placeholder, search_query, course_id):
    """Render create form for modules."""
    st.markdown("---")
    st.subheader("Create New Module")
    with st.form("create_module"):
        name = st.text_input("Module Name *", help="Required")
        credits = st.number_input("Credits *", min_value=0, max_value=100, value=15, help="Required")
        leader = st.text_input("Module Leader *", help="Required (e.g., Dr John Smith)")
        
        submitted = st.form_submit_button("Create")
        if submitted:
            if not name or not leader:
                st.error("All fields are required.")
            else:
                new = {
                    "module_name": name,
                    "credits": int(credits),
                    "module_leader": leader,
                }
                result = api.create_module(new, course_id)

                created = False
                if isinstance(result, dict):
                    succ = result.get("success")
                    if succ is True or (isinstance(succ, str) and succ.lower() == "true"):
                        created = True
                    if result.get("module"):
                        created = True

                if created:
                    try:
                        st.cache_data.clear()
                    except Exception:
                        pass
                    st.success("Module created successfully!")
                    
                    display_cols = ['id', 'name', 'credits', 'leader']
                    refresh_module_table(table_placeholder, display_cols, search_query, course_id)
                else:
                    err_msg = ""
                    if isinstance(result, dict):
                        err_msg = result.get("message") or result.get("error") or ""
                    st.error(f"Failed to create module. {err_msg}")


def refresh_module_table(table_placeholder, display_cols, search_query, course_id):
    """Helper to refresh module table."""
    modules_df = api.list_modules(course_id)
    filtered_df = modules_df.copy()
    
    if search_query and not modules_df.empty:
        q = search_query.strip().lower()
        mask = (
            filtered_df.get('name','').astype(str).str.lower().str.contains(q)
            | filtered_df.get('leader','').astype(str).str.lower().str.contains(q)
            | filtered_df.get('credits','').astype(str).str.contains(q)
            | filtered_df.get('id','').astype(str).str.contains(q)
        )
        filtered_df = filtered_df[mask]
    
    if not filtered_df.empty:
        available_cols = [col for col in display_cols if col in modules_df.columns]
        table_placeholder.dataframe(filtered_df[available_cols], use_container_width=True, height=400, hide_index=True)
    else:
        table_placeholder.info("No modules found for this course")
