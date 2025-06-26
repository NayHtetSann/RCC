import requests
import json
import base64


class Spreadsheet:

    def get_token(baseUrl, params):
        url = f"{baseUrl}/v1/api/token"
        payload = json.dumps({
            "jsonrpc": "2.0",
            "params": params,
        })
        headers = {
            'Content-Type': 'application/json',
        }

        try:
            response = requests.request("GET", url, headers=headers, data=payload)
            response_data = json.loads(response.text)
            return response_data['result']
        except Exception as e:
            print("Error:", e)

    def new_spreadsheet(baseUrl, filename, datas, token):
        url = f"{baseUrl}/v1/api/call/method"

        payload = json.dumps({
            "jsonrpc": "2.0",
            "params": {
                "model": "spreadsheet.spreadsheet",
                "method": "new_spreadsheet",
                "args": [
                    [],
                    {
                        "filename": filename,
                        "datas": datas.decode('utf-8')
                    }
                ]
            }
        })
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json',
        }
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            response_data = json.loads(response.text)
            print(response_data)
            return response_data['result']
        except Exception as e:
            print("Error:", e)
