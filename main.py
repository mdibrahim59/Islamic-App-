import streamlit as st
from groq import Groq

# 1. পেজ কনফিগারেশন
st.set_page_config(
    page_title="ইসলামিক সহীহ তথ্য", 
    page_icon="🕌", 
    layout="wide"
)

# লেআউট ঠিক করার জন্য CSS
st.markdown("""
<style>
.block-container {
    max-width: 98% !important;
    padding-top: 2rem;
    padding-bottom: 5rem;
}
</style>
""", unsafe_allow_html=True)

# 2. অ্যাপের হেডার বা টাইটেল
st.markdown("<h1 style='text-align: center; color: #008000;'>🕌 ইসলামিক সহীহ তথ্য 🕌</h1>", unsafe_allow_html=True)
st.markdown("---")
st.write("<h5 style='text-align: center;'>আপনার যেকোনো ইসলামিক প্রশ্নের নির্ভরযোগ্য উত্তর পেতে নিচে চ্যাট করুন।</h5>", unsafe_allow_html=True)
st.write("") 

# 3. চ্যাট হিস্ট্রি বা মেমোরি তৈরি করা
if "messages" not in st.session_state:
    st.session_state.messages = []

# আগের সব চ্যাট স্ক্রিনে দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. মূল চ্যাট ইনপুট বক্স
if user_query := st.chat_input("যেমন: জুমার নামাজের ফজিলত সম্পর্কে বলুন..."):
    
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        
        with st.spinner("🕌 ইসলামিক তথ্য অনুসন্ধান করা হচ্ছে... দয়া করে অপেক্ষা করুন।"):
            
            messages_payload = [
                {
                    "role": "system",
                    "content": "আপনি একজন অত্যন্ত জ্ঞানী ও নির্ভরযোগ্য ইসলামিক স্কলার বা আলেম। আপনি কোরআন ও হাদিসের সঠিক রেফারেন্স ব্যবহার করে ব্যবহারকারীর প্রশ্নের উত্তর দেবেন। আপনার ভাষা হবে অত্যন্ত বিনয়ী, জ্ঞানগর্ভ এবং সহজবোধ্য। উত্তর দেওয়ার সময় সর্বদা সালাম দেবেন এবং শেষে দোয়া করবেন।",
                }
            ]
            
            for m in st.session_state.messages:
                messages_payload.append({"role": m["role"], "content": m["content"]})

            # এখানে মডেলের নাম পরিবর্তন করে সঠিক ও কার্যকারী মডেল দেওয়া হয়েছে
            chat_completion = client.chat.completions.create(
                messages=messages_payload,
                model="llama-3.3-70b-versatile",
                temperature=0.5,
                max_tokens=4096
            )
            
            bot_response = chat_completion.choices[0].message.content
        
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(bot_response)
            st.markdown("---")
            st.caption("বি:দ্র: এই উত্তরটি কৃত্রিম বুদ্ধিমত্তা (AI) দ্বারা তৈরি। চূড়ান্ত ফতোয়ার জন্য কোনো বিজ্ঞ আলেমের পরামর্শ নেওয়া উচিত।")

    except Exception as e:
        st.error(f"❌ দুঃখিত, একটি ত্রুটি দেখা দিয়েছে: {e}")
