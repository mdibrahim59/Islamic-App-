import streamlit as st
from groq import Groq

# পেজ সেটআপ
st.set_page_config(page_title="Islamic App", page_icon="🕌")

st.title("🕌 Islamic Assistant App")
st.write("আপনার প্রশ্নের উত্তর পেতে নিচে Groq API Key দিন এবং প্রশ্ন লিখুন।")

# API Key ইনপুট
api_key = st.text_input("Groq API Key দিন:", type="password")

# প্রশ্ন লেখার জায়গা
user_query = st.text_area("আপনার ইসলামিক প্রশ্ন বা বিষয় লিখুন:")

# উত্তর পাওয়ার বাটন
if st.button("উত্তর দিন"):
    if not api_key:
        st.warning("দয়া করে আপনার Groq API Key টি দিন!")
    elif not user_query:
        st.warning("দয়া করে আপনার প্রশ্নটি লিখুন!")
    else:
        try:
            client = Groq(api_key=api_key)
            with st.spinner("উত্তর তৈরি করা হচ্ছে..."):
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": user_query}],
                    model="llama3-8b-8192",
                )
                st.write("### 📖 উত্তর:")
                st.success(chat_completion.choices[0].message.content)
        except Exception as e:
            st.error(f"ভুল হয়েছে: {e}")
