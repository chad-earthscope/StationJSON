# StationJSON
This is a prototype FDSN StationJSON schema.

The goal is a develop a schema to for exchanging core seismic station metadata using the parlance and patterns of the [FDSN StationXML schema](http://www.fdsn.org/xml/station/) and [FDSN SEED](http://www.fdsn.org/seed_manual/SEEDManual_V2.4.pdf) standards.

The schema has been developed with the following priorities:

1. To provide core seismic station metadata from multiple "levels" in a single, small container.  Content similar to the text data.  Unlike text output, the JSON will always include higher level information, e.g. station level includes network level details.
2. To provide a flavor of seismic station metadata for applications that would prefer JSON.

## Next steps

Following a period of feedback and integration of changes, the schema will be submitted to FDSN Working Group II for consideration to become an FDSN standard.  If approved, the format will be submitted to FDSN Working Group III for addition to the fdsnws-station service definition with well known 'format' identifier(s).

## Schema and validation

The schema language used JSON Schema draft 4: [http://json-schema.org/](http://json-schema.org/).

Online resources for draft 4 schema validation and instance documents include:

[http://jsonschemalint.com/draft4/](http://jsonschemalint.com/draft4/)
and
[http://json-schema-validator.herokuapp.com/](http://json-schema-validator.herokuapp.com/)

