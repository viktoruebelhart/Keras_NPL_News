import streamlit as st
import tensorflow as tf
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import gdown
import os

@st.cache_resource
def load_model():
    # Link atualizado para download direto
    url = 'https://drive.google.com/uc?id=1L_vCM0lUTI3tejprp_O1KYUqPnUn-7e-'
    output = 'model_seer.keras'
    
    # Baixando o modelo
    gdown.download(url, output, quiet=False)

    # Verifique se o arquivo foi baixado corretamente
    if not os.path.exists(output):
        st.error("Failed to download model.")
        return None, None

    # Carregando o modelo
    loaded_model = tf.keras.models.load_model(output)

    # Carregando o vetor de vetorização
    with open('vectorizer.pkl', 'rb') as file:
        vectorizer = pickle.load(file)

    return loaded_model, vectorizer

# Função omitida

def predict_next_words(model, vectorizer, text, max_sequence_len, top_k=3):
    # Vetorizar o texto de entrada
    tokenized_text = vectorizer([text])

    # Remover a dimensão extra adicionada pela vetorização
    tokenized_text = np.squeeze(tokenized_text)

    # Adicionar padding à esquerda
    padded_text = pad_sequences([tokenized_text], maxlen=max_sequence_len, padding='pre')

    # Fazer a previsão
    predicted_probs = model.predict(padded_text, verbose=0)[0]

    # Obter os índices dos top_k tokens com as maiores probabilidades
    top_k_indices = np.argsort(predicted_probs)[-top_k:][::-1]

    # Converter os tokens previstos de volta para palavras
    predicted_words = [vectorizer.get_vocabulary()[index] for index in top_k_indices]

    return predicted_words

# Função omitida

def main():
    max_vocab_size = 20000
    max_sequence_len = 50

    # Carregar o modelo e vetorizar
    loaded_model, vectorizer = load_model()

    st.title('Next Word Prediction')
    input_text = st.text_input('Enter a text string:')

    if st.button('Predict'):
        if input_text:
            try:
                predicted_words = predict_next_words(loaded_model, vectorizer, input_text, max_sequence_len)
                st.info('Most likely words:')

                for word in predicted_words:
                    st.success(word)
            except Exception as e:
                st.error(f'Error in prediction: {e}')
        else:
            st.warning('Please insert some text')

if __name__ == "__main__":
    main()
