import streamlit as st
import altair as alt
from data import dashboard_api as api
from utils import to_df
import pandas as pd


def render():
    st.header("💚 Wellbeing Officer")

    # CSV Import Section
    with st.expander("📥 Import Wellbeing Data from CSV"):
        st.markdown("""
        **CSV Format Requirements:**
        - Required columns: `student_id`, `date`, `stress_level`, `activity_level`, `quality_of_food`, `alcohol_drug_consumption`, `medication`, `hours_slept`
        - Date format: YYYY-MM-DD
        - All values (except hours_slept) must be between 1-10
        - hours_slept must be between 0-24
        """)
        
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        
        if uploaded_file is not None:
            try:
                # Read CSV file
                df = pd.read_csv(uploaded_file)
                
                # Validate required columns
                required_cols = ['student_id', 'date', 'stress_level', 'activity_level', 
                                'quality_of_food', 'alcohol_drug_consumption', 'medication', 'hours_slept']
                missing_cols = [col for col in required_cols if col not in df.columns]
                
                if missing_cols:
                    st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
                else:
                    st.success(f"✅ CSV loaded successfully with {len(df)} records")
                    st.dataframe(df.head(), use_container_width=True)
                    
                    if st.button("📤 Upload Records to Database", type="primary"):
                        progress_bar = st.progress(0)
                        success_count = 0
                        error_count = 0
                        errors = []
                        
                        for idx, row in df.iterrows():
                            try:
                                # Map CSV columns to API format
                                wellbeing_data = {
                                    "student_id": int(row['student_id']),
                                    "date": str(row['date']),
                                    "stress": int(row['stress_level']),
                                    "activity": int(row['activity_level']),
                                    "food_quality": int(row['quality_of_food']),
                                    "alcohol_drugs": int(row['alcohol_drug_consumption']),
                                    "medication": int(row['medication']),
                                    "hours_slept": int(row['hours_slept'])
                                }
                                
                                # Send to API
                                result = api.create_wellbeing_record(wellbeing_data)
                                
                                if result.get('success') or result.get('id'):
                                    success_count += 1
                                else:
                                    error_count += 1
                                    errors.append(f"Row {idx + 1}: {result.get('message', 'Unknown error')}")
                                    
                            except Exception as e:
                                error_count += 1
                                errors.append(f"Row {idx + 1}: {str(e)}")
                            
                            # Update progress
                            progress_bar.progress((idx + 1) / len(df))
                        
                        # Show results
                        progress_bar.empty()
                        
                        col1, col2 = st.columns(2)
                        col1.metric("✅ Successfully Uploaded", success_count)
                        col2.metric("❌ Failed", error_count)
                        
                        if errors:
                            with st.expander("View Errors"):
                                for error in errors[:10]:  # Show first 10 errors
                                    st.error(error)
                                if len(errors) > 10:
                                    st.info(f"... and {len(errors) - 10} more errors")
                        
                        if success_count > 0:
                            st.success(f"🎉 Import completed! {success_count} records uploaded successfully.")
                            st.cache_data.clear()  # Clear cache to refresh data
                            
            except Exception as e:
                st.error(f"❌ Error reading CSV file: {str(e)}")

    st.markdown("---")
    st.subheader("📊 Wellbeing Records")
    
    # Load courses for dropdown
    with st.spinner("Loading courses..."):
        courses_df = api.list_courses()
    
    # Course dropdown filter
    if not courses_df.empty:
        course_options = ["All Courses"] + courses_df['course_name'].tolist()
        course_ids = [None] + courses_df['course_id'].tolist()
        selected_course_name = st.selectbox("Select Course", course_options, key="wellbeing_course_filter")
        selected_course_id = course_ids[course_options.index(selected_course_name)]
    else:
        selected_course_id = None
    
    # Load wellbeing data based on selected course
    with st.spinner("Loading wellbeing data..."):
        wellbeing_df = api.get_wellbeing_all(course_id=selected_course_id)
    
    # Calculate metrics from the data
    if not wellbeing_df.empty:
        # Critical Alerts: Count of students with risk_level <= 4 (Red)
        critical_count = len(wellbeing_df[wellbeing_df['risk_level'] <= 4]) if 'risk_level' in wellbeing_df.columns else 0
        
        # Avg Stress: Average of stress_level column
        avg_stress = wellbeing_df['stress_level'].mean() if 'stress_level' in wellbeing_df.columns else 0
        
        # Avg Sleep: Average of hours_slept column
        avg_sleep = wellbeing_df['hours_slept'].mean() if 'hours_slept' in wellbeing_df.columns else 0
    else:
        critical_count = 0
        avg_stress = 0
        avg_sleep = 0
    
    # Display metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Critical Alerts", critical_count)
    c2.metric("Avg Stress", f"{avg_stress:.2f}" if avg_stress > 0 else "0")
    c3.metric("Avg Sleep", f"{avg_sleep:.2f}h" if avg_sleep > 0 else "0h")
    
    st.markdown("---")
    
    # Average Stress by Course Bar Chart
    st.subheader("📊 Average Stress Level by Course")
    with st.spinner("Loading stress data..."):
        stress_df = api.get_stress_avg_plot()
    
    if not stress_df.empty and 'course_name' in stress_df.columns and 'avg_stress' in stress_df.columns:
        chart = alt.Chart(stress_df).mark_bar(color='#ff4444').encode(
            x=alt.X('course_name:N', title='Course', sort=None),
            y=alt.Y('avg_stress:Q', title='Average Stress Level'),
            tooltip=['course_name', alt.Tooltip('avg_stress:Q', format='.2f')]
        ).properties(height=300)
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No stress data available")
    
    st.markdown("---")
    
    if not wellbeing_df.empty:
        # Search bar above the table
        wellbeing_search = st.text_input("🔍 Search wellbeing records...", key="wellbeing_search")
        
        # Function to convert risk level to colored text
        def risk_level_to_text(risk_level):
            if pd.isna(risk_level):
                return 'N/A'
            if risk_level <= 4:
                return 'Red'
            elif risk_level <= 7:
                return 'Amber'
            else:
                return 'Green'
        
        # Function to color the text based on risk category
        def color_risk_text(val):
            if val == 'Red':
                return 'color: #ff0000; font-weight: bold'
            elif val == 'Amber':
                return 'color: #ff8800; font-weight: bold'
            elif val == 'Green':
                return 'color: #00aa00; font-weight: bold'
            return ''
        
        # Display columns
        display_cols = [
            'wellbeing_id', 'student_id', 'student_first_name', 'student_last_name',
            'date', 'stress_level', 'activity_level', 'quality_of_food',
            'alcohol_drug_consumption', 'medication', 'hours_slept', 'risk_level'
        ]
        available_cols = [col for col in display_cols if col in wellbeing_df.columns]
        
        # Create a copy and convert risk_level to text
        display_df = wellbeing_df[available_cols].copy()
        if 'risk_level' in display_df.columns:
            display_df['risk_level'] = display_df['risk_level'].apply(risk_level_to_text)
        
        # Rename columns to shorter names to fit better
        display_df = display_df.rename(columns={
            'wellbeing_id': 'ID',
            'student_id': 'S_ID',
            'student_first_name': 'First',
            'student_last_name': 'Last',
            'date': 'Date',
            'stress_level': 'Stress',
            'activity_level': 'Activity',
            'quality_of_food': 'Food',
            'alcohol_drug_consumption': 'Alc/Drug',
            'medication': 'Med',
            'hours_slept': 'Sleep',
            'risk_level': 'Risk'
        })
        
        # Apply search filter
        if wellbeing_search:
            mask = display_df.astype(str).apply(
                lambda row: row.str.contains(wellbeing_search, case=False, na=False).any(),
                axis=1
            )
            display_df = display_df[mask]
        
        # Apply text coloring to risk_level column
        styled_df = display_df.style.map(
            color_risk_text,
            subset=['Risk']
        )
        
        st.dataframe(styled_df, use_container_width=True, height=400, hide_index=True)
    else:
        st.info("No wellbeing data available")
