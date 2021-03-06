from neo import SpikeTrain
from quantities import s
import pandas as pd
import numpy as np


def df_to_neo(df, stop='max'):
    '''convert a spiketime dataframe to a list of neo spike trains
    returns:
        ids, neo_list'''
    if stop == 'baseline':
        stop = 60 * 60
    elif stop == 'cond1':
        stop = 120 * 60
    elif stop == 'cond 2':
        stop = 180 * 60
    elif stop == 'max':
        stop = np.max(df['spike_times']) / 30000
    g = df.groupby('neuron_id')['spike_times']
    return g.apply(len).index.values, g.apply(neo_transformer, stop=stop)


def neo_transformer(col, stop):
    col = col.divide(30000)
    return SpikeTrain(col.values, t_stop=stop, units=s)


def neo_to_df(a_sig_list, ids):
    '''given a list of neo analog signals, returns those signals in a dataframe'''
    df_list = [pd.DataFrame(a_sig) for a_sig in a_sig_list]
    df = pd.concat(df_list, axis=1)
    df.columns = ids
    return df
