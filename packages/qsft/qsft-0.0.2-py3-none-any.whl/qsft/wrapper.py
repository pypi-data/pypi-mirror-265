import numpy as np
from .peel import QSFT
from .query import get_reed_solomon_dec
from .input_signal_subsampled import SubsampledSignal
from typing import Callable


def sparse_transform(func: Callable[[np.ndarray], np.ndarray], q: int, n: int, b=5,
                     max_degree=5, num_subsample=3, num_repeat=2, noise_sd=None, coded=True):
    """

    :param func: function to be transformed, input: ndarray of shape (batch_size, n), output: ndarray of shape (batch_size,)
    :param q: input alphabet size
    :param n: input length
    :param b:
    :type b: int
    :param max_degree:
    :type max_degree: int
    :param num_subsample:
    :type num_subsample: int
    :param num_repeat:
    :type num_repeat: int
    :param noise_sd: If provided, qsft will determine the thresholds based on this value.
    :type noise_sd: float
    :param coded:
    :type coded: bool
    :return: dictionary consisting of transform results
    """
    if coded:
        t = max_degree
        decoder = get_reed_solomon_dec(n, t, q)
        delays_method_source = "coded"
        delays_method_channel = "nso"

        query_args = {
            "query_method": "complex",
            "num_subsample": num_subsample,
            "delays_method_source": delays_method_source,
            "subsampling_method": "qsft",
            "delays_method_channel": delays_method_channel,
            "num_repeat": num_repeat,
            "b": b,
            "t": t
        }

        signal = SubsampledSignal(func=func,
                                  n=n,
                                  q=q,
                                  noise_sd=noise_sd,
                                  query_args=query_args,
                                  max_weight=t)

        qsft_args = {
            "num_subsample": num_subsample,
            "num_repeat": num_repeat,
            "reconstruct_method_source": delays_method_source,
            "reconstruct_method_channel": delays_method_channel,
            "b": b,
            "source_decoder": decoder
        }

        sft = QSFT(**qsft_args)

        return sft.transform(signal, verbosity=0, timing_verbose=True, report=True, sort=True)

    else:
        raise NotImplementedError
