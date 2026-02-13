# Sub-File 84-H: Global layout engine for Liquid UI/UX transitions.
# Follows 'Pichai Rule' for clean, minimalist design. [cite: 2026-02-11]

def apply_iphone_layout():
    import streamlit as st
    st.markdown("""
    <style>
    /* Rounded corners for all containers */
    div.stBlock {
        border-radius: 24px;
        background: rgba(255, 255, 255, 0.03);
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    </style>
    """, unsafe_allow_html=True)
  
