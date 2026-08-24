import streamlit as st
from groq import Groq
from PIL import Image

# ১. পেজ কনফিগারেশন (layout="wide" দিয়ে পুরো স্ক্রিন জুড়ে রাখা হয়েছে)
st.set_page_config(
    page_title="ইসলামিক সহীহ তথ্য",
    page_icon="🕌",
    layout="wide"
)

# ২. কাস্টম CSS (স্ক্রিন জুড়ে ডিসপ্লে, ডার্ক ব্যাকগ্রাউন্ড এবং স্ক্রল ঠিক করার জন্য)
st.markdown("""
<style>
.stApp {
    background-color: #121212;
    background-image: url('https://i.ibb.co/6P6X9K3/islamic-bg.jpg');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    overflow-y: auto !important;
    color: #ffffff;
}

/* কন্টেন্ট এবং চ্যাট বক্স ফুল স্ক্রিন করার জন্য */
.block-container {
    max-width: 100% !important;
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 2rem;
    padding-bottom: 5rem;
}
</style>
""", unsafe_allow_html=True)

# অ্যাপের হেডার ডিজাইন
st.markdown("<h1 style='text-align: center; color: #00FF7F;'>🕌 ইসলামিক সহীহ তথ্য ও মাসআলা 🕌</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #CCCCCC;'>কুরআন, সুন্নাহ এবং আরবি ইবারতসহ নির্ভরযোগ্য সমাধান</h4>", unsafe_allow_html=True)
st.markdown("---")

# ৩. চ্যাট হিস্ট্রি বা মেমোরি তৈরি করা
if "messages" not in st.session_state:
    st.session_state.messages = []

# ৪. আগের সব চ্যাট স্ক্রিনে দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ৫. ছবি আপলোড করার অপশন
uploaded_file = st.file_uploader("🖼️ কোনো প্রশ্ন বা কিতাবের পাতার ছবি থাকলে এখানে আপলোড করুন (ঐচ্ছিক)", type=["jpg", "jpeg", "png"])
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="আপলোড করা ছবি", width=250)

# ৬. মূল চ্যাট ইনপুট বক্স
if user_query := st.chat_input("যেমন: ইস্তিগফারের ফযিলত সম্পর্কে কুরআন ও হাদিসের আলোকে বলুন..."):
    
    # ইউজারের মেসেজ হিস্ট्रीতে যোগ করা এবং স্ক্রিনে দেখানো
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    try:
        # Groq ক্লায়েন্ট ইনিশিয়ালাইজ করা
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])

        with st.spinner("🕌 কুরআন ও হাদিস থেকে আরবি ইবারত ও রেফারেন্সসহ তথ্য অনুসন্ধান করা হচ্ছে..."):
            
            # সিস্টেম প্রম্পট (যা মডেলকে বিস্তারিত ও সঠিক উত্তর দিতে বাধ্য করবে)
            messages_payload = [
                {
                    "role": "system",
                    "content": (
                        "আপনি একজন অত্যন্ত জ্ঞানী, অভিজ্ঞ এবং নির্ভরযোগ্য ইসলামিক মুফতি বা স্কলার। "
                        "ব্যবহারকারী যেকোনো মাসআলা বা প্রশ্ন জিজ্ঞাসা করলে তাকে সংক্ষিপ্ত উত্তর দেবেন না; "
                        "বরং কুরআন ও সুন্নাহর আলোকে অত্যন্ত বিস্তারিত, প্রামাণিক এবং সহীহ তথ্য প্রদান করবেন। "
                        "উত্তর দেওয়ার সময় অবশ্যই সংশ্লিষ্ট আয়াতের তিলাওয়াত, হাদিসের আরবি ইবারত, এবং প্রামাণিক কিতাবের নাম "
                        "(যেমন বুখারী, মুসলিম, শামী ইত্যাদি) ও পৃষ্ঠা/হাদিস নম্বর উল্লেখ করবেন।"
                    )
                }
            ]

            # আগের কথোপকথনগুলো যোগ করা (যাতে আগের কথা মনে রাখতে পারে)
            for m in st.session_state.messages:
                if isinstance(m.get("content"), str):
                    messages_payload.append({"role": m["role"], "content": m["content"]})

            # Groq API কল করা (সঠিক ও আপডেট মডেল নাম ব্যবহার করা হয়েছে)
            chat_completion = client.chat.completions.create(
                messages=messages_payload,
                model="llama-3.3-70b-versatile",
                temperature=0.4,
                max_tokens=4096
            )

            bot_response = chat_completion.choices[0].message.content

        # বটের উত্তর হিস্টরিতে এবং স্ক্রিনে যোগ করা
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(bot_response)

    except Exception as e:
        st.error(f"দুঃখিত, একটি সমস্যা হয়েছে: {e}")
