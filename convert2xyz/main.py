# from io import StringIO
# from functools import reduce

# from rich import print
# from rich.traceback import install as rich_traceback_install
# rich_traceback_install()

import PySimpleGUI as sg

from params import atoms_dict
from window import layout, make_dpi_aware, ELEMENTS_COUNT

import traceback


def parse_lammps_dump(src:str, atoms_dict:dict, units_A:bool = False) -> dict:

    lines = list(
        filter(bool,
            map(
                str.strip, src.split('ITEM:')
            )
        )
    )

    print(lines)

    def parse_atoms_line(s:str, atoms_dict:dict, units_A:bool = units_A) -> dict:
        s = s.strip().replace(',', '.').replace('\t', ' ')
        s = ' '.join(filter(bool, s.split(' ')))
        parts = s.split(' ')
        print(parts)
        d = dict()
        d['id'] = int(parts[0])
        d['type'] = int(parts[1])
        d['elem'] = atoms_dict.get(d['type'], 'XX')
        d['x'] = float(parts[2])
        d['y'] = float(parts[3])
        d['z'] = float(parts[4])

        if units_A:
            d['x'] /= 10.
            d['y'] /= 10.
            d['z'] /= 10.
        return d

    data = dict()
    for line in lines:
        if line.startswith('NUMBER OF ATOMS'):
            data['noa'] = int(line.split('\n')[-1])

        if line.startswith('TIMESTEP'):
            data['timestep'] = int(line.split('\n')[-1])

        if line.startswith('ATOMS'):
            coords = list()
            parts = list(filter(bool, line.split('\n')))
            for p in parts[1:]:
                coords.append(parse_atoms_line(p, atoms_dict))

            coords = sorted(coords, key=lambda x:x['id'])
            data['atoms'] = coords

    return data


def dict2xyz(data:dict) -> str:
    coords = '\n'.join('{elem} {x:.6g} {y:.6g} {z:.6g}'.format(**d) for d in data['atoms'])
    comment = ''
    # xyz_header = '{noa}\n'.format(**data)
    xyz_header = '{0}\n'.format(len(data['atoms']))
    return xyz_header + f'{comment}\n' + coords


# def view_with_ase(data):
#     from ase import Atom, Atoms
#     from ase.visualize import view as ase_view

#     atoms = []
#     for atom in data['atoms']:
#         a = Atom(atom['elem'], position=(atom['x'], atom['y'], atom['z']))
#         print(a)
#         atoms.append(a)
#     atoms = Atoms(atoms)
#     ase_view(atoms)


def view_as_graph(xyz):
    from xyz2graph import MolGraph, to_plotly_figure
    from plotly.offline import offline

    mg = MolGraph()
    mg.read_xyz_from_str(xyz)
    fig = to_plotly_figure(mg)
    offline.plot(fig)


def main():
    make_dpi_aware()
    window = sg.Window('C2XYZ', layout, resizable=True, finalize=True)
    window.bind("<Escape>", "_esc")
    app_working = True

    app = dict()
    app['atoms_dict'] = atoms_dict


    try:
        while app_working:
            event, values = window.read()
            print(values)
            if event in (sg.WINDOW_CLOSED, '_esc'):
                app_working = False
                break

            if event == 'load_lammps':
                lammps_file = values['load_lammps']
                lammps = open(lammps_file).read().strip()
                window['lammps'].update(lammps)

                try:
                    app['data'] = parse_lammps_dump(lammps, app['atoms_dict'], values['units_A'])
                    types = set(x['type'] for x in app['data']['atoms'])

                    for t in types:
                        window[('num', t)].update(visible=True)
                        window[('elem', t)].update(visible=True)
                except:
                    pass


            if event == 'update_symbols':
                lammps = values['lammps']
                if not bool(lammps):
                    window['xyz'].update('Malformed input!')

                else:
                    app['data'] = parse_lammps_dump(lammps, atoms_dict, values['units_A'])
                    types = set(x['type'] for x in app['data']['atoms'])

                    for t in types:
                        window[('num', t)].update(visible=True)
                        window[('elem', t)].update(visible=True)

                    app['atoms_dict'] = dict((i+1, values[('elem', i+1)]) for i in range(ELEMENTS_COUNT))


            if event == 'convert':
                lammps = values['lammps']
                try:
                    app['data'] = parse_lammps_dump(lammps, app['atoms_dict'], values['units_A'])
                    app['xyz'] = dict2xyz(app['data'])
                    window['xyz'].update(app['xyz'])
                except:
                    window['xyz'].update('Malformed input data!')
                    sg.popup_error_with_traceback(f'An error happened.  Here is the info:', traceback.format_exc())


            if event == 'export_xyz':
                xyz_file = values['export_xyz']
                with open(xyz_file, 'w') as f:
                    f.write(app['xyz'])

            # if event == 'view_ase':
            #     lammps = values['lammps']
            #     app['data'] = parse_lammps_dump(lammps, app['atoms_dict'], values['units_A'])

            #     try:
            #         view_with_ase(app['data'])
            #     except ImportError:
            #         window['xyz'].update('ASE not included:( Use VESTA!')

            if event == 'view_graph':
                try:
                    view_as_graph(values['xyz'])
                except ImportError:
                    window['xyz'].update('Error occurred:( Use VESTA with xyz file!')


    except Exception as e:
        sg.popup_error_with_traceback(f'An error happened.  Here is the info:', traceback.format_exc())


    window.close()



if __name__ == '__main__':
    main()
