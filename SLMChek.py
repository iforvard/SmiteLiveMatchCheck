import PySimpleGUI as sg
import smite_API
import pickle


def version_project():
    return 'Smite Live Match Check: beta_0.4'


sg.ChangeLookAndFeel('Dark')

try:
    with open('data/data.pickle', 'rb') as f:  # Open Profile_list
        List_DI = pickle.load(f)
except FileNotFoundError:
    List_DI = [['1_Profile:', 'iforvard', '9236315']]
stat = version_project()
id_player = 'Need to add player ID'
tmp_id = '0'
hide_loc = (0, 0)

layout = [
    [sg.T(stat, key='ST', size=(100, 1), auto_size_text=False),
     sg.Button('', image_filename='data/hide.png', image_size=(30, 30), key='hide', border_width=False,
               button_color=('gray25', 'gray25')),
     sg.Button('', image_filename='data/Exit.png', key='Exit', image_size=(30, 30), border_width=False,
               button_color=('gray25', 'gray25'))],
    [sg.T(id_player, key='line2', size=(100, 1), auto_size_text=False),
     sg.Button('', key='CheckMatch', image_filename='data/match.png', image_size=(30, 30), border_width=False,
               button_color=('gray25', 'gray25')),
     sg.Button('', key='Settings', image_filename='data/settings.png', image_size=(30, 30), border_width=False,
               button_color=('gray25', 'gray25'))]]

hide_screen = [[sg.Text('', size=(1, 2))]]

Settings_Screen = [[sg.Text('Settings:')],
                   [sg.InputText('Name_Player', key='_NAME_'), sg.Text('Name', size=(5, 1))],
                   [sg.InputText('ID_Player', key='_ID_Name_'), sg.Text('ID', size=(3, 1))],
                   [sg.Button('Add', key='ADD__ID', size=(10, 1)),
                    sg.Text('Add profile to the LIST:')],
                   [sg.InputOptionMenu(List_DI, size=(49, 1), key='COMBO_LIST')],
                   [sg.Button('Del Profile', key='DEL__ID', size=(10, 1)),
                    sg.Button('Save Profile', key='Save_Settings', button_color=('white', 'green'), size=(10, 1)),
                    sg.Button('Cancel', key='Cancel', button_color=('white', 'firebrick3'), size=(10, 1))],
                   [sg.T(version_project(), key='About', size=(52, 1),
                         auto_size_text=False)],
                   [sg.Text('https://github.com/iforvard')]]
RKM = ['&Right', ['hide', 'CheckAPI', '!&Click', 'CheckMatch', 'E&xit', 'Settings']]

window = sg.Window('',
                   alpha_channel=0.8,
                   no_titlebar=True,
                   grab_anywhere=True,
                   keep_on_top=True,
                   location=(None, None),
                   element_padding=(3, 0),
                   margins=(2, 0),
                   border_depth=-False,
                   use_default_focus=False).Layout(layout)

win3_hide = sg.Window('Check',
                      right_click_menu=['&Right', ['BACK']],
                      alpha_channel=0.4,
                      no_titlebar=True,
                      grab_anywhere=True,
                      keep_on_top=True,
                      location=hide_loc).Layout(hide_screen)
win3_hide.Finalize()
win3_hide.Hide()

