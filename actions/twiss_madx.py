import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from cpymad.madx import Madx

from . import FIG_SIZE

targets = [
    "twiss_tables.json",
    "twiss.svg",
]


def action(lattice, lattice_path: Path, output_dir: Path):
    output_dir.mkdir(exist_ok=True)

    print(f"Run madx simulation ⚙")
    twiss_data = twiss_simulation(lattice_path, lattice["energy"])

    print(f"Generating tables 📝")
    with (output_dir / targets[0]).open("w") as file:
        json.dump(twiss_tables(twiss_data), file)

    print(f"Generating twiss plot 📊")
    twiss_plot(twiss_data).savefig(output_dir / targets[1])


def twiss_simulation(path: Path, energy: float):
    madx = Madx(stdout=False)
    madx.options.info = False
    madx.command.beam(particle="electron", energy=energy, charge=-1)
    madx.input(path.read_text())
    return madx.twiss(chrom=True)


def twiss_tables(twiss):
    twiss = twiss.summary
    return [
        [
            "Optical Functions",
            [targets[1]],
        ],
        [
            "Detailed Lattice Parameter",
            [
                [
                    ["Energy", twiss.energy],
                    ["Mom. compaction", twiss.alfa],
                    ["transition energy", twiss.gammatr],
                ],
                [
                    ["tune x", twiss.q1],
                    ["chromaticity x", twiss.dq1],
                    ["max beta x", twiss.betxmax],
                    ["max eta x", twiss.dxmax],
                ],
                [
                    ["Tune y", twiss.q2],
                    ["Chromaticity y", twiss.dq2],
                    ["max beta y", twiss.betxmax],
                    ["max eta y", twiss.dymax],
                ],
            ],
        ],
        [
            "Synchrotron Radiation Integrals",
            [
                [
                    ["I1", twiss.synch_1],
                    ["I2", twiss.synch_2],
                    ["I3", twiss.synch_3],
                    ["I4", twiss.synch_4],
                    ["I5", twiss.synch_5],
                ]
            ],
        ],
    ]


def twiss_plot(twiss):
    from math import floor, log10

    factor = np.max(twiss.summary.betxmax) / np.max(twiss.summary.dxmax)
    eta_x_scale = 10 ** floor(log10(factor))
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    ax.plot(twiss["s"], twiss["betx"], "#EF4444")
    ax.plot(twiss["s"], twiss["bety"], "#1D4ED8")
    ax.plot(twiss["s"], eta_x_scale * twiss["dx"], "#10B981")
    ax.grid(color="#E5E7EB", linestyle="--", linewidth=1)
    ax.set_xlim(0, 20)  # TODO: use cell length!
    fig.tight_layout()
    return fig
