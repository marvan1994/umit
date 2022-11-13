import pandas as pd
import json
import os



with open(r'umit_info_spec.json', 'r') as f:
    main_dict = json.loads(f.read())


df_dict = {file.split('_')[1].split('.')[0]:pd.read_excel(f'./umit_files/{file}') for file in os.listdir('umit_files')}