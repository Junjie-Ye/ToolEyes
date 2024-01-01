"""Tool for the OpenWeatherMap API."""

from typing import Optional

from pydantic import Field

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.tools.base import BaseTool
from langchain.utilities import OpenWeatherMapAPIWrapper
import os


class OpenWeatherMapQueryRun(BaseTool):
    """Tool that queries the OpenWeatherMap API."""

    api_wrapper: OpenWeatherMapAPIWrapper = Field(
        default_factory=OpenWeatherMapAPIWrapper
    )

    name = "OpenWeatherMap"
    description = (
        "A wrapper around OpenWeatherMap API. "
        "Useful for fetching current weather information for a specified location. "
        "Input should be a location string (e.g. London,GB)."
    )

    def _run(
        self, location: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the OpenWeatherMap tool."""
        return self.api_wrapper.run(location)


def current_weather(location: str, apikey: str = ''):
    os.environ['OPENWEATHERMAP_API_KEY'] = apikey
    tool = OpenWeatherMapQueryRun()
    return (tool._run(location))


if __name__ == "__main__":
    # print(current_weather('上海'))
    print(current_weather('London'))
