import numpy as np


def _robust_noise_std(signal, trim_percent=5.0):
	if signal.size == 0:
		raise ValueError("Signal is empty")
	if trim_percent < 0 or trim_percent >= 50:
		raise ValueError("trim_percent must be in [0, 50)")

	sorted_vals = np.sort(signal)
	trim = int(round((trim_percent / 100.0) * sorted_vals.size))
	if trim == 0:
		trimmed = sorted_vals
	else:
		trimmed = sorted_vals[trim:-trim]
	if trimmed.size == 0:
		raise ValueError("Trim removed all samples")
	return float(np.std(trimmed, ddof=0))


def snr_from_file(
	data_path,
	column=0,
	delimiter=" ",
	skip_header=1,
	trim_percent=5.0,
	use_abs_max=True,
):
	"""
	Compute SNR as max amplitude divided by robust noise std.

	Args:
		data_path (str): Path to data file.
		column (int): Column index for signal.
		delimiter (str): File delimiter.
		skip_header (int): Lines to skip at top of file.
		trim_percent (float): Percent to trim from both ends for noise std.
		use_abs_max (bool): Use max absolute amplitude if True.

	Returns:
		dict: {"snr": float, "max_amp": float, "noise_std": float}
	"""
	data = np.genfromtxt(data_path, delimiter=delimiter, skip_header=skip_header)
	if data.ndim == 1:
		signal = data
	else:
		if column < 0 or column >= data.shape[1]:
			raise ValueError("column index out of range")
		signal = data[:, column]

	if signal.size == 0:
		raise ValueError("Signal is empty")

	max_amp = float(np.max(np.abs(signal)) if use_abs_max else np.max(signal))
	noise_std = _robust_noise_std(signal, trim_percent=trim_percent)
	if noise_std == 0:
		raise ValueError("Noise std is zero; SNR is undefined")

	return {
		"snr": max_amp / noise_std,
		"max_amp": max_amp,
		"noise_std": noise_std,
	}


def snr_from_file_all(
	data_path,
	delimiter=" ",
	skip_header=1,
	trim_percent=5.0,
	use_abs_max=True,
):
	"""
	Compute SNR for all columns in a file.

	Returns:
		list: SNR values per column (or one value for 1D data).
	"""
	data = np.genfromtxt(data_path, delimiter=delimiter, skip_header=skip_header)
	if data.ndim == 1:
		signal = data
		max_amp = float(np.max(np.abs(signal)) if use_abs_max else np.max(signal))
		noise_std = _robust_noise_std(signal, trim_percent=trim_percent)
		if noise_std == 0:
			raise ValueError("Noise std is zero; SNR is undefined")
		return [max_amp / noise_std]

	results = []
	for idx in range(data.shape[1]):
		signal = data[:, idx]
		if signal.size == 0:
			raise ValueError("Signal is empty")
		max_amp = float(np.max(np.abs(signal)) if use_abs_max else np.max(signal))
		noise_std = _robust_noise_std(signal, trim_percent=trim_percent)
		if noise_std == 0:
			raise ValueError("Noise std is zero; SNR is undefined")
		results.append(max_amp / noise_std)

	return results

