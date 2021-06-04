def test_results(test_lattice, test_output_dir):
    from scripts.twiss_apace import action

    action(test_lattice, test_output_dir / "apace")
