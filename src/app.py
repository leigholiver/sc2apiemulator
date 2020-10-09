import sys, json, redis
from flask import Flask, Response, request

app = Flask(__name__)
conn = redis.Redis('localhost')

@app.route('/ui')
def ui():
    data = getData()
    if data['state'] == "nogame" or data['state'] == "postgame":
        activeScreens = [
            'ScreenBackgroundSC2/ScreenBackgroundSC2',
            data['menu_state'],
            'ScreenNavigationSC2/ScreenNavigationSC2',
            'ScreenForegroundSC2/ScreenForegroundSC2'
        ]

        if data['additional_menu_state'] != "None":
            activeScreens.append(data['additional_menu_state'])

        return respond({ 'activeScreens': activeScreens })

    if data['state'] == 'loading':
        return respond({'activeScreens': ['ScreenLoading/ScreenLoading']})

    if data['state'] == 'ingame':
        return respond({'activeScreens': []})

    return 400

@app.route('/game')
def game():
    data = getData()
    state = getState()

    if state['players'] == []:
        state['players'] = getPlayersFromData(data)
        conn.set("state", json.dumps(state))

    if data['state'] == "nogame" or data['state'] == "postgame":
        state['inGame'] = 0
        conn.set("state", json.dumps(state))

    if data['state'] == "nogame":
        return respond({'isReplay': False, 'displayTime': 0.0, 'players': []})

    state['replay'] = data['replay'] == "true"
    if data['state'] == "ingame" and state['inGame'] == 0:
        state['inGame'] = 1
        state['players'] = getPlayersFromData(data)
        conn.set("state", json.dumps(state))

    tmpPlayers = []
    for i in range(0,len(state['players'])):
        p = state['players'][i].copy()
        if data['state'] == "ingame" and data['replay'] == "false":
            p['result'] = "Undecided"
        else:
            p['result'] = data['result'+str(p['id'])]
        p['id'] = i + 1
        tmpPlayers.append(p)

    return respond({
        'isReplay': state['replay'],
        'displayTime': 0.0,
        'players': tmpPlayers
    })

@app.route('/set', methods = ['POST'])
def set():
    conn.set("data", json.dumps(request.form.to_dict()))
    return "", 200

def getPlayersFromData(data):
    players = []
    for i in range(1,9):
        if data['enabled'+str(i)] == "true":
            players.append({
                'id': i,
                'name': data['name'+str(i)],
                'type': 'user',
                'race': data['race'+str(i)],
                'result': data['result'+str(i)]
            })
    return players

def respond(data):
    return Response(response=json.dumps(data),
                    status=200,
                    mimetype="application/json")

def getState():
    state = conn.get("state")
    if not state:
        return {'players': [], 'replay': "false"}
    return json.loads(state)

def getData():
    data = conn.get("data")
    if not data:
        return {
            "state": "nogame",
            "menu_state": "ScreenHome/ScreenHome",
            "additional_menu_state": "None",
            "replay": "false",
            "enabled1": "true",
            "name1": "player1",
            "race1": "Terr",
            "result1": "Defeat",
            "enabled2": "true",
            "name2": "player2",
            "race2": "Terr",
            "result2": "Defeat",
            "enabled3": "false",
            "name3": "player3",
            "race3": "Terr",
            "result3": "Defeat",
            "enabled4": "false",
            "name4": "player4",
            "race4": "Terr",
            "result4": "Defeat",
            "enabled5": "false",
            "name5": "player5",
            "race5": "Terr",
            "result5": "Defeat",
            "enabled6": "false",
            "name6": "player6",
            "race6": "Terr",
            "result6": "Defeat",
            "enabled7": "false",
            "name7": "player7",
            "race7": "Terr",
            "result7": "Defeat",
            "enabled8": "false",
            "name8": "player8",
            "race8": "Terr",
            "result8": "Defeat"
        }
    return json.loads(data)

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')
