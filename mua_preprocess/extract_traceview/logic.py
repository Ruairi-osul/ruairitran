from extract_traceview.funcs import *


def main(ops):
    data = load_raw_data(kilosort_folder=ops.kilosort_folder, recording=ops.recording, num_channels=ops.num_channels)
    spike_clusters, spike_times, cluster_groups = load_data(recording=ops.recording, kilosort_folder=ops.kilosort_folder, verbose=ops.verbose)
    df, cluster_to_plot = choose_cluster_to_plot(cluster_groups=cluster_groups, spike_clusters=spike_clusters, spike_times=spike_times, chosen_cluster=ops.chosen_cluster)
    print('Cluster ID: ' + str(cluster_to_plot))
    extracted_spikes = df[df['cluster'] == cluster_to_plot]['spike_times']

    Spike_chosen = choosing_spike(extracted_spikes=extracted_spikes, time_chosen=ops.time_chosen)

    plt.figure(figsize=(15, 10))

    chosen_channel = choose_channel(Spike_chosen=Spike_chosen, extracted_spikes=extracted_spikes, time_span=ops.time_span, data=data, broken_chans=ops.broken_chans, num_spikes_for_averaging=ops.num_spikes_for_averaging)

    print('Channel to plot: ' + str(chosen_channel))

    df_trace = extract_trace(Spike_chosen=Spike_chosen, extracted_spikes=extracted_spikes, time_span=ops.time_span, data=data, chosen_channel=chosen_channel)

    plt.plot(df_trace['time'], df_trace['Value'], color='gray')

    for spike in np.arange(Spike_chosen - 2, Spike_chosen + 3):

        df_highlight = spike_highlight(spike=spike, extracted_spikes=extracted_spikes, data=data, chosen_channel=chosen_channel)
        plt.plot(df_highlight['time'], df_highlight['Value'], color='b')

    plot_final_data(kilosort_folder=ops.kilosort_folder, recording=ops.recording)