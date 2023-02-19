import streamlit as st

import pandas as pd

import json

from load_css import local_css

import pathlib

st.set_page_config(page_title='Привязка Подтем',
    page_icon="um.ico",layout="wide")

local_css("style.css")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

all_speaker_name = ['Артур Шарафиев', 'Анастасия Малова', 'Александр Долгих',
       'Аля Виноградова', 'Фариша Князева', 'Аделия Адамова',
       'Жанна Казанская', 'Виктория Ларионова', 'Макс Тесла',
       'Надежда Ковалевская', 'Милена Соколова', 'Виктория Ланская',
       'Анастасия Майер', 'Семён Кравченко', 'Максим Кораблёв',
       'Елена Зеленская', 'Дарья Королёва', 'Ольга Чехова',
       'Александра Лебедева', 'Алина Вернадская', 'Андрей Баканчев',
       'Данир Баев', 'Богдан Чагин', 'Равиль Кандинский', 'Азат Антипов',
       'Вероника Соколовская', 'Дарья Львова', 'Анастасия Гласная',
       'Денис Марков', 'Артем Фролов', 'Алина Максимова', 'Никита Павлов',
       'Лина Клевер', 'Шерин Келли', 'Айнур Даллас', 'Айбулат Чева',
       'Кристина Лазарева', 'Александра Май', 'Кристина Мельникова',
       'Никита Сахаров', 'Татьяна Граева', 'Никита Равич',
       'Елизавета Островская', 'Евгений Тьюринг', 'Илья Кузьмин',
       'Мария Вельф', 'Анастасия Аддамс', 'Софья Вайб']

def reset_session():
    st.session_state.subtheme = []


df = pd.read_csv('subtheme_import_v2.csv', dtype=str).rename(columns = {'Спикер':'speaker', 'Раздел':'section', 'Подтема':'subtheme','Айди подтемы':'subtheme_id'})
df = df[['speaker','section', 'subtheme', 'subtheme_id','theme_complexity','subtheme_complexity']]

def show():

    st.sidebar.image('um.png', caption=None, width = 100, use_column_width='True', clamp=False, channels="RGB", output_format="auto")


    st.write(
        """
        ## Это программа для привязывания подтем
        """
    )

    def subtheme_add(speaker_name,speaker_info):


        df.fillna('', inplace=True)
        st.dataframe(df.query(f'speaker == "{speaker_name}"'))


        if 'subtheme' not in st.session_state:
             st.session_state.subtheme = []

        section_names = list(speaker_info['sections'].keys())
        section = st.selectbox(label = 'Выберите раздел', options = ['']+section_names)

        if section !='':

            subtheme_number_to_name = {key: speaker_info['subtheme_names'][key] for key in speaker_info['subtheme_names'].keys()}
            subtheme_name_to_number = {value: key for (key, value) in subtheme_number_to_name.items()}


            section_number_list = speaker_info['sections'][section]

            section_name_list = [subtheme_number_to_name[subtheme] for subtheme in section_number_list]

            for i in range(len(section_number_list)):

                if int(section_number_list[i]) in st.session_state.subtheme:

                    cheker = st.checkbox(f'{section_name_list[i]} ({int(section_number_list[i])})', key = speaker_name+'_'+str(section_number_list[i]), value= True)

                else:
                    cheker = st.checkbox(f'{section_name_list[i]} ({int(section_number_list[i])})', key = speaker_name+'_'+str(section_number_list[i]))


                if cheker:

                    current_state = list(set(st.session_state.subtheme))
                    current_state.extend([int(section_number_list[i])])
                    current_state = list(set(current_state))
                    st.session_state.subtheme = current_state

                else:
                    current_state = list(set(st.session_state.subtheme))

                    if int(section_number_list[i]) in st.session_state.subtheme:
                        current_state = st.session_state.subtheme
                        current_state.remove(int(section_number_list[i]))
                        st.session_state.subtheme = current_state




    with open('subtheme_info_v2.json', 'r') as f:
        subtheme_info = json.loads(f.read())

    speaker = st.sidebar.selectbox('Выберите преподавателя', [''] + all_speaker_name)


    try:
            st.warning('Обратите внимание, это программа для подтем, а не умитов')
            st.markdown(f'##### Подтемы преподавателя {speaker}')
            speaker_info = subtheme_info[speaker]
            subtheme_add(speaker, speaker_info)
    except Exception as e:
        pass
    show_subtheme()

def show_subtheme():

    t1 = st.sidebar.empty()
    t1.markdown('# Здесь будут отображаться ID подтем')
    if 'subtheme' in st.session_state:

        current_state = st.session_state.subtheme

        if len(current_state) !=0:

            current_state.sort()
            current_state_str = [str(item) for item in current_state]
            t1.text_area(label = 'ID подтем можно копировать отсюда',value=','.join(current_state_str))
            istrue = st.sidebar.button('Очистить подтемы')
            if istrue:
                reset_session()
                current_state_str = [str(item) for item in st.session_state.subtheme]
                t1.markdown(','.join(current_state_str))


show()


