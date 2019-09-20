# sound-smoother
Sound filter that smooths audio input

In this exercise, we will implement a simple approach to downsample an audio signal by a factor
of two. Changing the sample rate is one of the most common data permutations taken when
working with audio data, and specifically this exercise will describe how to accomplish this using
a specific kind of low pass filter across the audio data, and then performing decimation.

![](https://github.com/tonyseing/sound-smoother/blob/master/images/lowpass.png?raw=true)  

![](https://github.com/tonyseing/sound-smoother/blob/master/images/decimation.png?raw=true)  

![](https://upload.wikimedia.org/wikipedia/commons/2/21/Comparison_convolution_correlation.svg)
