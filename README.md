# DTMF encoder and decoder w/ bandpass filters

DSP course assignment. Create a DTMF decoder with bandpass filters.

## Run
```bash
pip3 install -r requirements.txt
```

### Encoder

```bash
python3 encode_DTMF_signal.py <number you want to encode>
```
This will create a .wav file where each character has a duration of 0.6 seconds including pause.

### Decoder

```bash
python3 decode_DTMF_signal.py <.wav file> <number of characters>
```

This will return you the characters which are encoded in the .wav file.

**NOTE**: you have to know how many numbers are encoded or there will be an error/mistake.

## TODO
- clean up code, organize in functions, more comments
- fix number of characters
