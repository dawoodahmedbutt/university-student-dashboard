import streamlit as st


def top_header():
    st.title("🎓 UniSystem ")
    st.markdown("---")


def two_column_kpis(kpis):
    """Utility to render KPI columns. kpis is list of (label, value, delta).
    """
    cols = st.columns(len(kpis))
    for c, (label, value, *rest) in zip(cols, kpis):
        c.metric(label, value)
