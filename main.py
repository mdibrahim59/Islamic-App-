import streamlit as st
from groq import Groq

# 1. পেজ কনফিগারেশন এবং লোগো সেটআপ
st.set_page_config(
    page_title="ইসলামিক সহীহ তথ্য", 
    page_icon="🕌", 
    layout="centered"
)

# 2. অ্যাপের হেডার বা টাইটেল
st.markdown("<h1 style='text-align: center; color: #008000;'>🕌 সহীহ ইসলামিক ইনফো 🕌</h1>", unsafe_allow_html=True)
st.markdown("---")
st.write("<h5 style='text-align: center;'>আপনার যেকোনো ইসলামিক প্রশ্নের নির্ভরযোগ্য উত্তর পেতে নিচে প্রশ্ন লিখুন।</h5>", unsafe_allow_html=True)
st.write("") 

# 3. মূল প্রশ্ন লেখার জায়গা
st.write("### ❓ আপনার প্রশ্নটি লিখুন:")
user_query = st.text_area("প্রশ্ন:", height=150, placeholder="যেমন: জুমার নামাজের ফজিলত সম্পর্কে বলুন।")

# 4. উত্তর পাওয়ার বাটন
if st.button("🔍 উত্তর দিন"):
    if not user_query:
        st.warning("⚠️ দয়া করে আপনার প্রশ্নটি লিখুন।")
    else:
        try:
            # এখানে আপনার Groq API Key টি বসিয়ে দেওয়া হয়েছে, তাই কাউকে আলাদা করে দিতে হবে না
            client = Groq(api_key="আপনার_আসল_এপিআই_কি_এখানে_বসান")
            
            with st.spinner("🕌 ইসলামিক তথ্য অনুসন্ধান করা হচ্ছে... দয়া করে অপেক্ষা করুন।"):
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "আপনি একজন অত্যন্ত জ্ঞানী ও নির্ভরযোগ্য ইসলামিক স্কলার বা আলেম। আপনি কোরআন ও হাদিসের সঠিক রেফারেন্স ব্যবহার করে ব্যবহারকারীর প্রশ্নের উত্তর দেবেন। আপনার ভাষা হবে অত্যন্ত বিনয়ী, জ্ঞানগর্ভ এবং সহজবোধ্য। উত্তর দেওয়ার সময় সর্বদা সালাম দেবেন এবং শেষে দোয়া করবেন। আপনার উত্তরটি শুধুমাত্র বাংলা ভাষায় এবং ইসলামী দৃষ্টিকোণ থেকে দেবেন।",
                        },
                        {
                            "role": "user",
                            "content": user_query,
                        }
                    ],
                    model="llama3-70b-8192",
                    temperature=0.5,
                    max_tokens=2048
                )
                
                bot_response = chat_completion.choices[0].message.content
            
            # 5. উত্তর প্রদর্শন
            st.success("✅ আলহামদুলিল্লাহ! সঠিক উত্তরটি নিচে দেওয়া হলো:")
            st.markdown("---")
            st.markdown(f"<div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>{bot_response}</div>", unsafe_allow_html=True)
            st.markdown("---")
            st.caption("বি:দ্র: এই উত্তরটি কৃত্রিম বুদ্ধিমত্তা (AI) দ্বারা তৈরি। চূড়ান্ত ফতোয়ার জন্য কোনো বিজ্ঞ আলেমের পরামর্শ নেওয়া উচিত।")

        except Exception as e:
            st.error(f"❌ দুঃখিত, একটি ত্রুটি দেখা দিয়েছে: {e}")

# 6. ফুটার
st.markdown("---")
st.markdown("<p style='text-align: center;'>তৈরি করেছেন: মো: ইব্রাহিম | সহীহ ইসলামিক ইনফো © 2026</p>", unsafe_allow_html=True)
