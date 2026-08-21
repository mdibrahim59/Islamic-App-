import streamlit as st
from groq import Groq
from PIL import Image

# 1. পেজ কনফিগারেশন (layout="wide" দিয়ে পুরো স্ক্রিন জুড়েই রাখা হয়েছে)
st.set_page_config(
    page_title="ইসলামিক সহীহ তথ্য", 
    page_icon="🕌", 
    layout="wide"
)

# স্ক্রিন যেন একদম পুরো মোবাইল/কম্পিউটার জুড়ে চওড়া হয় এবং ব্যাকগ্রাউন্ড ঠিক থাকে
st.markdown("""
<style>
.stApp {
    background-image: url('https://i.ibb.co/6P6X9K3/islamic-bg.jpg'); 
    background-size: cover;          
    background-position: center;     
    background-repeat: no-repeat;    
    background-attachment: fixed;    
}

/* কন্টেন্ট এবং চ্যাট বক্স একদম ফুল স্ক্রিন চওড়া করার জন্য */
.block-container {
    max-width: 100% !important;
    padding-left: 1rem;
    padding-right: 1rem;
    padding-top: 2rem;
    padding-bottom: 5rem;
}
</style>
""", unsafe_allow_html=True)

# 2. অ্যাপের হেডার বা টাইটেল
st.markdown("<h1 style='text-align: center; color: #008000;'>🕌 ইসলামিক সহীহ তথ্য  🕌</h1>", unsafe_allow_html=True)
st.markdown("---")
st.write("<h5 style='text-align: center;'>আপনার যেকোনো ইসলামিক প্রশ্ন বা ছবি দিয়ে আরবি, কোরআন-হাদিসের রেফারেন্সসহ উত্তর নিন।</h5>", unsafe_allow_html=True)
st.write("") 

# 3. চ্যাট হিস্ট্রি বা মেমোরি তৈরি করা
if "messages" not in st.session_state:
    st.session_state.messages = []

# আগের সব চ্যাট স্ক্রিনে দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ৪. ছবি আপলোড করার অপশন
uploaded_file = st.file_uploader("🖼️ কোনো ছবি বা স্ক্রিনশট দিয়ে প্রশ্ন করতে চাইলে এখানে আপলোড করুন (ঐচ্ছিক):", type=["jpg", "jpeg", "png"])
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="আপলোড করা ছবি", width=250)

# 5. মূল চ্যাট ইনপুট বক্স
if user_query := st.chat_input("যেমন: ইস্তিগফারের ফজিলত সম্পর্কে কোরআন ও হাদিসের আলোকে বলুন।"):
    
    # ইউজারের মেসেজ হিস্ট্রিতে যোগ করা এবং দেখানো
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)
        if uploaded_file:
            st.image(img, width=250)

    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        
        with st.spinner("🕌 কোরআন ও হাদিস থেকে আরবি রেফারেন্সসহ তথ্য অনুসন্ধান করা হচ্ছে..."):
            
            # সিস্টেম প্রম্পট আপডেট করা হয়েছে যাতে আরবি এবং আপনার প্রসঙ্গ মনে রাখে
            messages_payload = [
                {
                    "role": "system",
                    "content": "আপনি একজন অত্যন্ত জ্ঞানী ও নির্ভরযোগ্য ইসলামিক স্কলার বা মুফতি। ব্যবহারকারী যখন কোনো প্রশ্ন করবেন, তখন কেবল বাংলায় উত্তর দেবেন না; বরং উত্তরের সাথে সংশ্লিষ্ট পবিত্র কোরআনের আয়াত (আরবিসহ বাংলা অর্থ) এবং সহীহ হাদিসের প্রামাণিক রেফারেন্স (আরবি বা হাদিসের মূল পাঠ থাকলে তা উল্লেখসহ) বাধ্যতামূলকভাবে প্রদান করবেন। ব্যবহারকারীর আগের সমস্ত কথা এবং প্রসঙ্গ মনে রেখে অত্যন্ত বিনয়ী ও প্রজ্ঞাপূর্ণ ভাষায় উত্তর দেবেন। উত্তর শুরু করার সময় সালাম দেবেন এবং শেষে দোয়া করবেন।",
                }
            ]
            
            # আগের কথোপকথনগুলো যোগ করা (যাতে আপনার আগের কথাগুলো মনে রাখে)
            for m in st.session_state.messages:
                # সুনিশ্চিত করার জন্য যে শুধু টেক্সট পাঠানো হচ্ছে
                if isinstance(m["content"], str):
                    messages_payload.append({"role": m["role"], "content": m["content"]})

            chat_completion = client.chat.completions.create(
                messages=messages_payload,
                model="openai/gpt-oss-20b",
                temperature=0.4,
                max_tokens=4096
            )
            
            bot_response = chat_completion.choices[0].message.content
        
        # বটের উত্তর হিস্ট্রি ও স্ক্রিনে যোগ করা
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(f"<div style='background-color: rgba(240, 242, 246, 0.95); padding: 20px; border-radius: 10px;'>{bot_response}</div>", unsafe_allow_html=True)
            st.markdown("---")
            st.caption("বি:দ্র: এই উত্তরটি কৃত্রিম বুদ্ধিমত্তা (AI) দ্বারা তৈরি। চূড়ান্ত ফতোয়ার জন্য কোনো বিজ্ঞ আলেমের পরামর্শ নেওয়া উচিত।")

    except Exception as e:
        st.error(f"❌ দুঃখিত, একটি ত্রুটি দেখা দিয়েছে: {e}")
