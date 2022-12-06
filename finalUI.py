import PySimpleGUI as sg
import requests
import json


search_column = [
    [
        sg.Text('Enter name of healthcare specialist or patient')
    ],
    [
        sg.InputText(size=(25,1),key='search'),
        sg.Button("search",key='searchBtn')
    ], 
    [
        sg.Multiline(size=(30,10),key="response")
    ]
]


append_column = [
    [
        sg.Text("Sender"),
        sg.InputText(size=(25,1),key='sender')
    ],
    [
        sg.Text("Patient"),
        sg.InputText(size=(25,1),key='patient')
    ],
    [
        sg.Text("HealthInfo")
    ],
    [
        sg.Multiline(size=(25,10),key='info')
    ], 
    [
        sg.Button("Submit", key = 'submitBtn')
    ]
]



layout = [
    [
        sg.Column(search_column),
        sg.VSeperator(),
        sg.Column(append_column),
    ]
]




window = sg.Window("Demo", layout)
while True:
    event, values = window.read()
    if event =='searchBtn':
        s='http://localhost:8080/search'
        value = values['search']
        payload = {"name":value}
        r = requests.post(s, json=payload)
        print(r.text)
        temp = r.text
        temp = temp.replace(",","\n")
        temp = temp.replace("[","")
        temp = temp.replace("]","")
        temp = temp.replace("{","")
        temp = temp.replace("}","\n------------------------------")
        temp = temp.replace('"',"")
        temp = temp.replace(":",": ")
        # for i in r:
        #     print(i)
        window['response'].update(temp)
    if event == 'submitBtn':
        s = 'http://localhost:8080/transactions/new'
        m = 'http://localhost:8080/mine'
        payloadS = {"sender":values['sender'],"patient":values['patient'],"healthInfo":values['info']}
        r = requests.post(s,json=payloadS)
        r = requests.get(m)
    if event == sg.WIN_CLOSED:
        break
window.close()