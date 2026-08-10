# Velocity X

An open drone simulator for visual-inertial odometry research under aggressive flight,
with ground truth that is **exact by construction** rather than measured.

**[→ Launch it in your browser](https://error404-wq.github.io/vio_simulator/)** — nothing to install.

---

## Why this exists

Aggressive-flight benchmarks record ground truth with motion-capture or total-station rigs.
Those references are excellent at low frequency and heavily filtered at high frequency —
which is exactly the band a drone occupies when it is doing something interesting.

When the reference cannot resolve the motion, measured error stops being a property of your
algorithm and becomes a property of the yardstick. We measured this: a reference bandwidth
below 5 Hz can inflate apparent gyroscope error by up to **10×** and manufacture correlation
between sensors whose errors are genuinely independent.

A simulator does not have that problem. The trajectory is a closed-form function, so its
derivatives are exact at every frequency.

## What is exact, and what is modelled

| Quantity | Status |
|---|---|
| Per-pixel depth | **Exact** — analytic ray–plane intersection, verified to 4.4×10⁻¹⁶ m |
| Pose & angular rate | **Exact** — closed form, integrated on SO(3) |
| Projection & lens | **Exact** — equidistant fisheye, ~115° FOV |
| Motion blur | Integrated sub-exposures (not a fixed convolution) |
| IMU noise | Modelled — calibrated to real in-flight noise (~9× datasheet) |
| Photon & read noise | Modelled — standard sensor physics |
| Event generation | Modelled — **not calibrated against a real sensor** |

That last row matters. Conclusions that depend on the event model are assumptions, not
measurements. See [Validation](https://error404-wq.github.io/vio_simulator/validation.html).

## Install

```bash
git clone https://github.com/ayushsankar12/Velocity-X.git
cd vio_simulator
pip install numpy scipy opencv-python
```

## Quick start

```python
import numpy as np
from sim.scene import Camera, render
from sim.worlds import corridor, add_obstacles
from sim.trajectory import Trajectory

cam   = Camera.davis346(noise_std=5.0, use_fisheye=True)
scene = add_obstacles(corridor(seed=42), count=8, seed=142)
traj  = Trajectory(peak_omega=4.0, omega_hz=0.6, speed=6.0)

R = traj.rotation(np.array([0.5]), duration=2.0)[0]
p = traj.position(np.array([0.5]))[0]

image, depth = render(scene, cam, R, p)   # depth is metric, per-pixel, exact
```

Full API in the [documentation](https://error404-wq.github.io/vio_simulator/docs.html).

## Site layout

| Page | Contents |
|---|---|
| `index.html` | Landing page — static, loads instantly |
| `simulator.html` | Interactive simulator (PyScript; the only page that loads Python) |
| `validation.html` | How the simulator is verified, and where it should not be trusted |
| `docs.html` | Installation, API, conventions |
| `research.html` | Findings, including negative results |
| `about.html` | About the author |

The landing page is deliberately free of PyScript so first-time visitors are not made to
wait on a Pyodide download before seeing anything.

## Contributing

Issues and pull requests welcome — including corrections. If a number here is wrong, that
is a bug worth reporting.

## License

MIT © Ayush Sankar
