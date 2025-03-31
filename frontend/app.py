import streamlit as st
import requests
import time

# API Endpoints
CHAT_API_URL = "https://<your-backend-app-name>.azurewebsites.net/ask"
RECOMMEND_API_URL = "https://<your-backend-app-name>.azurewebsites.net/recommend"
QUIZ_API_URL = "https://<your-backend-app-name>.azurewebsites.net/quiz"

st.title("🎓 AI Learning Companion")

# ============================
# Feature Selection
# ============================
st.sidebar.header("Select a Feature")
feature = st.sidebar.radio(
    "What would you like to do?",
    ("Ask AI Anything", "Get Personalized Recommendations", "Generate a Quiz")
)

# =======================
# Section 1: General Chat
# =======================
if feature == "Ask AI Anything":
    st.header("💬 Ask AI Anything")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Let's start chatting! 👇"}]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Ask your question here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Call the backend API to get the assistant's response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            try:
                response = requests.post(CHAT_API_URL, json={"question": prompt})
                if response.status_code == 200:
                    assistant_response = response.json().get("response", "Sorry, I couldn't process that.")
                else:
                    assistant_response = "Error: Unable to fetch response from the server."
            except Exception as e:
                assistant_response = f"Error: {str(e)}"

            # Simulate stream of response with milliseconds delay
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# ===============================
# Section 2: Personalized Learning
# ===============================
elif feature == "Get Personalized Recommendations":
    st.header("📚 Personalized Learning Recommendations")

    # User inputs
    topic = st.text_input("What topic do you want to learn?")
    goal = st.text_input("What is your learning goal?")

    if st.button("Get Personalized Study Plan"):
        if topic and goal:
            response = requests.post(RECOMMEND_API_URL, json={"topic": topic, "goal": goal})
            if response.status_code == 200:
                st.write("**Recommended Study Plan:**")
                st.success(response.json().get("recommendation"))
            else:
                st.error("Error fetching recommendation!")
        else:
            st.warning("Please enter both topic and goal!")

# ============================
# Section 3: Quiz Generation
# ============================
elif feature == "Generate a Quiz":
    st.header("📝 Generate a Quiz")

    quiz_topic = st.text_input("Enter a topic for the quiz:")

    if st.button("Generate Quiz"):
        if quiz_topic:
            response = requests.post(QUIZ_API_URL, json={"topic": quiz_topic})
            if response.status_code == 200:
                st.write("**Generated Quiz:**")
                st.success(response.json().get("quiz"))
            else:
                st.error("Error generating quiz!")
        else:
            st.warning("Please enter a topic for the quiz!")
