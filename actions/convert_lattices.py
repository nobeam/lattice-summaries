import latticejson


def action(source, targets):
    lattice_file = latticejson.load(source)
    for target in targets:
        latticejson.save(lattice_file, target)
