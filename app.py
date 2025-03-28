import streamlit as st
import asyncio
from core.chat_agent import ChatAgent
from core.storage import init_db, update_feedback, get_liked_suggestions

st.set_page_config(layout="wide")
init_db()

st.markdown("""
<style>
.like-btn-container > button {
    background-color: #4CAF50 !important;
    color: white !important;
    border: none !important;
    padding: 8px 15px !important;
    border-radius: 6px !important;
    font-size: 16px !important;
    margin-right: 10px !important;
}
.dislike-btn-container > button {
    background-color: #f44336 !important;
    color: white !important;
    border: none !important;
    padding: 8px 15px !important;
    border-radius: 6px !important;
    font-size: 16px !important;
}
.remove-btn-container > button {
    background-color: #ff9800 !important;
    color: white !important;
    border: none !important;
    padding: 6px 12px !important;
    border-radius: 6px !important;
    font-size: 14px !important;
}
</style>
""", unsafe_allow_html=True)

async def main():
    agent = ChatAgent()
    st.title("✨ CraveAI: Content Finder")
    user_input = st.text_input("What content are you craving today?",
                               placeholder="Describe anything you would love to watch in a video...")
    
    if user_input:
        if ("last_input" not in st.session_state) or (st.session_state.last_input != user_input):
            st.session_state.last_input = user_input
            with st.spinner("Generating suggestions..."):
                st.session_state.suggestions = await agent.generate_queries(user_input)
    else:
        st.session_state.suggestions = []
    
    with st.sidebar:
        st.header("💖 Liked Content")
        liked_items = get_liked_suggestions()
        if not liked_items:
            st.info("Like items to save them here")
        else:
            for idx, item in enumerate(liked_items):
                if item.get("type") == "video":
                    title = item.get("title") or "No Title"
                    st.markdown(f"""
                    <div style="border:1px solid #e0e0e0; border-radius:8px; padding:10px; margin-bottom:10px;">
                        <p style="font-size:14px;"><strong>{title[:40]}...</strong></p>
                        <iframe width="100%" height="150" 
                            src="https://www.youtube.com/embed/{item['video_id']}" 
                            frameborder="0" allowfullscreen></iframe>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("❌", key=f"remove_video_{idx}"):
                        update_feedback(item['video_id'], None, True)
                        st.rerun()
                elif item.get("type") == "query":
                    st.markdown(f"""
                    <div style="border:1px solid #e0e0e0; border-radius:8px; padding:10px; margin-bottom:10px;">
                        <p style="font-size:14px;"><strong>{item['query'][:60]}...</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("❌", key=f"remove_query_{idx}"):
                        update_feedback(item['query'], None, False)
                        st.rerun()
    
    col_suggestions, col_videos = st.columns(2)
    
    with col_suggestions:
        if user_input:
            st.header("💡 Search Suggestions")
            for q_idx, query in enumerate(st.session_state.suggestions):
                st.markdown(f"""
                <div style="border:1px solid #e0e0e0; border-radius:8px; padding:10px; margin-bottom:10px;">
                    <p style="font-size:14px;"><strong>{query}</strong></p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("👍", key=f"like_q_{q_idx}"):
                    update_feedback(query, "like", False)
                    st.rerun()
                if st.button("👎", key=f"dislike_q_{q_idx}"):
                    update_feedback(query, "dislike", False)
                    st.rerun()
    
    with col_videos:
        if user_input:
            st.header("🎬 Recommended Videos")
            videos = agent.search_youtube_videos(user_input)
            for v_idx, video in enumerate(videos[:5]):
                st.markdown(f"""
                <div style="border:1px solid #e0e0e0; border-radius:8px; padding:10px; margin-bottom:10px;">
                    <p style="font-size:14px;"><strong>{video['title'][:50]}...</strong></p>
                    <iframe width="100%" height="200" 
                        src="https://www.youtube.com/embed/{video['video_id']}" 
                        frameborder="0" allowfullscreen></iframe>
                </div>
                """, unsafe_allow_html=True)
                if st.button("👍", key=f"like_v_{v_idx}"):
                    update_feedback(video['video_id'], "like", True)
                    st.rerun()
                if st.button("👎", key=f"dislike_v_{v_idx}"):
                    update_feedback(video['video_id'], "dislike", True)
                    st.rerun()

if __name__ == "__main__":
    asyncio.run(main())






