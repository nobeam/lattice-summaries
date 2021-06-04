import json
from pathlib import Path

import apace as ap
import matplotlib.pyplot as plt
import numpy as np

from . import FIG_SIZE

targets = [
    "twiss_tables.json",
    "twiss.svg",
    "floor_plan.svg",
]


def action(lattice, lattice_path: Path, output_dir: Path):
    output_dir.mkdir(exist_ok=True)

    print("Compute simulation data")
    lattice_obj = ap.Lattice.from_file(lattice_path)
    twiss_data = ap.Twiss(lattice_obj, energy=lattice["energy"], steps_per_meter=100)

    print("Generating tables 📝")
    with (output_dir / targets[0]).open("w") as file:
        json.dump(twiss_tables(twiss_data), file)

    print("Generating twiss plot 📊")
    twiss_plot(twiss_data).savefig(output_dir / targets[1])

    print("Generating floor plan 📊")
    floor_plan_plot(lattice_obj).savefig(output_dir / targets[2])


def twiss_tables(twiss: ap.Twiss):
    return [
        [
            "Optical Functions",
            [targets[1]],
        ],
        [
            "Detailed Lattice Parameter",
            [
                [
                    ["Qₓ", twiss.tune_x],
                    # TODO: fix chroma in apace
                    # ["Chromaticity x", twiss.chromaticity_x],
                    ["βₓ,ₘₐₓ / m", np.max(twiss.beta_x)],
                    ["βₓ,ₘᵢₙ / m", np.min(twiss.beta_x)],
                    ["βₓ,ₘₑₐₙ / m", np.mean(twiss.beta_x)],
                    ["ηₓ,ₘₐₓ / m", np.max(twiss.eta_x)],
                ],
                [
                    ["Qᵧ", twiss.tune_y],
                    # TODO: fix chroma in apace
                    # ["Chromaticity y", twiss.chromaticity_y],
                    ["βᵧ,ₘₐₓ / m", np.max(twiss.beta_y)],
                    ["βᵧ,ₘᵢₙ / m", np.min(twiss.beta_y)],
                    ["βᵧ,ₘₑₐₙ / m", np.mean(twiss.beta_y)],
                    ["ηᵧ,ₘₐₓ / m", 0],
                ],
                [
                    ["Mom. compaction", twiss.alpha_c],
                    ["Emittance", twiss.emittance_x],
                    ["I₁", twiss.i1],
                    ["I₂", twiss.i2],
                    ["I₃", twiss.i3],
                    ["I₄", twiss.i4],
                    ["I₅", twiss.i5],
                ],
            ],
        ],
        [
            "Floor plan",
            [targets[2]],
        ],
    ]


def twiss_plot(twiss: ap.Twiss):
    from math import floor, log10

    from apace.plot import Color, draw_elements, draw_sub_lattices, plot_twiss

    factor = np.max(twiss.beta_x) / np.max(twiss.eta_x)
    eta_x_scale = 10 ** floor(log10(factor))
    cell = twiss.lattice.children[0]
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    ax.set_xlim(0, cell.length)
    plot_twiss(ax, twiss, scales={"eta_x": eta_x_scale})
    draw_elements(ax, cell, labels=len(cell.sequence) < 150)
    draw_sub_lattices(ax, cell, labels=len(cell.children) < 5)
    ax.grid(axis="y", color=Color.LIGHT_GRAY, linestyle="--", linewidth=1)
    plt.legend(
        bbox_to_anchor=(0, 1.05, 1, 0.2),
        loc="lower left",
        mode="expand",
        ncol=3,
        frameon=False,
    )
    fig.tight_layout()

    return fig


def floor_plan_plot(lattice: ap.Lattice):
    from apace.plot import floor_plan

    # fig_ring, ax = plt.subplots()
    # ax.axis("off")
    # floor_plan(ax, lattice, labels=False)

    fig_cell, ax = plt.subplots(figsize=FIG_SIZE)
    ax.axis("off")
    cell = lattice.children[0]
    floor_plan(ax, cell)
    return fig_cell
