import streamlit as st
import gdown

def load_model():
     url = 'https://drive.google.com/ud?id=1L_vCM0lUTI3tejprp_O1KYUqPnUn-7e-'
     gdown.download(url, 'model_seer_keras')
     loaded_model = tf.keras.models.load_model('model_seer.keras')
     with open ('vectorizer.pkl', 'rb') as file:
          vectorizer = pickel.load(file)

    return loaded_model, vectorizer

def main():

    max_sequence_len = 50

    #load the model
    loaded_model, vectorizer

    st.title('Next Word Prediction')
    input_text = st.text_input('Enter a text string:')

if __name__ == "__main__":
     main()