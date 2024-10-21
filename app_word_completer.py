import streamlit as st
import gdown
import tensorflow as tf
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

def load_model():
     url = 'https://drive.google.com/ud?id=1L_vCM0lUTI3tejprp_O1KYUqPnUn-7e-'
     gdown.download(url, 'model_seer_keras')
     loaded_model = tf.keras.models.load_model('model_seer.keras')
     with open ('vectorizer.pkl', 'rb') as file:
          vectorizer = pickel.load(file)

    return loaded_model, vectorizer

# código omitido

def predict_next_words(model, vectorizer, text, max_sequence_len, top_k=3):
    """
    Prediz as próximas palavras mais prováveis em uma sequência de texto.

    Args:
        model: O modelo treinado.
        vectorizer: A camada de vetorização.
        text: O texto de entrada.
        max_sequence_len: O comprimento máximo da sequência usado na vetorização.
        top_k: O número de palavras mais prováveis a serem retornadas.

    Returns:
        As próximas palavras mais prováveis.
    """
    # Vetorizar o texto de entrada
    tokenized_text = vectorizer([text])

    # Remover a dimensão extra adicionada pela vetorização
    tokenized_text = np.squeeze(tokenized_text)

    # Adicionar padding à esquerda
    padded_text = pad_sequences([tokenized_text], maxlen=max_sequence_len, padding='pre')

    # Fazer a previsão
    predicted_probs = model.predict(padded_text, verbose=0)[0]  # Remove a dimensão extra adicionada pela previsão

    # Obter os índices dos top_k tokens com as maiores probabilidades
    top_k_indices = np.argsort(predicted_probs)[-top_k:][::-1]

    # Converter os tokens previstos de volta para palavras
    predicted_words = [vectorizer.get_vocabulary()[index] for index in top_k_indices]

    return predicted_words

# código omitido

def main():

    max_sequence_len = 50

    #load the model
    loaded_model, vectorizer

    st.title('Next Word Prediction')
    input_text = st.text_input('Enter a text string:')

    if st.button('Predict'):
         if input_text:
              try:
                   predicted_words = predicted_next_words(load_model, vectorizer, input_text, max_sequence_len)
                   st.info('Most likely words')

                   for word in predicted_words:
                        st.sucess(word)
                except:
                   st.error('Error in prediction {e}')

        else:
            st.warning('Please insert some text')


if __name__ == "__main__":
     main()