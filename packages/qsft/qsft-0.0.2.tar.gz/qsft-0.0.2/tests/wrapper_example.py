# import colorama
import numpy as np

from qsft.wrapper import sparse_transform
from synt_src.synthetic_signal import generate_signal_w
from qsft.utils import dec_to_qary_vec

if __name__ == '__main__':

    '''
    Generate a synthetic test signal
    '''
    n = 20
    q = 5
    sparsity = 1000
    a_min = 1
    a_max = 1
    max_weight = 5
    noise_sd = 0

    signal_w, locq, strengths = generate_signal_w(n, q, sparsity, a_min, a_max, noise_sd, full=False, max_weight=max_weight)
    freq_normalized = 2j * np.pi * locq / q

    def test_function(query_batch):
        query_indices_qary_batch = np.array(dec_to_qary_vec(query_batch, q, n)).T
        output = np.exp(query_indices_qary_batch @ freq_normalized) @ strengths
        return output

    '''
    Use sparse_transform method to compute the Fourier transform
    '''
    result = sparse_transform(test_function, q=q, n=n, max_degree=max_weight, noise_sd=noise_sd)

    '''
    Display the Reported Results
    '''
    qsft = result.get("qsft")
    loc = result.get("locations")
    n_used = result.get("n_samples")
    peeled = result.get("locations")
    avg_hamming_weight = result.get("avg_hamming_weight")
    max_hamming_weight = result.get("max_hamming_weight")

    # def color_sign(x):
    #     c = colorama.Fore.RED if x > 0 else colorama.Fore.RESET
    #     return f'{c}{x}{colorama.Fore.RESET}'
    #
    # np.set_printoptions(formatter={'int': color_sign}, threshold=10000, linewidth=2000)

    print("found non-zero indices QSFT: ")
    print(peeled)
    print("True non-zero indices: ")
    print(locq.T)
    print("Total samples = ", n_used)
    print("Total sample ratio = ", n_used / q ** n)
    signal_w_diff = signal_w.copy()
    for key in qsft.keys():
        signal_w_diff[key] = signal_w_diff.get(key, 0) - qsft[key]
    print("NMSE SPRIGHT= ",
          np.sum(np.abs(list(signal_w_diff.values())) ** 2) / np.sum(np.abs(list(signal_w.values())) ** 2))
    print("AVG Hamming Weight of Nonzero Locations = ", avg_hamming_weight)
    print("Max Hamming Weight of Nonzero Locations = ", max_hamming_weight)
