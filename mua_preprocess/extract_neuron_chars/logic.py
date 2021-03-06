from extract_neuron_chars.funcs import *


def main(ops):
    create_dirs(ops.spikes_df_csv_out_folder)
    for recording in ops.recordings_to_extract:
        spike_clusters, spike_times, cluster_groups = load_data(recording=recording,
                                                                kilosort_folder=ops.kilosort_folder,
                                                                verbose=ops.verbose,
                                                                sep=ops.sep)
        good_cluster_numbers = get_good_cluster_numbers(cluster_groups)
        data = [spike_clusters.flatten(), spike_times.flatten()]
        create_good_spikes_df(data=data,
                              good_cluster_numbers=good_cluster_numbers,
                              sampling_rate=ops.sampling_rate,
                              experiment=ops.experiment,
                              verbose=ops.verbose,
                              recording=recording,
                              sep=ops.sep,
                              spikes_df_csv_out_folder=ops.spikes_df_csv_out_folder
                              )
