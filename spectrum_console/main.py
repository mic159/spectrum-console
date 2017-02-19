# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import pyaudio
from numpy.fft import rfft
from numpy import int16, empty, fromstring, roll

CHUNK = 32 # Size of each 'frame' in rolling buffer
FFT_LEN = CHUNK*8 # size of rolling buffer for FFT
SIGNAL_SCALE = 0.000005 # Scaling factor for output
RATE = 16000 # Sampling rate
HEIGHT = 4


SPARKS = [
  ' ',
  '\u2581',
  '\u2582',
  '\u2583',
  '\u2584',
  '\u2585',
  '\u2586',
  '\u2587',
  '\u2588'
]
SPARKS_LEN = len(SPARKS)


def spark(i, full):
    i = min(int(max(0.0, i) * SPARKS_LEN), SPARKS_LEN-1)
    if full > 3.0:
        return '\033[0;31m' + SPARKS[i] + '\033[0m'
    return SPARKS[i]


def run():
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1, # Mono
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )
    signal = empty(FFT_LEN, dtype=int16)

    try:
        # Disable cursor
        sys.stdout.write('\033[?25l')
        while 1:
            # Roll in new frame into buffer
            try:
                frame = stream.read(CHUNK)
            except IOError as e:
                if e[1] != pyaudio.paInputOverflowed:
                    raise
                continue
            signal = roll(signal, -CHUNK)
            signal[-CHUNK:] = fromstring(frame, dtype=int16)

            # Now transform!
            fftspec = list(abs(x * SIGNAL_SCALE) for x in rfft(signal)[:CHUNK*3])

            # Print it
            lines = [
                ''.join(spark(x - i+1, x) for x in fftspec)
                for i in range(HEIGHT, 0, -1)
            ]
            sys.stdout.write('│' + '│\n│'.join(lines) + '│')
            sys.stdout.write('\033[3A\r')
    except KeyboardInterrupt:
        sys.stdout.write('\n' * HEIGHT)
    finally:
        # Turn the cursor back on
        sys.stdout.write('\033[?25h')


if __name__ == "__main__":
    run()
