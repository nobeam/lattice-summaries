from pathlib import Path

from matplotlib import rcParams

FIG_SIZE = 8, 4.8
rcParams["font.family"] = "sans-serif"
rcParams["font.sans-serif"] = ["Inter"]

base_dir = Path(__file__).parent.parent

config_dir = base_dir / "config"
config_dir.mkdir(exist_ok=True)

simulation_dir = base_dir / "_simulations"
simulation_dir.mkdir(exist_ok=True)
