def test_results(test_lattice, test_output_dir):
    from scripts.lattice_info import results

    results(test_lattice, test_output_dir / "lattice_info")
