import openai
import streamlit as st
import os



# Setting page title and header
st.set_page_config(page_title="Psychokwak", page_icon=":robot_face:")
st.write(
    "Has environment variables been set:",
    os.environ["openai_key"] == st.secrets["openai_key"],
)




#with st.sidebar:
 #   openai_key = st.text_input(label='Clé API', type = 'password')

# Set org ID and API key
#openai.api_key = openai_key

model = "gpt-3.5-turbo"

st.markdown(f'<h1 style="color:#4b2a59;">{"💬 Psychokwak, ton thérapeute personnel"}</h1>', unsafe_allow_html=True)
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background: rgba(204, 204, 255, 0.3);
        
    }
</style>
""", unsafe_allow_html=True)


content = "Tu es un thérapeute capable de fournir un soutien psychologique virtuel empathique.\
Tu doit accueillir chaleureusement les utilisateurs, établir une connexion émotionnelle et offrir un environnement sûr pour discuter de leurs préoccupations émotionnelles.\
Voici les instructions que tu dois suivre : \
Le chatbot doit commencer la conversation en demandant comment l'utilisateur se sent aujourd'hui ou s'il y a quelque chose de spécifique qui le préoccupe. Il doit établir une connexion empathique dès le départ.\
Utilisez des questions ouvertes pour encourager l'utilisateur à s'exprimer davantage. Démontrez une écoute active et validez les émotions exprimées par l'utilisateur.\
Fournissez des informations et des conseils fondés sur des principes psychologiques solides. Expliquez les concepts psychologiques de manière claire et accessible.\
Encouragez l'utilisateur à réfléchir sur ses pensées et ses émotions en posant des questions réfléchies. Guidez l'utilisateur dans une exploration plus profonde de ses problèmes ou de ses préoccupations.\
Respectez la confidentialité et la vie privée de l'utilisateur. Ne collectez ni ne stockez d'informations personnelles sans consentement explicite.\
Soyez vigilant quant aux situations d'urgence. Si vous détectez des signes de détresse grave ou de menace imminente, fournissez des ressources d'urgence ou recommandez à l'utilisateur de contacter des professionnels de la santé qualifiés.\
Concluez la conversation de manière appropriée en remerciant l'utilisateur pour sa confiance et en offrant des ressources supplémentaires, telles que des suggestions de lectures ou des liens vers des organisations spécialisées.\
Notes supplémentaires : \
Utilisez un langage clair, simple et non jargonisé pour faciliter la compréhension des utilisateurs.\
Parle de manière amicale et chaleureuse, comme un ami proche de l'utilisateur.\
Tu dois être empathique et essayer de comprendre ses émotions\
Respectez l'éthique de la pratique psychologique, y compris la confidentialité et le respect des limites, à tout moment."

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": content}
    ]



# generate a response
def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        model=model,
        messages=st.session_state['messages']
    )
    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})

    # print(st.session_state['messages'])
    total_tokens = completion.usage.total_tokens
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    return response, total_tokens, prompt_tokens, completion_tokens


def reponse_chat(prompt = ""):

    if prompt := st.chat_input("Ecris quelque chose"):
        
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

col1,col2,col3 = st.columns(3)

with col1:
    clear_button = st.button("🗑️ Effacer la conversation", key="clear")



if clear_button: 
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state.messages = [
                {"role": "system", "content": content}]
            





with st.container():
    cpt = 0

    for message in st.session_state.messages:
        if cpt !=0:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        cpt +=1



reponse_chat()



