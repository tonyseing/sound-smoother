
KAISER_FILTER = [-0.01452123, -0.0155227 , 0.01667252, 0.01800633, -0.01957209, -0.0214361 , 0.02369253, 0.02647989, -0.03001054, -0.03462755, 0.04092347, 0.05001757, -0.06430831, -0.09003163, 0.15005272, 0.45015816, 0.45015816, 0.15005272, -0.09003163, -0.06430831, 0.05001757, 0.04092347, -0.03462755, -0.03001054, 0.02647989, 0.02369253, -0.0214361 , -0.01957209, 0.01800633, 0.01667252, -0.0155227 , -0.01452123]


def decimate_by_2(signal):
    return signal[::2]

def sublists(lst, sublist):
    num_windows = len(lst) + len(sublist) - 1
    padded_lst = [0] * (len(sublist)-1) + lst + [0] * (len(sublist)-1)
    sublists = [padded_lst[i:i+len(sublist)] for i in range(num_windows)]
    return list(sublists)

def convolution(kernel, signal):
    reversed_kernel = kernel[::-1]
    signal_chunks = sublists(signal, kernel)
    num_windows = len(signal_chunks)
    window_product = lambda idx: [signal_chunk * kernel for signal_chunk, kernel in zip(signal_chunks[idx], kernel)]
    window_sum = lambda idx: sum(window_product(idx))
    c = [window_sum(idx) for idx in range(num_windows)]
    return c

def low_pass_filter(signal):
    convolved = convolution(KAISER_FILTER, signal)
    applied_kaiser = [2 * i for i in convolved]
    return applied_kaiser

def downsample_by_2(signal):
    lp_filtered_signal = low_pass_filter(signal)
    return decimate_by_2(lp_filtered_signal)
