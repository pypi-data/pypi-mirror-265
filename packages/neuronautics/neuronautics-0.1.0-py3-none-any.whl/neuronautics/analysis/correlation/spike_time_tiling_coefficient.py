from neuronautics.analysis.type.graph_analysis import GraphAnalysis
from neuronautics.analysis.helpers import to_timeseries
from neuronautics.config.layout import Layout
import numpy as np
import neo
import quantities as pq
from elephant.spike_train_correlation import spike_time_tiling_coefficient


class SpikeTimeTilingCoefficient(GraphAnalysis):

    def get_input_params(self):
        """Get the input parameters for the activity correlation analysis.

        Returns:
            list: A list of dictionaries, each describing an input parameter.
                Each dictionary includes 'name', 'min', 'max', 'default', and 'type' keys.

        """
        return [
            {'name': 'corr_thr', 'min': 0, 'max': 1, 'default': 0.3, 'type': 'float'}
        ]

    def run(self, spikes, corr_thr, *args, **kwargs):
        """Run the activity correlation analysis.

        Args:
            spikes (DataFrame): A DataFrame containing spike data.
            corr_thr (float): The correlation threshold for considering correlations.

        Returns:
            ndarray: A boolean matrix indicating correlations above the threshold.

        """
        spikes['class'] = spikes['class'].astype(int)
        spikes = spikes[spikes['class'] >= 0]  # remove noise  TODO: hardcoded 0
        spikes = spikes[['channel_id', 'ts_ms']].copy().reset_index(drop=True)
        max_ms = spikes.ts_ms.max()
        spikes = spikes.groupby('channel_id').agg(list)
        spikes = spikes.to_dict()['ts_ms']

        spikes = {ch_id: neo.SpikeTrain(spike, units='ms', t_stop=max_ms) for (ch_id, spike) in spikes.items()}

        layout = Layout().current()
        max_lay = np.max([np.max([int(l) for lay in layout for l in lay if l != ''])])
        w_ij = np.zeros((max_lay, max_lay))

        channel_ids = list(spikes.keys())

        for ix, ch1 in enumerate(channel_ids):
            for ch2 in channel_ids[ix+1:]:
                coef = spike_time_tiling_coefficient(spikes[ch1], spikes[ch2])
                w_ij[ch1, ch2] = coef
                w_ij[ch2, ch1] = coef

        return w_ij > corr_thr
    
    def plot(self, *args, **kwargs):
        """Plot the activity correlation analysis.

        Args:
            *args: Variable-length positional arguments.
            **kwargs: Variable-length keyword arguments.

        Returns:
            object: matplotlib figure

        """
        return super().plot('Spike Time Tiling Coefficient', *args, **kwargs)
