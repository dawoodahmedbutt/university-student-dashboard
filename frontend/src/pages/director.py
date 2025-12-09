import streamlit as st
import altair as alt
from data import dashboard_api as api
from utils import to_df


def render():
    st.header("📈 Course Director")
    # Course selection
    with st.spinner("Loading courses..."):
        courses = api.get_courses()
    course_options = ["All Courses"] + [c["name"] for c in courses]
    selected_course = st.selectbox("Select Course", course_options)
    course_id = None if selected_course == "All Courses" else next((c["id"] for c in courses if c["name"] == selected_course), None)

    # Module selection
    if course_id:
        modules = api.get_modules_for_course(course_id)
        module_options = ["All Modules"] + [m["name"] for m in modules]
        selected_module = st.selectbox("Select Module", module_options)
        module_id = None if selected_module == "All Modules" else next((m["id"] for m in modules if m["name"] == selected_module), None)
    else:
        st.selectbox("Select Module", ["All Modules"], disabled=True)
        module_id = None

    st.divider()

    # Fetch data (show spinner while loading)
    with st.spinner("Loading dashboard data..."):
        averages = api.get_director_averages(course_id, module_id)
        bar_df = to_df(api.get_module_comparison(course_id) if course_id else api.get_course_comparison())
        scatter_df = to_df(api.get_attendance_vs_performance(course_id))

    c1, c2 = st.columns(2)
    c1.metric("Overall Attendance", f"{averages.get('attendance', 0):.2f}%")
    c2.metric("Overall Performance", f"{averages.get('performance', 0):.2f}%")

    st.markdown("---")

    st.subheader("Grade Distribution")
    if course_id and module_id:
        with st.spinner("Loading grade distribution..."):
            grade_dist = api.get_grade_distribution(course_id, module_id)
        
        if grade_dist:
            # Convert dictionary to DataFrame for plotting
            import pandas as pd
            dist_df = pd.DataFrame([
                {"Student ID": student_id, "Grade": grade}
                for student_id, grade in grade_dist.items()
            ])
            
            # Create histogram/bar chart of grade distribution
            chart = alt.Chart(dist_df).mark_bar().encode(
                x=alt.X('Grade:Q', bin=alt.Bin(maxbins=10), title='Grade Range'),
                y=alt.Y('count()', title='Number of Students'),
                tooltip=['count()', alt.Tooltip('Grade:Q', bin=alt.Bin(maxbins=10))]
            ).properties(height=300)
            
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("No grade distribution data available")
    else:
        st.info("Please select a course and module to view grade distribution")

    st.subheader("Attendance vs Performance")
    if not scatter_df.empty:
        # Transform data for grouped bar chart
        chart_data = scatter_df.melt(
            id_vars=['module_name'],
            value_vars=['attendance', 'performance'],
            var_name='metric',
            value_name='percentage'
        )
        
        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('module_name:N', title='Module'),
            y=alt.Y('percentage:Q', title='Percentage (%)'),
            color=alt.Color('metric:N', scale=alt.Scale(scheme='set1')),
            xOffset='metric:N',
            tooltip=['module_name', 'metric', 'percentage:Q']
        ).properties(width=600, height=400)
        
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No data available")
    
    st.markdown("---")
    
    # Student Risk Matrix
    st.subheader("📊 Student Risk Matrix")
    if course_id and module_id:
        with st.spinner("Loading student risk data..."):
            risk_data = api.get_student_risk_matrix(course_id, module_id)
        
        if risk_data:
            # Convert dictionary to DataFrame
            import pandas as pd
            risk_df = pd.DataFrame.from_dict(risk_data, orient='index')
            risk_df.index.name = 'Student ID'
            risk_df = risk_df.reset_index()
            
            # Rename columns for better display
            risk_df = risk_df.rename(columns={
                'Student ID': 'ID',
                'first_name': 'First Name',
                'last_name': 'Last Name',
                'attendance': 'Attendance (%)',
                'performance': 'Performance (%)',
                'risk': 'Risk Level'
            })
            
            # Function to color risk levels
            def color_risk(val):
                if val == 'HIGH':
                    return 'color: #ff0000; font-weight: bold'
                elif val == 'MEDIUM':
                    return 'color: #ff8800; font-weight: bold'
                elif val == 'LOW':
                    return 'color: #00aa00; font-weight: bold'
                return ''
            
            # Apply styling to Risk Level column
            styled_df = risk_df.style.applymap(
                color_risk,
                subset=['Risk Level']
            )
            
            st.dataframe(styled_df, use_container_width=True, height=400, hide_index=True)
        else:
            st.info("No student risk data available")
    else:
        st.info("Please select a course and module to view student risk matrix")
