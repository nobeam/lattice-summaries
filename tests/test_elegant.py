def test_results(test_lattice, test_output_dir):
    from scripts.twiss_elegant import results

    results(test_lattice, test_output_dir / "elegant")
