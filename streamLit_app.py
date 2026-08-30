import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(
    page_title="Bhagavad Gita RAG",
    page_icon="🙏",
    layout="centered",
)

st.title("Bhagavad Gita AI Assistant")

with st.sidebar:

    st.header("About")


    st.divider()

    st.info(
        "Answers are grounded in the "
        "uploaded Bhagavad Gita document."
    )

if "messages" not in st.session_state:

    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

question = st.chat_input(
    "Ask something about the Bhagavad Gita..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):

        st.markdown(
            question
        )

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Searching the Bhagavad Gita..."
        ):

            try:

                response = requests.post(
                    API_URL,
                    json={
                        "question": question
                    },
                    timeout=300,
                )

                if response.status_code == 200:

                    data = response.json()

                    answer = data.get(
                        "answer",
                        "No answer received.",
                    )

                    st.markdown(
                        answer
                    )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                        }
                    )
                else:

                    try:

                        error_data = (
                            response.json()
                        )

                        error_message = (
                            error_data.get(
                                "detail",
                                "Unknown API error.",
                            )
                        )

                    except Exception:

                        error_message = (
                            response.text
                        )

                    st.error(
                        f"API Error: {error_message}"
                    )


            
            except requests.exceptions.ConnectionError:

                st.error(
                    """
                    FastAPI server is not running.

                    """
                )

            except requests.exceptions.Timeout:

                st.error(
                    """
                    Request timed out.

                    Your 8 GB RAM system may need
                    more time for the local model.
                    """
                )

            except Exception as error:

                st.error(
                    f"Unexpected error: {error}"
                )