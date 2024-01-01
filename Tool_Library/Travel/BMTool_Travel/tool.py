import re
import json
import requests
from typing import Optional
from bs4 import BeautifulSoup
# from serpapi import GoogleSearch
import serpapi
from datetime import datetime, timedelta
from amadeus import Client


def cName2coords(place_name: str, limit: int = 1, serpapi_key: str = ""):
    url = f"https://serpapi.com/locations.json?q={place_name}&limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        if response.json():
            locations = response.json()
            return locations[0]['gps']
        else:  # if not a city, use google map to find this place
            params = {
                "engine": "google_maps",
                "q": place_name,
                "type": "search",
                "api_key": serpapi_key
            }
            # search = GoogleSearch(params)
            # results = search.get_dict()
            results = serpapi.search(**params)
            coords = results["place_results"]['gps_coordinates']
            return coords["longitude"], coords["latitude"]
    return None


def cName2IATA(city_name: str):
    try:
        url = f"https://www.iata.org/en/publications/directories/code-search/?airport.search={city_name}"
        response = requests.get(url)
        html_content = response.content

        soup = str(BeautifulSoup(html_content, "html.parser"))
        head = soup.find(f"<td>{city_name}</td>")

        string = soup[head:]
        pattern = r"<td>(.*?)</td>"
        matches = re.findall(pattern, string)
        return matches[2]
    except:
        raise ValueError(
            f"The input city {city_name} may not have an IATA registered air-port.")


def lodgingProducts(destination: str, exhibit_maxnum: int = 3,
                    serpapi_key: str = ""):
    try:
        # Convert destination to geographic coordinates
        coords = cName2coords(destination, serpapi_key=serpapi_key)

        # Set parameters for Google search
        params = {
            "engine": "google_maps",
            "q": "hotel",
            "ll": f"@{coords[1]},{coords[0]},15.1z",
            "type": "search",
            "api_key": serpapi_key
        }

        # search = GoogleSearch(params)
        # results = search.get_dict()
        results = serpapi.search(**params)
        local_results = results["local_results"]
        # hotel with website links are preferred
        filtered_results = sorted(
            local_results, key=lambda x: 1 if "website" in x else 0, reverse=True)[:exhibit_maxnum]

        # Return error message if no results match criteria
        if not filtered_results:
            return {"error": "No searching results satisfy user's demand."}

        # Parse and format relevant information for each result
        final_results = []
        for item in filtered_results:
            info = {}
            for metadata in ("title", "website", "address", "description", "gps_coordinates", "open_state", "thumbnail"):
                if metadata in item:
                    info[metadata] = item[metadata]
            final_results.append(info)
        # Return formatted results along with recommendations for next steps
        return json.dumps({"data": final_results})

    except Exception as e:
        return str(e)


def flightProducts(origin: str, destination: str, departureDate: Optional[str] = None,
                   adult_num: int = 1, exhibit_maxnum: int = 3,
                   amadeus_api_key: str = "nKJHiuN1UfIKhKBjykt4SjaV5Os0hK2p",
                   amadeus_api_secret: str = "LZDZrBCf01OA4FQY"):
    amadeus = Client(
        client_id=amadeus_api_key,
        client_secret=amadeus_api_secret,
    )

    # set default date if none or past date is given
    tomorrow = datetime.now() + timedelta(days=1)
    defaultDate = f"{tomorrow.year}-{'0' + str(tomorrow.month) if tomorrow.month < 10 else tomorrow.month}-{'0' + str(tomorrow.day) if tomorrow.day < 10 else tomorrow.day}"
    if not departureDate or departureDate < defaultDate:
        departureDate = defaultDate

    try:
        # Call API to search flight offers
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=cName2IATA(origin),
            destinationLocationCode=cName2IATA(destination),
            departureDate=departureDate,
            adults=adult_num
        )

        # Filter results based on exhibit_maxnum
        filterd_results = response.data[:exhibit_maxnum]

        # If no results found return error message
        if not filterd_results:
            return {"error": "No search results satisfy user's demand."}

        final_results = []
        for item in filterd_results:
            info = {}
            metadata = [
                "itineraries",
                "travelerPricings",
                "lastTicketingDate",
                "numberOfBookableSeats",
                "source"]

            # Only include relevant metadata in info
            for key in metadata:
                if key in item:
                    info[key] = item[key]
            final_results.append(info)
        # Return formatted results along with recommendations for next steps
        return json.dumps({"data": final_results})

    except Exception as e:
        return str(e)


