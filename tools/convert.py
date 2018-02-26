import requests
import json

from StationXML2StationJSON import StationXML2StationJSON

if __name__ == "__main__":

  """
  Example use of convert between
  FDSNStationXML and StationJSON
  """

  URL = "https://www.orfeus-eu.org/fdsnws/station/1/query?net=NL&sta=*&cha=HHN&level=response"

  Convertor = StationXML2StationJSON()

  # Parse & print
  output = Convertor.convert(requests.get(URL).content)

  print json.dumps(output, indent=4)
