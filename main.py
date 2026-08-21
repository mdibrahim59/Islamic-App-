import streamlit as st
from groq import Groq
from PIL import Image

# 1. পেজ কনফিগারেশন
st.set_page_config(
    page_title="ইসলামিক সহীহ তথ্য", 
    page_icon="🕌", 
    layout="wide"
)

# শক্তিশালী CSS কোড: লেখা ফুল স্ক্রিন করা এবং স্ক্রলিং ঠিক করা
st.markdown("""
<style>
/* মূল বডি কন্টেইনারকে পুরো চওড়া করা */
.block-container {
    max-width: 98% !important;
    padding-left: 10px !important;
    padding-right: 10px !important;
    margin: 0 auto;
}

/* চ্যাট মেসেজগুলোর সাইজ পুরো উইডথ জুড়ে করা */
[data-testid="stChatMessage"] {
    max-width: 100% !important;
}

/* ব্যাকগ্রাউন্ড ইমেজ ঠিক রাখা */
.stApp {
    background-image: url('https://i.ibb.co/6P6X9K3/islamic-bg.jpg');
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
}

/* ইনপুট বক্সটি নিচে ফিক্সড রাখা */
.stChatFloatingInputContainer {
    bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# 2. হেডার
st.markdown("<h1 style='text-align: center; color: #008000;'>🕌 ইসলামিক সহীহ তথ্য 🕌</h1>", unsafe_allow_html=True)
st.markdown("---")

# 3. হিস্ট্রি
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. ইমেজ আপলোডার
uploaded_file = st.file_uploader("🖼️ ছবি বা স্ক্রিনশট দিয়ে প্রশ্ন করুন:", type=["jpg", "jpeg", "png"])
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="আপলোড করা ছবি", width=300)

# 5. ইনপুট
if user_query := st.chat_input("আপনার প্রশ্ন লিখুন..."):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        with st.spinner("আরবি ও হাদিসের রেফারেন্সসহ উত্তর তৈরি হচ্ছে..."):
            
            messages_payload = [
                {"role": "system", "content": "আপনি একজন ইসলামিক স্কলার। আপনার উত্তরের সাথে অবশ্যই প্রাসঙ্গিক আরবি আয়াত (উচ্চারণসহ) এবং সহীহ হাদিসের রেফারেন্স দেবেন। উত্তর পুরো স্ক্রিন জুড়ে গুছিয়ে লিখবেন।"}
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
        st.error(f"ত্রুটি: {e}")