def landscapeProducts(destination: str, exhibit_maxnum: int = 3,
                      serpapi_key: str = ""):
    try:
        # Get the coordinates of the destination using the cName2coords function
        coords = cName2coords(destination, serpapi_key=serpapi_key)

        # Set parameters for the GoogleSearch API call
        params = {
            "engine": "google_maps",
            "q": "tourist attractions",
            "ll": f"@{coords[1]},{coords[0]},15.1z",
            "type": "search",
            "api_key": serpapi_key
        }

        # Call the GoogleSearch API
        # search = GoogleSearch(params)
        # results = search.get_dict()
        results = serpapi.search(**params)
        local_results = results["local_results"]

        # Sort the results by the specified keyword if provided
        sorting_keywords = "reviews"
        if sorting_keywords:
            local_results = sorted(
                local_results, key=lambda x: x[sorting_keywords] if sorting_keywords in x else 0, reverse=True)

        # Filter the results to exhibit_maxnum number of items
        filterd_results = local_results[:exhibit_maxnum]

        # Return an error message if no results are found
        if not filterd_results:
            return {"error": "No searching results satisfy user's demand."}

        # Format the results into a dictionary to be returned to the user
        final_results = []
        for item in filterd_results:
            final_results.append({"spot_name": item["title"]})

            for keywords in ("description", "address", "website", "rating", "thumbnail"):
                if keywords in item:
                    final_results[-1][keywords] = item[keywords]
        # Return the formatted data and some extra information to the user
        return json.dumps({"data": final_results})

    except Exception as e:
        return str(e)


def carProducts(pickup_location: str, exhibit_maxnum: Optional[int] = 3,
                serpapi_key: str = ""):
    try:
        coords = cName2coords(pickup_location)
        # Construct search query params with SERPAPI_KEY
        params = {
            "engine": "google_maps",
            "q": "car rentals",
            "ll": f"@{coords[1]},{coords[0]},15.1z",
            "type": "search",
            "api_key": serpapi_key
        }

        # Search for nearby car rentals on SERPAPI
        # search = GoogleSearch(params)
        # results = search.get_dict()
        results = serpapi.search(**params)
        local_results = results["local_results"]

        # Sort results by rating or reviews keywords if sorting_keywords is specified
        sorting_keywords = "reviews"
        if sorting_keywords:
            local_results = sorted(local_results, key=lambda x: x.get(
                sorting_keywords, 0), reverse=True)

        # Make sure spots with a website appear first
        local_results = sorted(
            local_results, key=lambda x: 'website' in x, reverse=True)

        # Choose the exhibit_maxnum rentals to display
        filtered_results = local_results[:exhibit_maxnum]

        # Return an error if there are no results
        if not filtered_results:
            return {"error": "No results found."}

        # Format the output dictionary with relevant data
        final_results = []
        for item in filtered_results:
            spot = {"spot_name": item["title"]}

            for keyword in ("description", "address", "website", "rating",  "thumbnail"):
                if keyword in item:
                    spot[keyword] = item[keyword]

            final_results.append(spot)

        # Return formatted results along with recommendations for next steps
        return json.dumps({"data": final_results})

    except Exception as e:
        return str(e)


if __name__ == "__main__":
    # print(cName2coords("Beijing"))
    # print(cName2IATA("Beijing"))
    # print(lodgingProducts("Oriental Pearl Tower"))
    # print(flightProducts("Shanghai", "Paris"))
    # print(landscapeProducts("Berlin"))
    print(carProducts("Madrid"))
