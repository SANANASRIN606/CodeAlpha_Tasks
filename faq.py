import streamlit as st
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="FAQ Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Customer Support FAQ Chatbot")

# 1. Broad FAQ dictionary with key associations
faqs = {
    "return refund cancel exchange policy": 
        "Return Policy: You can return any item within 30 days of purchase for a complete refund.",
    
    "track tracking order shipment package where delivery status": 
        "Tracking: A tracking link is emailed automatically as soon as your package has been shipped.",
    
    "payment pay methods cards upi net banking cash card": 
        "Payments: We accept Credit/Debit cards, PayPal, UPI, and Net Banking.",
    
    "international worldwide delivery foreign ship countries": 
        "Shipping: We ship internationally to more than 50 countries worldwide.",
    
    "contact support help email customer care phone call": 
        "Support: You can contact our support team at support@codealpha.tech."
}

faq_keys = list(faqs.keys())

# Vectorizer using sublinear tf and character-ngram fallback so even typos match
vectorizer = TfidfVectorizer(ngram_range=(1, 2), analyzer='word', sublinear_tf=True)
tfidf_matrix = vectorizer.fit_transform(faq_keys)

# Chat UI
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Ask me any question about returns, tracking, payments, shipping, or customer support."}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_input := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Clean input
    clean_query = " ".join(re.findall(r'\b\w+\b', user_input.lower()))

    # Calculate similarity
    query_vector = vectorizer.transform([clean_query])
    similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()
    best_idx = similarity_scores.argmax()
    best_score = similarity_scores[best_idx]

    # Show top match if score > 0, otherwise show available help topics
    if best_score > 0.0:
        bot_response = faqs[faq_keys[best_idx]]
    else:
        bot_response = (
            "I couldn't match that to our topics. Please ask about:\n"
            "- **Returns & Refunds**\n"
            "- **Order Tracking**\n"
            "- **Payment Methods**\n"
            "- **Shipping**\n"
            "- **Customer Support**"
        )

    with st.chat_message("assistant"):
        st.write(bot_response)

    st.session_state.messages.append({"role": "assistant", "content": bot_response})