win2_setting = sg.Window('Check_SLM',
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

    if event == 'CheckAPI':
        stat = 'status API: ' + smite_API.status_api()
        window.FindElement('ST').Update(stat)

    if event == 'CheckMatch':
        if tmp_id != '0':
            st = smite_API.get_player_status(tmp_id)[0]['status_string']
            if st == 'In Game':
                match_idm = smite_API.get_player_status(tmp_id)[0]['Match']
                match_idm = smite_API.get_match_player_details(str(match_idm))
                t2 = ''
                t1 = ''
                for i in range(len(match_idm)):
                    if match_idm[i]['taskForce'] == 1:
                        t1 += match_idm[i]['GodName'] + ': ' + str(match_idm[i]['Account_Level']) + '(' + str(
                            match_idm[i]['Mastery_Level']) + '); '
                    else:
                        t2 += match_idm[i]['GodName'] + ': ' + str(match_idm[i]['Account_Level']) + '(' + str(
                            match_idm[i]['Mastery_Level']) + '); '

                stat = t1
                id_player = t2
                window.FindElement('ST').Update(stat)
                window.FindElement('line2').Update(id_player)

            else:
                stat = version_project()
                window.FindElement('ST').Update(stat)
                id_player = "Player status must be 'In Game'; " + 'Your status :' + st
                window.FindElement('line2').Update(id_player)
        else:
            id_player = 'status Player: None, Need to add player ID'
            window.FindElement('line2').Update(id_player)

    if event == 'Settings':
        window.Hide()
        win2_setting.UnHide()
        # win2_setting = sg.Window('Check_SLM' ,
        #                          no_titlebar=True ,
        #                          alpha_channel=0.9 ,
        #                          grab_anywhere=True ,
        #                          keep_on_top=True).Layout(Settings_Screen).Finalize()

        event, values = win2_setting.Read()
        while True:  # Event Loop Settings
            if event == 'Cancel':
                win2_setting.Hide()
                window.UnHide()
                break
            if event == 'Save_Settings':
                if values['COMBO_LIST'][0] == '(':
                    tmp_id = List_DI[int(values['COMBO_LIST'][2:values['COMBO_LIST'].index('_')]) - 1][2]
                    tmp_name = List_DI[int(values['COMBO_LIST'][2:values['COMBO_LIST'].index('_')]) - 1][1]
                    id_player = 'Your ID: {}, Name: {}'.format(tmp_id, tmp_name)
                    window.FindElement('line2').Update(id_player)
                    stat = version_project()
                    window.FindElement('ST').Update(stat)
                    win2_setting.Hide()
                    window.UnHide()
                    break
                # else:
                #     tmp_id = List_DI[int(values['COMBO_LIST'][0:values['COMBO_LIST'].index('_')]) - 1][2]
                #     tmp_name = List_DI[int(values['COMBO_LIST'][2:values['COMBO_LIST'].index('_')]) - 1][1]
                #     id_player = 'Your ID: {}, Name: {}'.format(tmp_id, tmp_name)
                #     window.FindElement('line2').Update(id_player)
                #     stat = version_project()
                #     window.FindElement('ST').Update(stat)
                #     win2_setting.Hide()
                #     window.UnHide()
                #     break
            if event == 'ADD__ID':
                List_DI.append([str(len(List_DI) + 1) + '_Profile:', values['_NAME_'], values['_ID_Name_']])
                win2_setting.FindElement('COMBO_LIST').Update(values=(List_DI))
                with open('data/data.pickle', 'wb') as f:  # Save Profile_list
                    pickle.dump(List_DI, f)
            if event == 'DEL__ID':
                if len(List_DI) == 1:
                    pass
                else:
                    del List_DI[int(values['COMBO_LIST'][2:values['COMBO_LIST'].index('_')]) - 1]
                    for i in range(len(List_DI)):
                        List_DI[i][0] = str(i + 1) + '_Profile:'
                    win2_setting.FindElement('COMBO_LIST').Update(values=(List_DI))
                    with open('data/data.pickle', 'wb') as f:  # Save Profile_list
                        pickle.dump(List_DI, f)
            event, values = win2_setting.Read()

    if event == 'hide':
        # win_loc = window.CurrentLocation()
        window.Hide()
        win3_hide.UnHide()
        # win3_hide = sg.Window('Check' ,
        #                       right_click_menu=['&Right' , ['BACK']] ,
        #                       alpha_channel=0.4 ,
        #                       no_titlebar=True ,
        #                       grab_anywhere=True ,
        #                       keep_on_top=True ,
        #                       location=hide_loc).Layout(hide_screen)

        event, values = win3_hide.Read()
        while True:  # Event Loop hide
            if event == 'BACK':
                # window = sg.Window('' ,
                #    alpha_channel=0.8 ,
                #    no_titlebar=True ,
                #    grab_anywhere=True ,
                #    keep_on_top=True ,
                #    location=(win_loc) ,
                #    element_padding=(3,0) ,
                #    margins=(2 , 0) ,
                #     border_depth=-False,
                #    use_default_focus=False).Layout(layout)
                # hide_loc = win3_hide.CurrentLocation()
                # win3_hide.Close()
                win3_hide.Hide()
                window.UnHide()
                break
