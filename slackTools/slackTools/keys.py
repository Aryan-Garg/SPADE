import os
import json


'''Load slack keys
- Default storage location is global in home directory
- Secondary storage location is in local directory
'''
def load(filePath='~/.slack/slack.key'):

    # Default storage location is global in home directory
    try:
        print("Retrieving Slack Keys from", filePath)
        with open(filePath, mode="r") as j_object:
            data = json.load(j_object)
    except:
        try:
            filePath = './slackTools/'+os.path.basename(filePath)
            print("Retrieving Slack Keys from", filePath)
            with open(filePath, mode="r") as j_object:
                data = json.load(j_object)
        except:
            filePath = os.path.basename(filePath)
            print("<?> Slack Keys not found. Checking for "+filePath+" in local directory.("+os.getcwd()+")")

            # Secondary storage location is in local directory
            print("Retrieving Slack Keys from", filePath)
            with open(filePath, mode="r") as j_object:
                data = json.load(j_object)

    # Cleanup
    if data['NOTIFY_ON_EVENT'][0] == "":
        data['NOTIFY_ON_EVENT'] = []

    print("Success!")
    # print("Found:", data.keys())
    # print("Found:", data['USERS']['jf'])
    return data