import streamlit as st
import data_handler as dh
import util 
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import requests
import json

if not util.check_password():
    st.stop()  # Do not continue if check_password is not True.

API_URL = 'http://localhost:8000'

#dados = dh.load_data()

response = requests.get(f'{API_URL}/get_titanic_data/')

dados = None

if response.status_code == 200:
    dados_json = json.loads(response.json())
    dados = pd.DataFrame(dados_json)
else:
    print("Error: ", response.status_code)

data_analyses_on = st.toggle('Mostrar gráficos')

# model = pickle.load(open('./models/model.pkl', 'rb'))


if(data_analyses_on):
    st.dataframe(dados)
    st.header('Histograma das idade')
    fig = plt.figure()
    plt.hist(dados['Age'], bins=30)
    plt.xlabel('Idade')
    plt.ylabel('Quantidade')
    st.pyplot(fig)

    st.header('Sobreviventes')
    st.bar_chart(dados['Survived'].value_counts())

st.header('Preditor de Sobrevivência')

col1, col2, col3 = st.columns(3)

with col1:
    classes = ["1st", "2nd", "3rd"]
    p_class = st.selectbox('Ticket class', classes)

with col2:
    classes = ['Male', 'Female']
    sex = st.selectbox('Sex', classes)

with col3:
    age = st.number_input('Age', min_value=0, max_value=100, value=0, step=1)

col1, col2, col3 = st.columns([2,2,1])

with col1:
    sib_sp = st.number_input('Number of siblings/spouses aboard', step=1)

with col2:
    par_ch = st.number_input('Number of parents/children aboard', step=1)

with col3:
    fare = st.number_input('Passenger fare')

col1, col2 = st.columns(2)

with col1:
    classes = ['Cherbourg', 'Queenstown', 'Southampton']
    embarked = st.selectbox('Port of Embarkation', classes)
with col2:
    submit = st.button('Verificar')

if(submit or 'survived' in st.session_state):

    passageiro = {
        'Pclass': p_class,
        'Sex': sex,
        'Age': age,
        'SibSp': sib_sp,
        'Parch': par_ch,
        'Fare': fare,
        'Embarked': embarked
    }

    # values = pd.DataFrame([passageiro])
    # st.dataframe(values)

    # results = model.predict(values)

    passageiro_json = json.dumps(passageiro)

    response = requests.post(f'{API_URL}/predict/', json=passageiro_json)

    results = None

    if response.status_code == 200:
        results = response.json()
    else:
        print("Error: ", response.status_code)

    if results is not None:
        survived = results
        if survived == 1:
            st.subheader('Passageiro Sobreviveu')
            if 'survived' in st.session_state:
                st.balloons()
        else:
            st.subheader('Passageiro Não sobreviveu ')
            if 'survived' in st.session_state:
                st.snow()
            
    st.session_state['survived'] = survived

    if passageiro and 'survived' in st.session_state:
        st.write('A predição está correta?')

        col1, col2, col3 = st.columns([1,1,5])

        with col1:
            correct_prediction = st.button('Sim')

        with col2:
            wrong_prediction = st.button('Não')

        if correct_prediction or wrong_prediction:
            message = "Muito obrigado pelo feedback"
            if wrong_prediction:
                message += ", iremos usar esses dados para melhorar as predições"
            message += "."
            
            # adiciona no dict do passageiro se a predição está correta ou não
            if correct_prediction:
                passageiro['CorrectPrediction'] = True
            elif wrong_prediction:
                passageiro['CorrectPrediction'] = False
                
            # adiciona no dict do passageiro se ele sobreviveu ou não
            passageiro['Survived'] = st.session_state['survived']
            
            # escreve a mensagem na tela
            st.write(message)
            print(message)
            
            # salva a predição no JSON para cálculo das métricas de avaliação do sistema
            # dh.save_prediction(passageiro)
            passageiro_json = json.dumps(passageiro)
            response = requests.post(f'{API_URL}/save_prediction/', json=passageiro_json)

            if response.status_code == 200:
                print("passageiro salvo")
            else:
                print("Error: ", response.status_code)

        st.write('')
        # adiciona um botão para permitir o usuário realizar uma nova análise
        col1, col2, col3 = st.columns(3)
        with col2:
            new_test = st.button('Iniciar Nova Análise')
            
            # se o usuário pressionar no botão e já existe um passageiro, remove ele do cache
            if new_test and 'survived' in st.session_state:
                del st.session_state['survived']
                st.rerun()
        accuracy_predictions_on = st.toggle('Exibir acurácia')

        if accuracy_predictions_on:
            
            predictions = None

            response = requests.post(f'{API_URL}/get_all_predictions/', json=dados_json)

            if response.status_code == 200:
                predictions = response.json()
            else:
                print("Error: ", response.status_code)

            num_total_predictions = len(predictions)
            
            accuracy_hist = [0]
            
            correct_predictions = 0
            
            for index, passageiro in enumerate(predictions):
                total = index + 1
                if passageiro['CorrectPrediction'] == True:
                    correct_predictions += 1
                    
                temp_accuracy = correct_predictions / total if total else 0
                
                accuracy_hist.append(round(temp_accuracy, 2))

            accuracy = correct_predictions / num_total_predictions if num_total_predictions else 0

            st.metric(label='Acurácia', value=round(accuracy, 2))
            # TODO: usar o attr delta do st.metric para exibir a diferença na variação da acurácia
            
            # exibe o histórico da acurácia
            st.subheader("Histórico de acurácia")
            st.line_chart(accuracy_hist)

    