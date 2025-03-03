-- Create Dimension Table: Address
CREATE TABLE IF NOT EXISTS Logistics.Address (
    addressID STRING, -- SHA-256 truncated 16-character ID, intended primary key
    stateRegion STRING, -- State or region
    streetNumber STRING, -- Street number
    street STRING, -- Street name
    country STRING, -- Country
    floor STRING, -- Floor number
    city STRING, -- City name
    postCode STRING, -- Postal code
    name STRING
);

-- Create Dimension Table: Facility
CREATE TABLE IF NOT EXISTS Logistics.Facility (
    facilityID STRING, -- SHA-256 truncated 16-character ID, intended primary key
    facilityCodeListProvider STRING, -- Provider of facility codes
    facilityCode STRING, -- Facility code
    facilityTypeCode STRING
);

-- Create Dimension Table: Vessel
CREATE TABLE IF NOT EXISTS Logistics.Vessel (
    vesselID STRING, -- SHA-256 truncated 16-character ID, intended primary key
    vesselCallSignNumber STRING, -- Vessel call sign number
    vesselFlag STRING, -- Country flag of the vessel
    vesselIMONumber STRING, -- IMO number
    vesselName STRING, -- Name of the vessel
    vesselOperatorCarrierCode STRING, -- Carrier code
    vesselOperatorCarrierCodeListProvider STRING
);

-- Create Dimension Table: TransportCall
CREATE TABLE IF NOT EXISTS Logistics.TransportCall (
    transportCallID STRING, -- SHA-256 truncated 16-character ID, intended primary key
    carrierServiceCode STRING, -- Carrier service code
    exportVoyageNumber STRING, -- Export voyage number
    importVoyageNumber STRING, -- Import voyage number
    modeOfTransport STRING, -- Mode of transport (Air, Sea, Road)
    vesselID STRING, -- Intended foreign key to Vessel
    facilityID STRING -- Intended foreign key to Facility
);

-- Create Dimension Table: EventLocation
CREATE TABLE IF NOT EXISTS Logistics.EventLocation (
    locationID STRING, -- SHA-256 truncated 16-character ID, intended primary key
    latitude FLOAT64, -- Latitude coordinate
    longitude FLOAT64, -- Longitude coordinate
    unlocationCode STRING, -- UN location code
    facilityID STRING, -- Intended foreign key to Facility
    addressID STRING -- Intended foreign key to Address
);

-- Create Dimension Table: DocumentReferences
CREATE TABLE IF NOT EXISTS Logistics.DocumentReferences (
    documentReferenceID STRING, -- SHA-256 truncated 16-character ID, intended primary key
    documentIndex INT64, -- Index number of the document
    documentReferenceType STRING, -- Type of document reference
    documentReferenceValue STRING
);

-- Create Dimension Table: Seals
CREATE TABLE IF NOT EXISTS Logistics.Seals (
    sealID STRING, -- SHA-256 truncated 16-character ID, intended primary key
    sealIndex INT64, -- Index number of the seal
    sealNumber STRING, -- Seal number
    sealSource STRING, -- Source of the seal
    sealType STRING
);

-- Create Fact Table: EquipmentEvent
CREATE TABLE IF NOT EXISTS Logistics.EquipmentEvent (
    eventID STRING, -- SHA-256 truncated 16-character ID, intended primary key
    eventCreatedDateTime TIMESTAMP, -- When the event was created
    eventClassifierCode STRING, -- Classifier code for the event
    equipmentEventTypeCode STRING, -- Equipment event type code
    equipmentReference STRING, -- Reference to equipment
    eventDateTime TIMESTAMP, -- Actual event time
    eventType STRING, -- Event type description
    transportCallID STRING, -- Intended foreign key to TransportCall
    locationID STRING, -- Intended foreign key to EventLocation
    sealID STRING, -- Intended foreign key to Seals
    documentReferenceID STRING -- Intended foreign key to DocumentReferences
);