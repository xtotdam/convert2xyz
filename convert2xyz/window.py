from pathlib import Path

import PySimpleGUI as sg
import ctypes
import platform

from params import atoms_dict

def make_dpi_aware() -> None:
    if int(platform.release()) >= 8:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)

sg.theme('TealMono')

ELEMENTS_COUNT = 25
elements_layout = [[
    sg.Text(str(i+1), size=(3,1), key=('num', i+1), visible=False),
    sg.Input(atoms_dict.get(i+1, 'XX'), size=(5,1), key=('elem', i+1), visible=False)
] for i in range(ELEMENTS_COUNT)]


lammps_placeholder = '''\
ITEM: ATOMS id type xs ys zs
1   4   49,01993 54,41678 43,5755
7   3   49,21519 56,14928 46,33995
8   2   49,00395 57,23499 47,96693
9   1   44,51714 57,34797 48,43434
10  1   45,52261 58,4657 49,37007
11  1   44,16624 57,89539 49,15538
4   1   43,72985 59,27789 47,42163
2   2   44,98157 59,63186 45,92418
3   3   44,87193 53,07427 48,31953
5   1   45,88641 52,32251 48,30398
6   1   46,25052 51,25304 49,11811'''
lammps_placeholder = ''


layout = [
    [
        sg.Multiline(lammps_placeholder, size=(70,10), key='lammps'),



        # sg.Input(key='load_lammps', do_not_clear=False, enable_events=True, visible=False),
        # sg.FileBrowse('Open Lammps file', initial_folder=Path('.')),
    ],
    [sg.HorizontalSeparator(),],
    [
        sg.Text('Paste ITEM: ATOMS part from single LAMMPS timestep above'),
    ],
    [
        sg.Button('1. Update symbols', key='update_symbols'),
        sg.Button('2. Convert', key='convert'),
        # sg.Button('View with ASE', key='view_ase'),

        sg.Input(key='export_xyz', do_not_clear=False, enable_events=True, visible=False),
        sg.FileSaveAs('3. Save XYZ file', file_types = (('XYZ Files', '*.xyz'),), default_extension="*.xyz", initial_folder=Path('.')),

        sg.Button('Show as graph', key='view_graph'),
    ],
    [
        sg.Text('Units: '),
        sg.Radio('nanometers', group_id='units', key='units_nm', default=True),
        sg.Radio('Angstroems', group_id='units', key='units_A'),
    ],
    [sg.HorizontalSeparator(),],
    [
        sg.Column(elements_layout),
    ],
    [sg.HorizontalSeparator(),],
    [
        sg.Multiline('XYZ will be here', size=(70,10), key='xyz'),
    ],
    # [sg.HorizontalSeparator(),],
    # [
    #     sg.Text('Footer')
    # ]
]



if __name__ == '__main__':
    print('Hey, dumbass, you built the wrong file')

    make_dpi_aware()
    window = sg.Window('Test', layout, resizable=True, finalize=True, location=(0,0))
    window.bind("<Escape>", "_esc")

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, '_esc'):
            break

    window.close()
