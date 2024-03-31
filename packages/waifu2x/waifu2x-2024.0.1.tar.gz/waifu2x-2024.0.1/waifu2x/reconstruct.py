from __future__ import annotations

import chainer
import numpy as np
from chainer.link import Chain
from PIL import Image


def _get_padding_size(size: int, block_size: int, offset: int) -> int:
	pad = size % block_size
	return offset if pad == 0 else block_size - pad + offset


def blockwise(src: np.ndarray, model: Chain, block_size: int, batch_size: int):
	if src.ndim == 2:
		src = src[:, :, np.newaxis]
	xp = model.xp

	inner_block_size = block_size // model.inner_scale
	inner_offset = model.offset // model.inner_scale
	in_block_size = inner_block_size + inner_offset * 2

	in_h, in_w, ch = src.shape
	out_h, out_w = in_h * model.inner_scale, in_w * model.inner_scale
	in_ph = _get_padding_size(in_h, inner_block_size, inner_offset)
	in_pw = _get_padding_size(in_w, inner_block_size, inner_offset)
	out_ph = _get_padding_size(out_h, block_size, model.offset)
	out_pw = _get_padding_size(out_w, block_size, model.offset)

	psrc = np.pad(src, ((inner_offset, in_ph), (inner_offset, in_pw), (0, 0)), "edge")
	nh = (psrc.shape[0] - inner_offset * 2) // inner_block_size
	nw = (psrc.shape[1] - inner_offset * 2) // inner_block_size
	psrc = psrc.transpose(2, 0, 1)

	x = np.zeros((nh * nw, ch, in_block_size, in_block_size), dtype=np.uint8)
	for i in range(nh):
		ih = i * inner_block_size
		for j in range(nw):
			jw = j * inner_block_size
			psrc_ij = psrc[:, ih : ih + in_block_size, jw : jw + in_block_size]
			x[(i * nw) + j, :, :, :] = psrc_ij

	y = xp.zeros((nh * nw, ch, block_size, block_size), dtype=xp.float32)
	with chainer.no_backprop_mode(), chainer.using_config("train", value=False):
		for i in range(0, nh * nw, batch_size):
			batch_x = xp.array(x[i : i + batch_size], dtype=np.float32) / 255
			batch_y = model(batch_x)
			y[i : i + batch_size] = batch_y.data
	y = chainer.backends.cuda.to_cpu(y)

	dst = np.zeros((ch, out_h + out_ph, out_w + out_pw), dtype=np.float32)
	for i in range(nh):
		ih = i * block_size
		for j in range(nw):
			jw = j * block_size
			dst[:, ih : ih + block_size, jw : jw + block_size] = y[(i * nw) + j]

	dst = dst[:, :out_h, :out_w]
	return dst.transpose(1, 2, 0)


def inv(rot: int, *, flip: bool = False):
	if flip:
		return lambda x: np.rot90(x, rot // 90, axes=(0, 1))[:, ::-1, :]
	return lambda x: np.rot90(x, rot // 90, axes=(0, 1))


def get_tta_patterns(src: np.ndarray, n: int):
	src_lr = src.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
	patterns = [
		[src, None],
		[src.transpose(Image.Transpose.ROTATE_90), inv(-90)],
		[src.transpose(Image.Transpose.ROTATE_180), inv(-180)],
		[src.transpose(Image.Transpose.ROTATE_270), inv(-270)],
		[src_lr, inv(0, flip=True)],
		[src_lr.transpose(Image.Transpose.ROTATE_90), inv(-90, flip=True)],
		[src_lr.transpose(Image.Transpose.ROTATE_180), inv(-180, flip=True)],
		[src_lr.transpose(Image.Transpose.ROTATE_270), inv(-270, flip=True)],
	]
	if n == 2:
		return [patterns[0], patterns[4]]
	if n == 4:
		return [patterns[0], patterns[2], patterns[4], patterns[6]]
	if n == 8:
		return patterns
	return [patterns[0]]


def image_tta(src: Image.Image, model: Chain, tta_level: int, block_size: int, batch_size: int):
	inner_scale = model.inner_scale
	dst = np.zeros((src.size[1] * inner_scale, src.size[0] * inner_scale, 3))
	patterns = get_tta_patterns(src, tta_level)
	if model.ch == 1:
		for i, (pat, inv_) in enumerate(patterns):
			pat = np.array(pat.convert("YCbCr"), dtype=np.uint8)
			if i == 0:
				cbcr = pat[:, :, 1:]
			tmp = blockwise(pat[:, :, 0], model, block_size, batch_size)
			if inv_ is not None:
				tmp = inv_(tmp)
			dst[:, :, 0] += tmp[:, :, 0]
		dst /= len(patterns)
		dst = np.clip(dst, 0, 1) * 255
		dst[:, :, 1:] = cbcr
		dst = dst.astype(np.uint8)
		dst = Image.fromarray(dst, mode="YCbCr").convert("RGB")
	elif model.ch == 3:
		for i, (pat, inv_) in enumerate(patterns):
			pat = np.array(pat, dtype=np.uint8)
			tmp = blockwise(pat, model, block_size, batch_size)
			if inv_ is not None:
				tmp = inv_(tmp)
			dst += tmp
		dst /= len(patterns)
		dst = np.clip(dst, 0, 1) * 255
		dst = Image.fromarray(dst.astype(np.uint8))
	return dst


def image(src, model, block_size: int, batch_size: int) -> Image.Image:
	if src is None:
		return src
		# raise RuntimeError("Image cannot be None")
	if model.ch == 1:
		y2rgb = src.mode == "L"
		src = np.array(src.convert("YCbCr"), dtype=np.uint8)
		dst = blockwise(src[:, :, 0], model, block_size, batch_size)
		dst = np.clip(dst, 0, 1) * 255
		src[:, :, 0] = dst[:, :, 0]
		dst = Image.fromarray(src, mode="YCbCr")
		dst = dst.split()[0] if y2rgb else dst.convert("RGB")
	elif model.ch == 3:
		y2rgb = src.mode == "L"
		if y2rgb:
			src = src.convert("RGB")
		src = np.array(src, dtype=np.uint8)
		dst = blockwise(src, model, block_size, batch_size)
		dst = np.clip(dst, 0, 1) * 255
		dst = Image.fromarray(dst.astype(np.uint8))
		if y2rgb:
			dst = dst.convert("YCbCr").split()[0]
	return dst
