import xml.etree.ElementTree as ET
import datetime

class StationXML2StationJSON():

  """
  Class StationXML2StationJSON
  Python class to convert from StationXML to StationJSON
 
  Author: Mathijs Koymans, 2018

  Work in Progress

  """

  NAMESPACE = "{http://www.fdsn.org/xml/station/1}"
  MODULE = None
  SCHEMA_VERSION = "1.0"

  def __init__(self):
    pass

  def convert(self, XMLString):

    """
    public StationXML2StationJSON.convert
    Converts FDSNStationXML (xml.etree.ElementTree.Element) to StationJSON
    """

    XMLDocument = ET.fromstring(XMLString)

    return {
      "schemaVersion": self.SCHEMA_VERSION,
      "module": self.MODULE,
      "source": "StationXML2StationJSON",
      "created": datetime.datetime.now().isoformat(),
      "networks": map(self.extractNetwork, XMLDocument.findall(self.NAMESPACE + "Network"))
    }


  def findElementText(self, element, tag, fn=None):
  
    """
    StationXML2StationJSON.findElementText
    Finds element in tree and sets type
    """

    if element is None:
      return None
  
    # Tag is a list: recursion
    if isinstance(tag, list):
      if len(tag) > 1:
        return self.findElementText(element.find(self.NAMESPACE + tag[0]), tag[1:], fn)
      tag = tag[0]
  
    el = element.find(self.NAMESPACE + tag)
  
    if el is None:
      return None
  
    # Convert to type
    if fn is None:
      return el.text
    else:
      return fn(el.text)
  
  
  def extractComplex(self, zero):
  
    """
    StationXML2StationJSON.extractComplex
    Extracts complex (r, i) element
    """

    return [
      self.findElementText(zero, "Real", float),
      self.findElementText(zero, "Imaginary", float)
    ]
  
  def extractPolesZeros(self, stage):
  
    """
    StationXML2StationJSON.extractPolesZeros
    Extracts poles and zeros response element
    """

    return {
      "type": "paz",
      "inputUnits": self.findElementText(stage, ["InputUnits", "Name"]),
      "outputUnits": self.findElementText(stage, ["OutputUnits", "Name"]),
      "transferFunctionType": self.findElementText(stage, "PzTransferFunctionType"),
      "normalizationFactor": self.findElementText(stage, "NormalizationFactor", float),
      "normalizationFrequency": self.findElementText(stage, "NormalizationFrequency", float),
      "zeros": map(self.extractComplex, stage.findall(self.NAMESPACE + "Zero")),
      "poles": map(self.extractComplex, stage.findall(self.NAMESPACE + "Pole"))
    }
  
  def extractCoefficient(self, x):
  
    """
    StationXML2StationJSON.extractCoefficient
    Returns float representation of an element
    """

    return float(x.text)
    
  
  def extractDecimation(self, decimation):
  
    """
    StationXML2StationJSON.extractDecimation
    Returns decimation element
    """

    if decimation is None:
      return None
  
    return {
      "inputSampleRate": self.findElementText(decimation, "InputSampleRate", float),
      "factor": self.findElementText(decimation, "Factor", float),
      "delay": self.findElementText(decimation, "Delay", float),
      "correction": self.findElementText(decimation, "Correction", float),
    }
  
  def extractFIRStage(self, stage):
  
    """
    StationXML2StationJSON.extractFIRStage
    Returns FIR stage element
    """

    return {
      "type": "fir",
      "inputUnits": self.findElementText(stage, ["InputUnits", "Name"]),
      "outputUnits": self.findElementText(stage, ["OutputUnits", "Name"]),
      "symmetry": self.findElementText(stage, "Symmetry"),
      "firCoefficients": map(self.extractCoefficient, stage.findall(self.NAMESPACE + "NumeratorCoefficient"))
    }
  
  def extractCoefficients(self, stage):

    """
    StationXML2StationJSON.extractCoefficients
    Returns Coefficients stage element
    """
 
    return {
      "type": "coefficients",
      "inputUnits": self.findElementText(stage, ["InputUnits", "Name"]),
      "outputUnits": self.findElementText(stage, ["OutputUnits", "Name"]),
      "transferFunctionType": self.findElementText(stage, "CfTransferFunctionType")
    }
  
  def extractResponseListItem(self, item):
  
    """
    StationXML2StationJSON.extractResponseListItem
    Returns items (f, a, p) of ResponseList stage
    """

    return {
      "frequency": self.findElementText(item, "Frequency", float),
      "amplitude": self.findElementText(item, "Amplitude", float),
      "phase": self.findElementText(item, "Phase", float)
    }
  
  def extractResponseList(self, stage):
  
    """
    StationXML2StationJSON.extractResponseList
    Returns ResponseList stage element
    """

    return {
      "type": "responseList",
      "inputUnits": self.findElementText(stage, ["InputUnits", "Name"]),
      "outputUnits": self.findElementText(stage, ["OutputUnits", "Name"]),
      "items": map(self.extractResponseListItem, stage.findall(self.NAMESPACE + "ResponseListElement"))
    }
  
  def extractPolynomial(self, stage):
  
    """
    StationXML2StationJSON.extractPolynomial
    Returns Polynomial stage element
    """

    polynomialDict = {
      "type": "polynomial",
      "inputUnits": self.findElementText(stage, ["InputUnits", "Name"]),
      "outputUnits": self.findElementText(stage, ["OutputUnits", "Name"])
    }
  
    polynomialDict.update(self.extractInstrumentPolynomial(stage))
  
    return polynomialDict
  
  
  def extractStage(self, stage):
  
    """
    StationXML2StationJSON.extractStage
    Returns respons stage for of particular type
    """

    stageDict = {
      "gain": self.findElementText(stage, ["StageGain", "Value"], float),
      "gainFrequency": self.findElementText(stage, ["StageGain", "Frequency"], float)
    }
  
    if stage.find(self.NAMESPACE + "Decimation") is not None:
      stageDict.update({"decimation": self.extractDecimation(stage.find(self.NAMESPACE + "Decimation"))})
  
    if stage.find(self.NAMESPACE + "PolesZeros") is not None:
      stageDict.update(self.extractPolesZeros(stage.find(self.NAMESPACE + "PolesZeros")))
    elif stage.find(self.NAMESPACE + "Coefficients") is not None:
      stageDict.update(self.extractCoefficients(stage.find(self.NAMESPACE + "Coefficients")))
    elif stage.find(self.NAMESPACE + "FIR") is not None:
      stageDict.update(self.extractFIRStage(stage.find(self.NAMESPACE + "FIR")))
    elif stage.find(self.NAMESPACE + "ResponseList") is not None:
      stageDict.update(self.extractResponseList(stage.find(self.NAMESPACE + "ResponseList")))
    elif stage.find(self.NAMESPACE + "Polynomial") is not None:
      stageDict.update(extractPolynomial(stage.find(self.NAMESPACE + "Polynomial")))
  
    return stageDict
  
  def extractInstrumentPolynomial(self, polynomial):

    """
    StationXML2StationJSON.extractInstrumentPolynomial
    Returns InstrumentPolynomial response element (not stage)
    """

    return {
      "approximation": self.findElementText(polynomial, "ApproximationType"),
      "approximationLowerBound": self.findElementText(polynomial, "ApproximationLowerBound", float),
      "approximationUpperBound": self.findElementText(polynomial, "ApproximationUpperBound", float),
      "frequencyLowerBound": self.findElementText(polynomial, "FrequencyLowerBound", float),
      "frequencyUpperBound": self.findElementText(polynomial, "FrequencyUpperBound", float),
      "maximumError": self.findElementText(polynomial, "MaximumError", float),
      "coefficients": map(extractCoefficient, polynomial.findall(self.NAMESPACE + "Coefficient"))
    }
  
  def extractChannel(self, channel):
  
    """
    StationXML2StationJSON.extractChannel
    Returns channel element
    """

    response = channel.find(self.NAMESPACE + "Response")
  
    if response is None:
      return
  
    channelDict = {
      "location": channel.attrib.get("locationCode"),
      "code": channel.attrib.get("code"),
      "startTime": channel.attrib.get("startDate"),
      "endTime": channel.attrib.get("endDate"),
      "latitude": self.findElementText(channel, "Latitude", float),
      "longitude": self.findElementText(channel, "Longitude", float),
      "elevation": self.findElementText(channel, "Elevation", float),
      "depth": self.findElementText(channel, "Depth", float),
      "azimuth": self.findElementText(channel, "Azimuth", float),
      "dip": self.findElementText(channel, "Dip", float),
      "sensorDescription": self.findElementText(channel, ["Sensor", "Description"]),
      "sampleRate": self.findElementText(channel, "SampleRate", float),
      "scale": self.findElementText(response, ["InstrumentSensitivity", "Value"], float),
      "scaleUnits": self.findElementText(response, ["InstrumentSensitivity", "InputUnits", "Name"]),
      "scaleFrequency": self.findElementText(response, ["InstrumentSensitivity", "Frequency"], float),
      "restrictedStatus": channel.attrib.get("restrictedStatus")
    }
  
    if len(response.findall(self.NAMESPACE + "Stage")) > 0:
      channelDict.update({"responseStages": map(self.extractStage, response.findall(self.NAMESPACE + "Stage"))})
  
    if response.find(self.NAMESPACE + "InstrumentPolynomial") is not None:
      channelDict.update({"responsePolynomial": self.extractInstrumentPolynomial(response.find(self.NAMESPACE + "InstrumentPolynomial"))})
      
    return channelDict
  
  def extractStation(self, station):
  
    """
    StationXML2StationJSON.extractStation
    Returns station element
    """

    return {
      "latitude": self.findElementText(station, "Latitude", float),
      "longitude": self.findElementText(station, "Longitude", float),
      "elevation": self.findElementText(station, "Elevation", float),
      "startTime": station.attrib.get("startDate"),
      "endTime": station.attrib.get("endDate"),
      "site": self.extractSite(station.find(self.NAMESPACE + "Site")),
      "restrictedStatus": station.attrib.get("restrictedStatus"),
      "code": station.attrib.get("code"),
      "channels": map(self.extractChannel, station.findall(self.NAMESPACE + "Channel"))
    }
  
  def extractSite(self, site):
  
    """
    StationXML2StationJSON.extractSite
    Returns site element
    """

    if site is None:
      return None
  
    return {
      "name": self.findElementText(site, "Name"),
      "country": self.findElementText(site, "Country")
    }
  
  def extractNetwork(self, network):
  
    """
    StationXML2StationJSON.extractNetwork
    Returns network element
    """

    return {
      "code": network.attrib.get("code"),
      "startTime": network.attrib.get("startDate"),
      "endTime": network.attrib.get("endDate"),
      "description": network.find(self.NAMESPACE + "Description").text,
      "restrictedStatus": network.attrib.get("restrictedStatus"),
      "stations": map(self.extractStation, network.findall(self.NAMESPACE + "Station"))
    }

