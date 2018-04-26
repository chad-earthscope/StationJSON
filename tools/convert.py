import requests
import os
import json
import jsonschema

from StationXML2StationJSON import StationXML2StationJSON

if __name__ == "__main__":

  """
  Example use of convert between
  FDSNStationXML and StationJSON
  """

  URL = "https://www.orfeus-eu.org/fdsnws/station/1/query?net=NL&sta=HGN&cha=BHZ&level=response"

  Convertor = StationXML2StationJSON()

  # Parse & print
  output = Convertor.convert(requests.get(URL).content)

  # Validate against the schema
  schemaPath = os.path.join(os.path.dirname(__file__), "..", "fdsn-station-schema.json");
  with open(schemaPath, "rt") as filehandle:
    schema = json.load(filehandle)
  jsonschema.validate(output, schema)

  print json.dumps(output, indent=4)
