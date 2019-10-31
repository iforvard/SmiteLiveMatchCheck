import PySimpleGUI as P_sg
from HiRezAPI import Smite
import pickle

DevId = None
AuthKey = None
smite_api = Smite(DevId, AuthKey)


def version_project():
    return 'Smite Live Match Check: beta 0.4.1'


P_sg.ChangeLookAndFeel('Dark')

try:
    with open('data/data.pickle', 'rb') as f:  # Open Profile_list
        list_id = pickle.load(f)
except FileNotFoundError:
    list_id = [['1_Profile:', 'iforvard', '9236315']]
text_line_1 = version_project()
text_line_2 = 'Need to add player ID'
tmp_id = '0'
hide_loc = (0, 0)

layout = [
    [P_sg.T(text_line_1, key='ST', size=(100, 1), auto_size_text=False),
     P_sg.Button('', image_filename='data/hide.png', image_size=(30, 30), key='hide', border_width=False,
                 button_color=('gray25', 'gray25')),
     P_sg.Button('', image_filename='data/Exit.png', key='Exit', image_size=(30, 30), border_width=False,
                 button_color=('gray25', 'gray25'))],
    [P_sg.T(text_line_2, key='line2', size=(100, 1), auto_size_text=False),
     P_sg.Button('', key='CheckMatch', image_filename='data/match.png', image_size=(30, 30), border_width=False,
                 button_color=('gray25', 'gray25')),
     P_sg.Button('', key='Settings', image_filename='data/settings.png', image_size=(30, 30), border_width=False,
                 button_color=('gray25', 'gray25'))]]

hide_screen = [[P_sg.Text('', size=(1, 2))]]

Settings_Screen = [[P_sg.Text('Settings:')],
                   [P_sg.InputText('Name_Player', key='_NAME_'), P_sg.Text('Name', size=(5, 1))],
                   [P_sg.InputText('ID_Player', key='_ID_Name_'), P_sg.Text('ID', size=(3, 1))],
                   [P_sg.Button('Add', key='ADD__ID', size=(10, 1)),
                    P_sg.Text('Add profile to the LIST:')],
                   [P_sg.InputOptionMenu(list_id, size=(49, 1), key='COMBO_LIST')],
                   [P_sg.Button('Del Profile', key='DEL__ID', size=(10, 1)),
                    P_sg.Button('Save Profile', key='Save_Settings', button_color=('white', 'green'), size=(10, 1)),
                    P_sg.Button('Cancel', key='Cancel', button_color=('white', 'firebrick3'), size=(10, 1))],
                   [P_sg.T(version_project(), key='About', size=(52, 1),
                           auto_size_text=False)],
                   [P_sg.Text('https://github.com/iforvard')]]
RKM = ['&Right', ['hide', 'CheckAPI', '!&Click', 'CheckMatch', 'E&xit', 'Settings']]

window = P_sg.Window('',
                     alpha_channel=0.8,
                     no_titlebar=True,
                     grab_anywhere=True,
                     keep_on_top=True,
                     location=(None, None),
                     element_padding=(3, 0),
                     margins=(2, 0),
                     border_depth=-False,
                     use_default_focus=False).Layout(layout)

win3_hide = P_sg.Window('Check',
                        right_click_menu=['&Right', ['BACK']],
                        alpha_channel=0.4,
                        no_titlebar=True,
                        grab_anywhere=True,
                        keep_on_top=True,
                        location=hide_loc).Layout(hide_screen)
win3_hide.Finalize()
win3_hide.Hide()

win2_setting = P_sg.Window('Check_SLM',
                           no_titlebar=True,
                           alpha_channel=0.9,
                           grab_anywhere=True,
                           keep_on_top=True).Layout(Settings_Screen)

win2_setting.Finalize()
win2_setting.Hide()

# if you have operations on elements that must take place before the event loop, do them here

while True:  # Event Loop App
    event, values = window.Read()
    if event is None or event == 'Exit':
        break

    if event == 'CheckMatch':
        if tmp_id != '0':
            status = smite_api.get_player_status(player_id=tmp_id)[0]['status_string']
            if status == 'In Game':
                match_id = smite_api.get_player_status(tmp_id)[0]['Match']
                match_id = smite_api.get_match_player_details(match_id)
                team1 = ''
                team2 = ''
                for statistic in match_id:
                    data = f"{statistic['GodName']}:{statistic['Account_Level']}({statistic['Mastery_Level']}); "
                    if statistic['taskForce'] == 1:
                        team1 += data
                    else:
                        team2 += data

                text_line_1 = team2
                text_line_2 = team1
                window.FindElement('ST').Update(text_line_1)
                window.FindElement('line2').Update(text_line_2)

            else:
                text_line_1 = version_project()
                window.FindElement('ST').Update(text_line_1)
                text_line_2 = "Player status must be 'In Game'; " + 'Your status :' + status
                window.FindElement('line2').Update(text_line_2)
        else:
            text_line_2 = 'status Player: None, Need to add player ID'
            window.FindElement('line2').Update(text_line_2)

    if event == 'Settings':
        window.Hide()
        win2_setting.UnHide()
        event, values = win2_setting.Read()
        while True:  # Event Loop Settings
            if event == 'Cancel':
                win2_setting.Hide()
                window.UnHide()
                break
            if event == 'Save_Settings':
                if values['COMBO_LIST'][0] == '(':
                    tmp_id = list_id[int(values['COMBO_LIST'][2:values['COMBO_LIST'].index('_')]) - 1][2]
                    tmp_name = list_id[int(values['COMBO_LIST'][2:values['COMBO_LIST'].index('_')]) - 1][1]
                    text_line_2 = 'Your ID: {}, Name: {}'.format(tmp_id, tmp_name)
                    window.FindElement('line2').Update(text_line_2)
                    text_line_1 = version_project()
                    window.FindElement('ST').Update(text_line_1)
                    win2_setting.Hide()
                    window.UnHide()
                    break
            if event == 'ADD__ID':
                list_id.append([str(len(list_id) + 1) + '_Profile:', values['_NAME_'], values['_ID_Name_']])
                win2_setting.FindElement('COMBO_LIST').Update(values=list_id)
                with open('data/data.pickle', 'wb') as f:  # Save Profile_list
                    pickle.dump(list_id, f)
            if event == 'DEL__ID':
                if len(list_id) == 1:
                    pass
                else:
                    del list_id[int(values['COMBO_LIST'][2:values['COMBO_LIST'].index('_')]) - 1]
                    for i in range(len(list_id)):
                        list_id[i][0] = str(i + 1) + '_Profile:'
                    win2_setting.FindElement('COMBO_LIST').Update(values=list_id)
                    with open('data/data.pickle', 'wb') as f:  # Save Profile_list
                        pickle.dump(list_id, f)
            event, values = win2_setting.Read()

    if event == 'hide':
        window.Hide()
        win3_hide.UnHide()
        event, values = win3_hide.Read()
        while True:  # Event Loop hide
            if event == 'BACK':
                win3_hide.Hide()
                window.UnHide()
                break
