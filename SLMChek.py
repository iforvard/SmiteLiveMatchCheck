import os
import pickle
import PySimpleGUI as P_sg
from HiRezAPI import Smite


def version_project():
    return 'Smite Live Match Check: beta 0.4.2'


DevId = None
AuthKey = None
smite_api = Smite(DevId, AuthKey)
P_sg.ChangeLookAndFeel('Dark')

# Open Profile_list
if os.path.isfile('data/data.pickle'):
    with open('data/data.pickle', 'rb') as f:
        list_id = pickle.load(f)
else:
    list_id = [[0, 'Profile:', 'iforvard', '9236315']]
text_line_1 = version_project()
text_line_2 = 'You need to select the player ID in the settings.'
smite_player_id = None

main_screen = [
    [P_sg.T(text_line_1, key='line1', size=(100, 1), auto_size_text=False),
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

settings_screen = [[P_sg.Text('Settings:')],
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

win1_main = P_sg.Window('',
                        alpha_channel=0.8,
                        no_titlebar=True,
                        grab_anywhere=True,
                        keep_on_top=True,
                        location=(None, None),
                        element_padding=(3, 0),
                        margins=(2, 0),
                        border_depth=-False,
                        use_default_focus=False).Layout(main_screen)

win3_hide = P_sg.Window('Check',
                        right_click_menu=['&Right', ['BACK']],
                        alpha_channel=0.4,
                        no_titlebar=True,
                        grab_anywhere=True,
                        keep_on_top=True,
                        location=(0, 0)).Layout(hide_screen)
win3_hide.Finalize()
win3_hide.Hide()

win2_setting = P_sg.Window('Check_SLM',
                           no_titlebar=True,
                           alpha_channel=0.9,
                           grab_anywhere=True,
                           keep_on_top=True).Layout(settings_screen)

win2_setting.Finalize()
win2_setting.Hide()

# if you have operations on elements that must take place before the event loop, do them here

while True:  # Event Loop App
    event, values = win1_main.Read()
    if event is None or event == 'Exit':
        break

    if event == 'CheckMatch':
        if smite_player_id:
            status = smite_api.get_player_status(player_id=smite_player_id)[0]['status_string']
            if status == 'In Game':
                match_id = smite_api.get_player_status(smite_player_id)[0]['Match']
                match_id = smite_api.get_match_player_details(match_id)
                team1 = ''
                team2 = ''
                for statistic in match_id:
                    data = f"{statistic['GodName']}:{statistic['Account_Level']}({statistic['Mastery_Level']}) "
                    if statistic['taskForce'] == 1:
                        team1 += data
                    else:
                        team2 += data

                text_line_1 = team2
                text_line_2 = team1
                win1_main.FindElement('line1').Update(text_line_1)
                win1_main.FindElement('line2').Update(text_line_2)

            else:
                text_line_1 = version_project()
                win1_main.FindElement('line1').Update(text_line_1)
                text_line_2 = f"Player status must be 'In Game', Your status :{status}"
                win1_main.FindElement('line2').Update(text_line_2)
        else:
            text_line_2 = 'status Player: None, Need to add player ID'
            win1_main.FindElement('line2').Update(text_line_2)

    if event == 'Settings':
        win1_main.Hide()
        win2_setting.UnHide()
        event, values = win2_setting.Read()
        while True:  # Event Loop Settings
            if event == 'Cancel':
                win2_setting.Hide()
                win1_main.UnHide()
                break
            if event == 'Save_Settings':
                number_profile = int(values['COMBO_LIST'].split(',')[0].replace('(', ''))
                smite_player_id = list_id[number_profile][3]
                profile_player_name = list_id[number_profile][2]
                text_line_2 = f'Your ID: {smite_player_id}, Name: {profile_player_name}'
                win1_main.FindElement('line2').Update(text_line_2)
                text_line_1 = version_project()
                win1_main.FindElement('line1').Update(text_line_1)
                win2_setting.Hide()
                win1_main.UnHide()
                break
            if event == 'ADD__ID':
                list_id.append([len(list_id), "Profile:", values['_NAME_'], values['_ID_Name_']])
                win2_setting.FindElement('COMBO_LIST').Update(values=list_id)
                with open('data/data.pickle', 'wb') as f:  # Save Profile_list
                    pickle.dump(list_id, f)
            if event == 'DEL__ID':
                if len(list_id) == 1:
                    pass
                else:
                    number_profile = int(values['COMBO_LIST'].split(',')[0].replace('(', ''))
                    del list_id[number_profile]
                    for index, profile in enumerate(list_id):
                        profile[0] = index
                    win2_setting.FindElement('COMBO_LIST').Update(values=list_id)
                    with open('data/data.pickle', 'wb') as f:  # Save Profile_list
                        pickle.dump(list_id, f)
            event, values = win2_setting.Read()

    if event == 'hide':
        win1_main.Hide()
        win3_hide.UnHide()
        event, values = win3_hide.Read()
        while True:  # Event Loop hide
            if event == 'BACK':
                win3_hide.Hide()
                win1_main.UnHide()
                break
