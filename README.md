# GPU Power Draw Visualizer (TUI)

This is a simple command line application that displays the power draw of an NVIDIA GPU over time.

YouTube video where I use this to give a live demo of [Zeus](https://ml.energy/zeus): https://youtu.be/aZoD-jgO3fE?t=747

I wrote this (with the help of ChatGPT) for a live demo, so I made it extra-resilient to potential errors that might crash the program.
The TUI should survive terminal resizing events and random curses errors.

If you need a programmatic GPU energy measurement tool, check out the [Zeus repository](https://github.com/ml-energy/zeus). [`ZeusMonitor`](https://ml.energy/zeus/reference/monitor/energy/#zeus.monitor.energy.ZeusMonitor) is built for that.

## How to use

This application requires NVML (`libnvidia-ml.so`) on your system. It comes together with the CUDA toolkit.
The Python package `nvidia-ml-py` is merely a wrapper of the library and will fail if it cannot find `libnvidia-ml.so` on your system.

```console
$ pip install nvidia-ml-py
$ python power_monitor.py
```
