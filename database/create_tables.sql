-- Create Fact Table: EquipmentEvent
CREATE TABLE IF NOT EXISTS logistic_datawarehouse.EquipmentEvent (
    eventID STRING, -- SHA-256 truncated 16-character ID
    equipmentEventTypeCode STRING, -- Equipment event type code
    equipmentReference STRING, -- Reference to equipment
    eventClassifierCode STRING, -- Classifier code for the event
    eventCreatedDateTime TIMESTAMP, -- When the event was created
    eventDateTime TIMESTAMP, -- Actual event time
    eventType STRING, -- Event type description
    documentReferenceID STRING, -- Foreign key to documentReferences
    eventLocationID STRING, -- Foreign key to location
    sealID STRING, -- Foreign key to seals
    transportCallID STRING -- Foreign key to transportCall
);

-- Create Dimension Table: DocumentReferences
CREATE TABLE IF NOT EXISTS logistic_datawarehouse.DocumentReferences (
    documentReferenceID STRING, -- SHA-256 truncated 16-character ID
    documentIndex INT, -- Index number of the document
    documentReferenceType STRING, -- Type of document reference
    documentReferenceValue STRING -- Reference value
);

-- Create Dimension Table: EventLocation
CREATE TABLE IF NOT EXISTS logistic_datawarehouse.EventLocation (
    eventLocationID STRING, -- SHA-256 truncated 16-character ID
    latitude DECIMAL(10,7), -- Latitude coordinate
    longitude DECIMAL(10,7), -- Longitude coordinate
    unlocationCode STRING, -- UN location code
    facilityID STRING, -- Foreign key to facility
    addressID STRING -- Foreign key to address
);

-- Create Dimension Table: Address
CREATE TABLE IF NOT EXISTS logistic_datawarehouse.Address (
    addressID STRING, -- SHA-256 truncated 16-character ID
    stateRegion STRING, -- State or region
    streetNumber STRING, -- Street number
    street STRING, -- Street name
    country STRING, -- Country
    floor STRING, -- Floor number
    city STRING, -- City name
    postCode STRING, -- Postal code
    name STRING -- Address name
);

-- Create Dimension Table: Facility
CREATE TABLE IF NOT EXISTS logistic_datawarehouse.Facility (
    facilityID STRING, -- SHA-256 truncated 16-character ID
    facilityCodeListProvider STRING, -- Provider of facility codes
    facilityCode STRING, -- Facility code
    facilityTypeCode STRING -- Type of facility
);

-- Create Dimension Table: TransportCall
CREATE TABLE IF NOT EXISTS logistic_datawarehouse.TransportCall (
    transportCallID STRING, -- SHA-256 truncated 16-character ID
    carrierServiceCode STRING, -- Carrier service code
    exportVoyageNumber INT, -- Export voyage number
    importVoyageNumber INT, -- Import voyage number
    modeOfTransport STRING, -- Mode of transport (Air, Sea, Road)
    vesselID STRING, -- Foreign key to vessel
    facilityID STRING -- Foreign key to facility
);

-- Create Dimension Table: Vessel
CREATE TABLE IF NOT EXISTS logistic_datawarehouse.Vessel (
    vesselID STRING, -- SHA-256 truncated 16-character ID
    vesselCallSignNumber STRING, -- Vessel call sign number
    vesselFlag STRING, -- Country flag of the vessel
    vesselIMONumber STRING, -- IMO number
    vesselName STRING, -- Name of the vessel
    vesselOperatorCarrierCode STRING, -- Carrier code
    vesselOperatorCarrierCodeListProvider STRING -- Provider of the carrier code
);

-- Create Dimension Table: Seals
CREATE TABLE IF NOT EXISTS logistic_datawarehouse.Seals (
    sealID STRING, -- SHA-256 truncated 16-character ID
    sealIndex INT, -- Index number of the seal
    sealNumber STRING, -- Seal number
    sealSource STRING, -- Source of the seal
    sealType STRING -- Type of seal
);