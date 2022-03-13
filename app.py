import pandas as pd

import streamlit as st

import  plotly.express as px

import os

import json

from PIL import Image

from load_css import local_css

st.set_page_config(page_title='Уровни знаний')

local_css("style.css")

def text_in_orange_highlight(text):

    return "<div style= \"horizontal-align: middle;\" > <span class='highlight orange'> {0} </span><div>".format(text)

def text_in_red_color(text):

    return "<h1 style = \"font-size: 12px; color: #800000\"> {0} </h1>".format(text)

def text_for_section(text):

    return "<pre style = \"font-size: 22px; color: #FFBF00\"> {0}  </pre>".format(text)

def text_for_theme(text):

    return "<pre style = \"font-size: 14px; color: #7A3803\"> {0} </pre>".format('\t\t'+text)



def result_view(stud_info,subject_name):

    results = stud_info['subjects'][subject_name]

    sections = stud_info['subjects'][subject_name]['sections'].keys()

    for section in sections:
        section_knowledge = stud_info['subjects'][subject_name]['sections'][section]['knowledge']
        #if float(section_knowledge) != 0:

        st.markdown(text_for_section(section.replace('\n','') +'\t' + str(round(float(section_knowledge)*100,1))+' %'),unsafe_allow_html=True )

        themes = stud_info['subjects'][subject_name]['sections'][section]['themes'].keys()

        for theme in themes:
            theme_knowledge = stud_info['subjects'][subject_name]['sections'][section]['themes'][theme]['knowledge']

            #if float(theme_knowledge) != 0:
            st.markdown(text_for_theme(theme.replace('\n','') + '\t' + str(round(float(theme_knowledge) * 100, 1)) + ' %'),
                        unsafe_allow_html=True)


def get_stud_info(stud_id,subject_name):
#    if stud_vk == '...':
#
 #       st.markdown(text_in_red_color('Не забудь вписать свой вк'),unsafe_allow_html = True)
#
#    else:
    students = os.listdir('./stud_info')

        #if 'vk.com/' not in stud_vk:

        #    st.markdown(text_in_red_color('Вставь пожалуйста полную ссылку в вк '), unsafe_allow_html=True)

        #else:
            #stud_id = vk_id.split('vk.com/')[1]
            
    stud_id = f'stud_{stud_id}_info.json'

    if stud_id not in students:

        st.markdown(text_in_red_color('Такого ID не найдено ... '), unsafe_allow_html = True)
    else:
        st.markdown(text_in_red_color('Подожди минутку, сейчас все посчитаем...'), unsafe_allow_html = True)

        with open('./stud_info/'+stud_id, 'r+') as f:

            stud_info = json.loads(f.read())

            result_view(stud_info,subject_name)



#st.markdown(t, unsafe_allow_html=True)
st.markdown(text_in_orange_highlight('Исскуственный интеллект от Умскул'),unsafe_allow_html=True)

st.subheader('Тут ты сможешь узнать свои уровни знаний!')

stud_id = st.text_input('Введите id', key = 'input')
subject_name = stud_id[0:7]
st.button('Запустить вычисление', on_click=get_stud_info(stud_id,subject_name))
#st.markdown(text_in_red_color('С тобой говорит исскуственный интеллект от Умскул'),unsafe_allow_html=True)



