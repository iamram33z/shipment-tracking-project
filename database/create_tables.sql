-- Create Fact Table: EquipmentEvent
CREATE TABLE IF NOT EXISTS logistic_datawarehouse.EquipmentEvent (
    eventID STRING,
    equipmentEventTypeCode STRING,
    equipmentReference STRING,
    eventClassifierCode STRING,
    eventCreatedDateTime TIMESTAMP,
    eventDateTime TIMESTAMP,
    eventType STRING,
    documentReferenceID STRING,
    eventLocationID STRING,
    sealID STRING,
    transportCallID STRING
);

-- Create Dimension Table: DocumentReferences
CREATE TABLE IF NOT EXISTS logistic_datawarehouse.DocumentReferences (
    documentReferenceID STRING,
    documentReferenceType STRING,
    documentReferenceValue STRING
);

-- Create Dimension Table: EventLocation
CREATE TABLE IF NOT EXISTS logistic_datawarehouse.EventLocation (
    eventLocationID STRING,
    city STRING,
    country STRING,
    floor STRING,
    name STRING,
    postCode STRING,
    stateRegion STRING,
    street STRING,
    streetNumber STRING,
    facilityCode STRING,
    facilityCodeListProvider STRING,
    latitude STRING,
    longitude STRING,
    locationName STRING,
    unlocationCode STRING
);

-- Create Dimension Table: Seals
CREATE TABLE IF NOT EXISTS logistic_datawarehouse.Seals (
    sealID STRING,
    sealNumber STRING,
    sealSource STRING,
    sealType STRING
);

-- Create Dimension Table: TransportCall
CREATE TABLE IF NOT EXISTS logistic_datawarehouse.TransportCall (
    transportCallID STRING,
    carrierServiceCode STRING,
    exportVoyageNumber STRING,
    facilityCode STRING,
    facilityCodeListProvider STRING,
    facilityTypeCode STRING,
    importVoyageNumber STRING,
    modeOfTransport STRING,
    vesselCallSignNumber STRING,
    vesselFlag STRING,
    vesselIMONumber STRING,
    vesselName STRING,
    vesselOperatorCarrierCode STRING,
    vesselOperatorCarrierCodeListProvider STRING
);