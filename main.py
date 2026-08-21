import streamlit as st
from groq import Groq
from PIL import Image

# 1. পেজ কনফিগারেশন
st.set_page_config(
    page_title="ইসলামিক সহীহ তথ্য", 
    page_icon="🕌", 
    layout="wide"
)

# ব্যাকগ্রাউন্ড কালো এবং লেখা যেন পুরো স্ক্রিন জুড়ে আসে তার জন্য CSS
st.markdown("""
<style>
/* ব্যাকগ্রাউন্ড কালো করা */
.stApp {
    background-color: #000000 !important;
}

/* কন্টেন্ট পুরো স্ক্রিন জুড়ে চওড়া করা */
.block-container {
    max-width: 100% !important;
    padding-top: 1rem;
    padding-bottom: 5rem;
}

/* টেক্সট কালার সাদা করা যাতে কালো ব্যাকগ্রাউন্ডে বোঝা যায় */
h1, h5, p, div {
    color: #FFFFFF !important;
}

/* চ্যাট মেসেজ বক্সের কালার */
[data-testid="stChatMessage"] {
    background-color: #1a1a1a !important;
    border-radius: 10px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# 2. হেডার
st.markdown("<h1 style='text-align: center; color: #008000;'>🕌 ইসলামিক সহীহ তথ্য 🕌</h1>", unsafe_allow_html=True)
st.markdown("---")

# 3. চ্যাট হিস্ট্রি
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. ছবি আপলোড
uploaded_file = st.file_uploader("🖼️ ছবি বা স্ক্রিনশট আপলোড করুন:", type=["jpg", "jpeg", "png"])
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="আপলোড করা ছবি", width=250)

# 5. ইনপুট বক্স
if user_query := st.chat_input("আপনার প্রশ্ন লিখুন..."):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        with st.spinner("আরবি ও হাদিসের রেফারেন্সসহ উত্তর তৈরি হচ্ছে..."):
            
            messages_payload = [
                {"role": "system", "content": "আপনি একজন ইসলামিক স্কলার। ব্যবহারকারীর প্রতিটি প্রশ্নের উত্তর কোরআনের আয়াত (আরবি ও বাংলা অর্থসহ) এবং সহীহ হাদিসের রেফারেন্স দিয়ে দেবেন। উত্তর পুরো স্ক্রিন জুড়ে সুন্দরভাবে সাজিয়ে লিখবেন।"}
            ]
            for m in st.session_state.messages:
                if isinstance(m["content"], str):
                    messages_payload.append({"role": m["role"], "content": m["content"]})

            chat_completion = client.chat.completions.create(
                messages=messages_payload,
                model="openai/gpt-oss-20b",
                temperature=0.4
            )
            bot_response = chat_completion.choices[0].message.content
        
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(bot_response)
    except Exception as e:
        st.error(f"ত্রুটি হয়েছে: {e}")
