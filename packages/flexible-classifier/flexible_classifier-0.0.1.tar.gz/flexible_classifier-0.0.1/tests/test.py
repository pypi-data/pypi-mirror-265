from flexible_classifier import classifier
import pandas as pd

salaries = pd.read_csv('./data/ds_salaries.csv')
classifier.process_data('./data/ds_salaries.csv', 'experience_level')

# customers1 = pd.read_csv('./data/Train.csv', index_col='ID')
# customers2 = pd.read_csv('./data/Test.csv', index_col='ID')
# customers = pd.concat([customers1, customers2])
# classifier.process_data(customers, 'Segmentation')


salaries = pd.read_csv('../../tests/data/ds_salaries.csv')
process_data('../../tests/data/ds_salaries.csv', 'experience_level')