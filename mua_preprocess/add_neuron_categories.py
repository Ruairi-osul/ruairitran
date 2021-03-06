import pandas as pd
import os
from glob import glob

path_to_neuron_stats = r'/media/ruairi/Ephys_back_up_1/SERT_DREADD/csvs'
neuron_stats_csv_name = 'neuron_stats'

path_to_ts = r'/media/ruairi/Ephys_back_up_1/SERT_DREADD/csvs/spikes_time_series'

file_out_dir = r'/media/ruairi/Ephys_back_up_1/SERT_DREADD/csvs'
file_out_name_ts = 'all_neurons_ts_with_clusters.csv'


def load_spikes_df(parent_dir):
    sub_dirs = os.listdir(parent_dir)
    df_list = []
    for sub_dir in sub_dirs:
        file_path = glob(os.path.join(parent_dir, sub_dir, '*.csv'))[0]  # should be only one csv file
        df_list.append(pd.read_csv(file_path))
    return pd.concat(df_list)


def load_neuron_stats(path, csv_name):
    if not csv_name.endswith('.csv'):
        csv_name = ''.join([csv_name, '.csv'])
    return pd.read_csv(os.path.join(path, csv_name))


def neuron_category_mapper(row):
    '''
    This is the function we use to categorise neurons as either slow or fast, and as either regular or irregular
    It categorises neurons firing slower than 4.5 Hz as slow and neurons with a CV ISI of less than 0.55 as regular
    '''
    if (row['Firing Rate'] <= 10) & (row['CV ISI'] <= 0.8):
        rate = 'slow'
        reg = 'regular'
    elif (row['Firing Rate'] <= 10) & (row['CV ISI'] >= 0.8):
        rate = 'slow'
        reg = 'irregular'
    elif (row['Firing Rate'] > 10) & (row['Firing Rate'] <25):
        rate= 'fast'
        reg = 'firing'
    else:
        rate= 'V.fast'
        reg = 'firing'
    return ' '.join([rate, reg])

df_ts = load_spikes_df(path_to_ts)
df_stats = load_neuron_stats(path=path_to_neuron_stats, csv_name=neuron_stats_csv_name)
df_stats['category'] = df_stats.apply(neuron_category_mapper, axis=1)
df_ts_merge = pd.merge(left=df_ts,
                       right=df_stats[['recording', 'category', 'spike_cluster']],
                       left_on=['recording', 'spike_cluster'],
                       right_on=['recording', 'spike_cluster'],
                       how='right')

df_ts_merge.to_csv(os.path.join(file_out_dir, file_out_name_ts), index=False)
df_stats.to_csv(os.path.join(file_out_dir, neuron_stats_csv_name) + '.csv',
                index=False)
