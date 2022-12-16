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


layout = [
    [
        sg.Multiline('', size=(50,10), key='lammps'),



        # sg.Input(key='load_lammps', do_not_clear=False, enable_events=True, visible=False),
        # sg.FileBrowse('Open Lammps file', initial_folder=Path('.')),
    ],
    [sg.HorizontalSeparator(),],
    [
        sg.Column(elements_layout),
    ],
    [sg.HorizontalSeparator(),],
    [
        sg.Text('Paste ITEM: ATOMS part from single LAMMPS timestep above'),
    ],
    [
        sg.Button('1. Update symbols', key='update_symbols'),
        sg.Button('2. Convert', key='convert'),
        # sg.Button('View with ASE', key='view_ase')

        sg.Input(key='export_xyz', do_not_clear=False, enable_events=True, visible=False),
        sg.FileSaveAs('3. Save XYZ file', file_types = (('XYZ Files', '*.xyz'),), default_extension="*.xyz", initial_folder=Path('.')),
    ],
    [
        sg.Text('Units: '),
        sg.Radio('nanometers', group_id='units', key='units_nm', default=True),
        sg.Radio('Angstroems', group_id='units', key='units_A'),
    ],
    [sg.HorizontalSeparator(),],
    [
        sg.Multiline('XYZ will be here', size=(50,10), key='xyz'),
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
