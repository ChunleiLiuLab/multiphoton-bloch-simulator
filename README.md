# Multiphoton Bloch Simulator

A Python C-extension multiphoton Bloch simulator with support for an optional,
time-varying longitudinal field `b1z`. Multiphoton excitation is implemented
by combining transverse RF excitation with this oscillating longitudinal field.
The simulator also accepts general `b1z` waveforms and conventional excitation
with `b1z=None`.

This repository is based on
[`utcsilab/bloch-simulator-python`](https://github.com/utcsilab/bloch-simulator-python)
at commit
[`94826e5`](https://github.com/utcsilab/bloch-simulator-python/commit/94826e5).
That project adapts Brian Hargreaves's original MATLAB/MEX Bloch simulator to a
Python C extension. This version adds `b1z` to the Python wrapper and C
simulation path for use with longitudinally modulated excitation waveforms.

## Installation

The extension requires Python development headers, a C compiler, NumPy, SciPy,
and Matplotlib. From a repository clone:

```bash
python -m pip install -e .
```

The build configuration supplies NumPy headers in pip's isolated build
environment. The inherited C interface currently requires NumPy 1.x
(`numpy>=1.22,<2`).

To build the extension in place instead:

```bash
python setup.py build_ext --inplace
```

## Usage

```python
from bloch import bloch

mx, my, mz = bloch(
    b1,
    gr,
    tp,
    t1,
    t2,
    df,
    dp,
    mode,
    mx=None,
    my=None,
    mz=None,
    b1z=None,
)
```

Inputs use the conventions of the upstream simulator:

- `b1`: complex transverse RF field in gauss, with one value per time sample.
- `b1z`: optional real longitudinal field in gauss, with one value per time
  sample. `None` is equivalent to an all-zero waveform.
- `gr`: gradient waveform in G/cm, with up to three spatial dimensions.
- `tp`: time interval or intervals in seconds.
- `t1`, `t2`: relaxation times in seconds.
- `df`: off-resonance in Hz.
- `dp`: spatial positions in cm.
- `mode`: upstream simulation-mode bit mask. Bit 0 requests steady state and
  bit 1 records all time points.

The C core uses `GAMMA = 26753.0 rad/s/G`. A positive constant `b1z` therefore
contributes the same z rotation as a positive off-resonance of
`b1z * GAMMA / (2*pi)` Hz.

`b1z` is a general waveform input and is not restricted to a particular pulse
sequence or multiphoton-excitation method.

## Tests

```bash
python -m unittest discover -s bloch/tests -v
```

The inherited tests compare against MATLAB-generated fixtures. The additional
`b1z` tests check that:

- omitted and zero-valued `b1z` inputs are equivalent;
- a constant `b1z` matches the corresponding off-resonance shift;
- a time-varying waveform matches analytical z rotation; and
- mismatched waveform lengths fail clearly.

## Attribution

The original Bloch equation simulator was written as MATLAB/MEX code by Brian
Hargreaves at Stanford University. The Python C-extension adaptation was
created by Niraj Amalkanti. The upstream project also credits Miki Lustig for
MATLAB helper modules converted to Python, Jon Tamir for later modifications,
and NPann for assistance with a critical bug fix.

Please retain these acknowledgments when using or redistributing this modified
version.

If you use the `b1z` extension in published work, please also cite
“Multiphoton simultaneous transmission and reception MRI: Theory and
validation.” Complete publication details will be added when available.

## License

The upstream Python repository states that it is distributed under the same
terms as Brian Hargreaves's original Bloch simulator. This repository retains
that upstream attribution and licensing statement.
