import requests

"""
This module provides a class for interacting with Google Apps Script projects
deployed as web apps. The class provides methods for sending GET and POST
requests to the web app URL.

Dependencies:
    - requests


"""


class Gas:
    """
    A class to interact with Google Apps Script deployments.

    This class provides methods to make GET and POST requests to a specified
    Google Apps Script deployment.

    Attributes:
        _deployment_id (str): The deployment ID of the Google Apps Script.
    """

    def __init__(self, deployment_id: str):
        """
        Initializes the Gas object with a deployment ID.

        Args:
            deployment_id (str): The deployment ID of the Google Apps Script.

        Raises:
            TypeError: If the deployment_id is not a string.
        """

        if not isinstance(deployment_id, str):
            raise TypeError("Deployment ID must be a string")

        self._deployment_id = deployment_id

    def get_deployment_id(self) -> str:
        """
        Returns the deployment ID.

        Returns:
            str: The deployment ID.
        """
        return self._deployment_id

    def get_url(self) -> str:
        """
        Constructs and returns the URL for the Google Apps Script deployment.

        Returns:
            str: The URL to access the Google Apps Script deployment.
        """
        return f"https://script.google.com/macros/s/{self._deployment_id}/exec"

    def post(self, params: dict = None, data: dict = None) -> dict:
        """
        Sends a POST request to the Google Apps Script deployment.

        Args:
            params (dict, optional): URL parameters to be sent with the request.
            data (dict, optional): Data to be sent in the JSON body of the request.

        Returns:
            dict: The JSON response from the Google Apps Script deployment.

        Raises:
            HTTPError: If the request did not succeed.
        """
        # Send a POST request to the Google Apps Script URL
        response = requests.post(self.get_url(), params=params, json=data)

        # Raise an exception if the response is not successful
        response.raise_for_status()

        # return the JSON response
        return response.json()

    def get(self, params: dict = None) -> dict:
        """
        Sends a GET request to the Google Apps Script deployment.

        Args:
            params (dict, optional): URL parameters to be sent with the request.

        Returns:
            dict: The JSON response from the Google Apps Script deployment.

        Raises:
            HTTPError: If the request did not succeed.
        """
        # Send a GET request to the Google Apps Script URL
        response = requests.get(self.get_url(), params=params)

        # Raise an exception if the response is not successful
        response.raise_for_status()

        return response.json()
