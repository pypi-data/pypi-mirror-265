import numpy as np
from peel import QSFT
from query import get_reed_solomon_dec
from exps.synt_exp.synt_src.synthetic_signal import get_random_subsampled_signal
import colorama

if __name__ == '__main__':
    # np.random.seed(20)
    q = 19
    n = 128
    N = q ** n
    sparsity = 1000
    a_min = 1
    a_max = 1
    b = 2
    noise_sd = 1
    num_subsample = 3
    num_repeat = 2
    t = 6
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

    qsft_args = {
        "num_subsample": num_subsample,
        "num_repeat": num_repeat,
        "reconstruct_method_source": delays_method_source,
        "reconstruct_method_channel": delays_method_channel,
        "b": b,
        "noise_sd": noise_sd,
        "source_decoder": decoder
    }
    '''
    Generate a Signal Object
    '''
    test_signal = get_random_subsampled_signal(n=n,
                                               q=q,
                                               sparsity=sparsity,
                                               a_min=a_min,
                                               a_max=a_max,
                                               noise_sd=noise_sd,
                                               query_args=query_args,
                                               max_weight=t)
    '''
    Create a QSFT instance and perform the transformation
    '''
    sft = QSFT(**qsft_args)
    result = sft.transform(test_signal, verbosity=0, timing_verbose=True, report=True, sort=True)

    '''
    Display the Reported Results
    '''
    gwht = result.get("gwht")
    loc = result.get("locations")
    n_used = result.get("n_samples")
    peeled = result.get("locations")
    avg_hamming_weight = result.get("avg_hamming_weight")
    max_hamming_weight = result.get("max_hamming_weight")

    def color_sign(x):
        c = colorama.Fore.RED if x > 0 else colorama.Fore.RESET
        return f'{c}{x}'

    np.set_printoptions(formatter={'int': color_sign}, threshold=10000, linewidth=2000)

    print("found non-zero indices QSFT: ")
    print(peeled)
    print("True non-zero indices: ")
    print(test_signal.locq.T)
    print("Total samples = ", n_used)
    print("Total sample ratio = ", n_used / q ** n)
    signal_w_diff = test_signal.signal_w.copy()
    for key in gwht.keys():
        signal_w_diff[key] = signal_w_diff.get(key, 0) - gwht[key]
    print("NMSE SPRIGHT= ",
         np.sum(np.abs(list(signal_w_diff.values())) ** 2) / np.sum(np.abs(list(test_signal.signal_w.values())) ** 2))
    print("AVG Hamming Weight of Nonzero Locations = ", avg_hamming_weight)
    print("Max Hamming Weight of Nonzero Locations = ", max_hamming_weight)
