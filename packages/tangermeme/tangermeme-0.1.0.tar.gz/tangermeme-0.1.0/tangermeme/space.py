# space.py
# Contact: Jacob Schreiber <jmschreiber91@gmail.com>

import numpy
import torch

from .utils import one_hot_encode
from .ersatz import multisubstitute
from .predict import predict


def space(model, X, motifs, spacing, start=None, alphabet=['A', 'C', 'G', 'T'], 
	args=None, batch_size=32, device='cuda', verbose=False):
	"""Runs a single spacing experiment and returns predictions.

	Given a predictive model, a set of motifs to insert and the spacings
	between them, and a set of background sequences, return the predictions 
	from the model when using the background sequences and after inserting 
	the motifs into the sequences.


	Parameters
	----------
	model: torch.nn.Module
		A PyTorch model to use for making predictions. These models can take in
		any number of inputs and make any number of outputs. The additional
		inputs must be specified in the `args` parameter.

	X: torch.tensor, shape=(-1, len(alphabet), length)
		A one-hot encoded set of sequences to have a motif inserted into.

	motifs: list of torch.tensor, shape=(-1, len(alphabet), motif_length)
		A list of strings or of one-hot encoded version of a short motif to 
		substitute into the set of sequences.

	spacing: list or int
		An integer specifying a constant spacing between all motifs or a list
		of spacings of length equal to n-1 where n is the number of motifs. If
		a list is provided, the $i$-th entry should be interpreted as the
		distance after the $i$-th motif that the $i+1$-th motif begins.

	start: int or None, optional
		The starting position of where to insert the motif. If None, insert the
		motif into the middle of the sequence such that the middle of the motif
		occurs at the middle of the sequence. Default is None.

	alphabet : set or tuple or list, optional
		A pre-defined alphabet where the ordering of the symbols is the same
		as the index into the returned tensor, i.e., for the alphabet ['A', 'B']
		the returned tensor will have a 1 at index 0 if the character was 'A'.
		Characters outside the alphabet are ignored and none of the indexes are
		set to 1. This is not necessary or used if a one-hot encoded tensor is
		provided for the motif. Default is ['A', 'C', 'G', 'T'].

	args: tuple or list or None
		An optional set of additional arguments to pass into the model. If
		provided, each element in the tuple or list is one input to the model
		and the element must be formatted to be the same batch size as `X`. If
		None, no additional arguments are passed into the forward function.
		Default is None.

	batch_size: int, optional
		The number of examples to make predictions for at a time. Default is 32.

	device: str or torch.device
		The device to move the model and batches to when making predictions. If
		set to 'cuda' without a GPU, this function will crash and must be set
		to 'cpu'. Default is 'cuda'. 

	verbose: bool, optional
		Whether to display a progress bar during predictions. Default is False.

	Returns
	-------
	y_before: torch.Tensor or list of torch.Tensors
		The predictions from the model before inserting the motif in. If the
		output from the model's forward function is a single tensor, it will
		return that. If the model outputs a list of tensors, it will return
		those.

	y_after: torch.Tensor or list of torch.Tensors
		The predictions from the model after inserting the motif in. If the
		output from the model's forward function is a single tensor, it will
		return that. If the model outputs a list of tensors, it will return
		those.
	"""

	X_perturb = multisubstitute(X, motifs, spacing, start=start, 
		alphabet=alphabet)
	y_before = predict(model, X, args=args, batch_size=batch_size, 
		device=device, verbose=verbose)
	y_after = predict(model, X_perturb, args=args, batch_size=batch_size, 
		device=device, verbose=verbose)

	return y_before, y_after
