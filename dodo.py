from operator import itemgetter
from pathlib import Path

import tomlkit

base_dir = Path(__file__).parent
config = tomlkit.loads((base_dir / "config.toml").read_text())

data_dir = base_dir / str(config["DATA_DIR"])
data_dir.mkdir(exist_ok=True)

results_dir = base_dir / str(config["RESULTS_DIR"])
results_dir.mkdir(exist_ok=True)

info_files = list(data_dir.rglob("info.toml"))
lattices_by_namespace = {
    path.parent.stem: tomlkit.loads(path.read_text()) for path in info_files
}


lattices_all = []
lattices_by_simulation = {}
for namespace, lattices in lattices_by_namespace.items():
    for name, lattice in lattices.items():
        lattice["namespace"] = namespace
        lattice["name"] = name
        lattices_all.append(lattice)
        for simulation in lattice["simulations"]:
            try:
                lattices_by_simulation[simulation].append(lattice)
            except KeyError:
                lattices_by_simulation[simulation] = [lattice]


def task_convert_lattices():
    "Convert lattice files into different formats"
    from actions.convert_lattices import __file__ as python_file
    from actions.convert_lattices import action

    for lattice in lattices_all:
        namespace, name = itemgetter("namespace", "name")(lattice)
        source_dir = data_dir / namespace
        # TODO: is there a better way?
        source = next(source_dir.glob(f"{name}.*"))
        target_base = results_dir / namespace / name / name
        target_base.parent.mkdir(parents=True, exist_ok=True)
        targets = [
            target_base.with_suffix(".json"),
            target_base.with_suffix(".lte"),
            target_base.with_suffix(".madx"),
        ]
        yield {
            "name": source,
            "actions": [(action, [source, targets])],
            "targets": targets,
            "file_dep": [python_file, source],
            "clean": True,
        }


def task_index_json():
    "Create global index.json from all info.toml files"
    import json

    def action(path, data):
        with path.open("w") as file:
            json.dump(data, file)

    index_path = results_dir / "index.json"
    yield {
        "name": "index.json",
        "actions": [(action, (index_path, lattices_all))],
        "targets": [index_path],
        "file_dep": info_files,
    }


def task_index_json_per_lattice():
    "Similar to task_index.json, but info file per lattice."
    import json

    def save_data(path, data):
        path.write_text(json.dumps(data))

    for lattice in lattices_all:
        namespace, name = itemgetter("namespace", "name")(lattice)
        info_file = data_dir / namespace / "info.toml"
        target = results_dir / namespace / name / "index.json"
        target.parent.mkdir(parents=True, exist_ok=True)

        yield {
            "name": f"{namespace}/{name}",
            "actions": [(save_data, (target, lattice))],
            "targets": [target],
            "file_dep": [info_file],
            "clean": True,
        }


def task_lattice_info():
    from actions.lattice_info import __file__ as python_file
    from actions.lattice_info import action, targets

    for lattice in lattices_all:
        namespace, name = itemgetter("namespace", "name")(lattice)
        output_dir = results_dir / namespace / name
        lattice_path = (results_dir / namespace / name / name).with_suffix(".json")
        yield {
            "name": f"{namespace}/{name}",
            "actions": [(action, (lattice, lattice_path, output_dir))],
            "targets": [output_dir / path for path in targets],
            "file_dep": [python_file, lattice_path],
            "clean": True,
        }


def task_apace_summary():
    "Generate lattice summaries using apace"
    from actions.twiss_apace import __file__ as python_file
    from actions.twiss_apace import action, targets

    for lattice in lattices_by_simulation["apace"]:
        namespace, name = itemgetter("namespace", "name")(lattice)
        lattice_path = (results_dir / namespace / name / name).with_suffix(".json")
        output_dir = results_dir / namespace / name / "apace"
        # TODO: what does clean do??
        yield {
            "name": f"{namespace}/{name}",
            "actions": [(action, (lattice, lattice_path, output_dir))],
            "targets": [output_dir / path for path in targets],
            "file_dep": [python_file, lattice_path],
            "clean": True,
        }


def task_elegant_twiss_simulation():
    from actions import config_dir
    from actions.twiss_elegant import simulation_elegant_dir

    for lattice in lattices_by_simulation["elegant"]:
        namespace, name, energy = itemgetter("namespace", "name", "energy")(lattice)
        run_file = config_dir / "twiss.ele"
        lattice_path = (results_dir / namespace / name / name).with_suffix(".lte")
        target = (simulation_elegant_dir / namespace / name).with_suffix(".twi")
        target.parent.mkdir(parents=True, exist_ok=True)
        yield {
            "name": f"{namespace}/{name}",
            "actions": [
                f"elegant {run_file} -macro=energy={energy},lattice={lattice_path},filename={target} > /dev/null"
            ],
            "targets": [target],
            "file_dep": [run_file, lattice_path],
            "clean": True,
        }


def task_elegant_summary():
    from actions.twiss_elegant import __file__ as python_file
    from actions.twiss_elegant import action, simulation_elegant_dir, targets

    for lattice in lattices_by_simulation["elegant"]:
        namespace, name = itemgetter("namespace", "name")(lattice)
        output_dir = results_dir / namespace / name / "elegant"
        twi_data_path = (simulation_elegant_dir / namespace / name).with_suffix(".twi")
        yield {
            "name": f"{namespace}/{name}",
            "actions": [(action, (twi_data_path, output_dir))],
            "targets": [output_dir / path for path in targets],
            "file_dep": [python_file, twi_data_path],
            "clean": True,
        }


def task_madx_summary():
    from actions.twiss_madx import __file__ as python_file
    from actions.twiss_madx import action, targets

    for lattice in lattices_by_simulation["madx"]:
        namespace, name = itemgetter("namespace", "name")(lattice)
        lattice_path = (results_dir / namespace / name / name).with_suffix(".madx")
        output_dir = results_dir / namespace / name / "madx"
        yield {
            "name": f"{namespace}/{name}",
            "actions": [(action, (lattice, lattice_path, output_dir))],
            "targets": [output_dir / path for path in targets],
            "file_dep": [python_file, lattice_path],
            "clean": True,
        }
