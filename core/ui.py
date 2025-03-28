import streamlit as st
from typing import List, Optional, Tuple

def display_intro() -> str:
    """
    Display the introduction and input field with enhanced UI.
    """
    with st.container():
        st.markdown("""
        <style>
            .stTextInput input {
                font-size: 18px;
                padding: 12px;
            }
        </style>
        """, unsafe_allow_html=True)
        
        return st.text_input(
            "What kind of content are you craving right now?",
            placeholder="e.g., 'sustainable fashion', 'AI ethics', 'indie music'...",
            help="Be as specific or broad as you like"
        )

def display_liked_only(liked_suggestions: List[str]) -> None:
    """
    Display liked suggestions in the sidebar with enhanced UI.
    """
    if not liked_suggestions:
        st.info("🌟 Like suggestions to save them here")
        return
    
    st.success(f"You have {len(liked_suggestions)} liked suggestions")
    
    for idx, suggestion in enumerate(liked_suggestions, 1):
        with st.expander(f"{idx}. {suggestion[:30]}..." if len(suggestion) > 30 else f"{idx}. {suggestion}"):
            st.markdown(suggestion)
            if st.button("Remove", key=f"remove_{idx}"):
                update_feedback(suggestion, None)
                st.rerun()

def display_suggestions_with_feedback(suggestions_feedback: List[Tuple[str, str]]) -> None:
    """
    Display suggestions with their feedback status (enhanced version).
    """
    if not suggestions_feedback:
        st.info("No suggestions yet. Enter your craving above!")
        return
    
    tab1, tab2, tab3 = st.tabs(["All", "Liked", "Disliked"])
    
    with tab1:
        st.subheader("All Suggestions")
        for suggestion, feedback in suggestions_feedback:
            display_suggestion_card(suggestion, feedback)
    
    with tab2:
        st.subheader("Liked Suggestions")
        liked = [(s, f) for s, f in suggestions_feedback if f == "True"]
        if not liked:
            st.info("No liked suggestions yet")
        for suggestion, feedback in liked:
            display_suggestion_card(suggestion, feedback)
    
    with tab3:
        st.subheader("Disliked Suggestions")
        disliked = [(s, f) for s, f in suggestions_feedback if f == "False"]
        if not disliked:
            st.info("No disliked suggestions")
        for suggestion, feedback in disliked:
            display_suggestion_card(suggestion, feedback)

def display_suggestion_card(suggestion: str, feedback: Optional[str]) -> None:
    """
    Helper function to display a suggestion card with consistent styling.
    """
    status_emoji = {
        "True": "✅ Liked",
        "False": "❌ Disliked",
        None: "⭐ Not rated"
    }.get(feedback, "⭐ Not rated")
    
    with st.container(border=True):
        st.markdown(f"**{suggestion}**")
        st.caption(status_emoji)
        
        if feedback != "True":
            if st.button("Like", key=f"like_{suggestion}"):
                update_feedback(suggestion, "True")
                st.rerun()
        else:
            if st.button("Remove like", key=f"unlike_{suggestion}"):
                update_feedback(suggestion, None)
                st.rerun()

def display_video_analysis(video_url: str, summary: str, recommendations: List[str]):
    """New section for transcript-based recommendations."""
    with st.expander("🎬 Video Insights", expanded=True):
        st.subheader("Summary")
        st.write(summary)
        
        st.subheader("Recommended Searches")
        for i, query in enumerate(recommendations, 1):
            if st.button(f"🔍 {query}", key=f"rec_{i}"):
                st.session_state.user_input = query  # Auto-fill search