from cluster_heatmap.logic import main
from cluster_heatmap.classes import Options


ops = Options(csv_dir=r'/media/ruairi/Ephys_back_up_1/SERT_DREADD/csvs',
              csv_file_name='all_neurons_ts_with_clusters',
              out_folder=r'cluster_heat_maps',
              resample_period='5sec',
              category_column='category',
              rolling_periods=120,
              normalisation_method='zscore',
              vmin=-2.5,
              vmax=2.5)

if __name__ == '__main__':
    main(ops)
