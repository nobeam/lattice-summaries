# Lattice Summaries

Framework to generate comparable summaries for different lattice files.

Can be used for local lattice development or to host a lattice database.

## Requirements

* Python 3.8 and Poetry (to manage dependencies)
* elegant

## Setup

Install the dependencies into new virtual environment:

```
poetry install
```

To make the **Lattice Summaries** useful for other facilities and to make it possible to use different lattice files during local development, lattice and other input files are stored in the `DATA_DIR` directory **separate** from this repository.

The `DATA_DIR` needs to have a folder structure like this:


```console
data
├── namespace-1
│  ├── bessy2_design-1996_v_1.json
│  ├── bessy2_stduser-2019-05-07-v_1.json
│  └── info.toml
├── namespace-2
│  ├── bessy3_5ba-20p_v_long-bend-tgrb.lte
│  ├── bessy3_5ba-20p_v_reference.lte
│  └── info.toml
...
```

Lattices must be stored in a [restricted/simplified format](lattice-file-requirements) to make it possible to convert them into different formats. The `info.toml` contains information and additional simulation parameters (e.g. energy). As an example you can check [NoBeam's lattice-summaries-data repository](https://github.com/nobeam/lattice-summaries-data).

The simulation results will be written to the `RESULTS_DIR` directory.

The paths of the `DATA_DIR` and `RESULTS_DIR` can be changed in the in `config.toml`. It's recommanded to make both of these directories Git repositories as well. This allows sharing the lattices/input files and makes it easy to deploy the results ([see below](##Publish-Results)).

## Usage

### Run Simulations
You may to use this variable to use the right mpl backend

```
export MPLBACKEND=SVG
```

Run all simulations and store results in the `RESULTS_DIR` directory:

```
poetry run doit
```

or for indiviual lattices

```
poetry run doit elegant_summary:bessy2/bessy2_design-1996_v_1
```

### View Results

The simulation results can be displayed using the [lattice-summaries-website](https://github.com/nobeam/lattice-summaries-website).

## Publish Results

Just deploy the `RESULTS_DIR` directory to any static website hosting like [Github Pages](https://pages.github.com/) and make sure the [lattice-summaries-website](https://github.com/nobeam/lattice-summaries-website) points to the correct URL.


## License

[GNU General Public License v3.0](https://github.com/nobeam/lattice-summaries/blob/main/LICENSE)
