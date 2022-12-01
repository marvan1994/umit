import streamlit as st

import pandas as pd

import json

from load_css import local_css

import pathlib

st.set_page_config(page_title='Привязка Подтем',
    page_icon="um.ico",)

local_css("style.css")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

all_subject_names = ['ang_ege', 'baz_ege', 'bio_ege', 'geo_ege', 'inf_ege', 'ist_ege', 'lit_ege', 'mat_ege',
                         'nem_ege', 'rus_ege', 'fiz_ege', 'him_ege', 'obs_ege']

def reset_session():
    st.session_state.subtheme = []


df = pd.read_csv('subtheme_sheet.csv', dtype=str)
df = df[['subject', 'class_year', 'section', 'subtheme', 'subtheme_id']]
df['class_year'] = df.class_year.map({'3': 'ege', '1': 'oge', '4': '10c'})

def show():

    st.sidebar.image('um.png', caption=None, width = 100, use_column_width='True', clamp=False, channels="RGB", output_format="auto")


    st.write(
        """
        ## Это программа для привязывания подтем
        """
    )

    def subtheme_add(subject_name,subject_info):


        df.fillna('', inplace=True)
        st.dataframe(df.query(f'subject == "{subject_name[0:3]}" and class_year == "{subject_name[-3:]}"'))


        if 'subtheme' not in st.session_state:
             st.session_state.subtheme = []

        section_names = list(subject_info['sections'].keys())
        section = st.selectbox(label = 'Выберите раздел', options = ['']+section_names , key = subject_name)

        if section !='':

            subtheme_number_to_name = {key: subject_info['subtheme_names'][key] for key in subject_info['subtheme_names'].keys()}
            subtheme_name_to_number = {value: key for (key, value) in subtheme_number_to_name.items()}


            section_number_list = subject_info['sections'][section]

            section_name_list = [subtheme_number_to_name[subtheme] for subtheme in section_number_list]

            for i in range(len(section_number_list)):

                if int(section_number_list[i]) in st.session_state.subtheme:

                    cheker = st.checkbox(f'{section_name_list[i]} ({int(section_number_list[i])})', key = subject_name+'_'+str(section_number_list[i]), value= True)

                else:
                    cheker = st.checkbox(f'{section_name_list[i]} ({int(section_number_list[i])})', key = subject_name+'_'+str(section_number_list[i]))


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




    with open('subtheme_info.json', 'r') as f:
        subtheme_info = json.loads(f.read())

    subject_names = subtheme_info.keys()


    subjects_inrus = ['Английский', "Базовая", "Биология", "География", "Информатика", "История", "Литература",
                      "Математика", "Немецкий", "Русский", "Физика", "Химия", 'Обществознание']
    subjects_ineng = ['ang', 'baz', 'bio', 'geo', 'inf', 'ist', 'lit', 'mat', 'nem', 'rus', 'fiz', 'him', 'obs']
    subject_dict = dict(zip(subjects_inrus, subjects_ineng))
    degree_dict = {'ЕГЭ':'ege', 'ОГЭ':'oge','10 класс':'10c'}


    subject = st.sidebar.selectbox('Выберите предмет', [''] + list(subject_dict.keys()))
    degree = st.sidebar.radio('Выберите направление', ['ЕГЭ', 'ОГЭ','10 класс'])


    try:
        subject_name = subject_dict[subject]+'_'+degree_dict[degree]
        if subject_name in subject_names:
            st.warning('Обратите внимание, это программа для подтем, а не умитов')
            st.markdown(f'##### Подтемы по предмету {subject} {degree}')

            subject_info = subtheme_info[subject_name]
            subtheme_add(subject_name, subject_info)

        else:

            st.markdown(f'##### Подтем по направлению {degree} по предмету {subject} не существует')
    except Exception as e:
        #print(str(e))
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


