import requests


class Gas:
    def __init__(self, deployment_id: str):

        if not isinstance(deployment_id, str):
            raise TypeError("Deployment ID must be a string")

        self._deployment_id = deployment_id

    def get_deployment_id(self) -> str:
        return self._deployment_id

    def get_url(self) -> str:
        return f"https://script.google.com/macros/s/{self._deployment_id}/exec"

    def post(self, params: dict = None, data: dict = None) -> dict:

        # Send a POST request to the Google Apps Script URL
        response = requests.post(self.get_url(), params=params, json=data)

        # Raise an exception if the response is not successful
        response.raise_for_status()

        # return the JSON response
        return response.json()

    def get(self, params: dict = None) -> dict:
        # Send a GET request to the Google Apps Script URL
        response = requests.get(self.get_url(), params=params)

        # Raise an exception if the response is not successful
        response.raise_for_status()

        return response.json()
