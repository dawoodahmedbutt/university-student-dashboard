import streamlit as st
from pages.tables import student_table, course_table, module_table


def render():
    st.header(' Data Management')
    
    # Dropdown to select which table to manage
    table_options = {
        'Students': 'students',
        'Courses': 'courses',
        'Modules': 'modules'
    }
    
    selected_table = st.selectbox(
        ' Select Table to Manage',
        options=list(table_options.keys()),
        help='Choose which table you want to view and manage'
    )
    
    st.markdown('---')
    
    # Create placeholder for the selected table
    table_placeholder = st.empty()
    
    # Render the appropriate table based on selection
    table_type = table_options[selected_table]
    
    if table_type == 'students':
        student_table.render_student_table(table_placeholder)
    elif table_type == 'courses':
        course_table.render_course_table(table_placeholder)
    elif table_type == 'modules':
        module_table.render_module_table(table_placeholder)
