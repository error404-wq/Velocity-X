# Perfect VIO Simulator

This repository contains a lightweight, mathematically perfect drone simulator designed to test Visual-Inertial Odometry (VIO) algorithms under aggressive flight conditions.

## Why this exists
Aggressive flight benchmarks (like UZH-FPV) often suffer from Ground-Truth Bandwidth limitations. Their "Answer Keys" are heavily low-pass filtered, artificially inflating the apparent error of high-frequency sensors like cameras and gyroscopes.

This simulator solves that by generating **analytic, mathematically exact ground truth** while rendering highly realistic sensor data, allowing researchers to evaluate their tracking algorithms without benchmark confounds.

## Features
- **Exact Analytic Depth**: Depth maps are computed via exact ray-plane intersections, accurate to machine precision (`4.4e-16 m`). No Z-buffer quantization artifacts.
- **Controlled Aggressiveness**: Peak angular rate is an independent variable that can be swept effortlessly.
- **Equidistant Fisheye Lens**: Full support for real-world drone optics (~115° FOV), ensuring algorithms are tested against highly warped geometries.
- **Physically Integrated Motion Blur**: Sub-exposure integration captures spatially varying blur trajectories during violent spins.
- **Realistic Image Noise**: Simulates camera shot and readout noise.
- **Inertial Simulation**: Gyroscope and Accelerometer generation with tunable white noise and random walk biases.

## GitHub Pages Web UI
This simulator has been packaged to run natively in your web browser using **PyScript**. 

You can launch the interactive simulation directly from the GitHub Pages deployment. The web app allows you to tune parameters like Angular Rate, Camera Noise, and Fisheye mapping, and watch the drone flight render directly on a canvas in real-time.
