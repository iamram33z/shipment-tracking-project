-- Create the schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS LogisticsSchema;

-- Use the schema
SET search_path TO LogisticsSchema;

-- Create Dimension Table: Address
CREATE TABLE IF NOT EXISTS Address (
    addressID CHAR(16) PRIMARY KEY, -- SHA-256 truncated 16-character ID, primary key
    stateRegion VARCHAR(100), -- State or region
    streetNumber VARCHAR(20), -- Street number
    street VARCHAR(255), -- Street name
    country VARCHAR(100), -- Country
    floor VARCHAR(10), -- Floor number
    city VARCHAR(100), -- City name
    postCode VARCHAR(20), -- Postal code
    name VARCHAR(255) -- Address name
);

-- Create Dimension Table: Facility
CREATE TABLE IF NOT EXISTS Facility (
    facilityID CHAR(16) PRIMARY KEY, -- SHA-256 truncated 16-character ID, primary key
    facilityCodeListProvider VARCHAR(100), -- Provider of facility codes
    facilityCode VARCHAR(50), -- Facility code
    facilityTypeCode VARCHAR(50) -- Type of facility
);

-- Create Dimension Table: Vessel
CREATE TABLE IF NOT EXISTS Vessel (
    vesselID CHAR(16) PRIMARY KEY, -- SHA-256 truncated 16-character ID, primary key
    vesselCallSignNumber VARCHAR(50), -- Vessel call sign number
    vesselFlag VARCHAR(50), -- Country flag of the vessel
    vesselIMONumber VARCHAR(50), -- IMO number
    vesselName VARCHAR(255), -- Name of the vessel
    vesselOperatorCarrierCode VARCHAR(50), -- Carrier code
    vesselOperatorCarrierCodeListProvider VARCHAR(50) -- Provider of the carrier code
);

-- Create Dimension Table: TransportCall
CREATE TABLE IF NOT EXISTS TransportCall (
    transportCallID CHAR(16) PRIMARY KEY, -- SHA-256 truncated 16-character ID, primary key
    carrierServiceCode VARCHAR(50), -- Carrier service code
    exportVoyageNumber INT, -- Export voyage number
    importVoyageNumber INT, -- Import voyage number
    modeOfTransport VARCHAR(50), -- Mode of transport (Air, Sea, Road)
    vesselID CHAR(16), -- Foreign key to Vessel
    facilityID CHAR(16), -- Foreign key to Facility
    CONSTRAINT FK_TransportCall_Vessel FOREIGN KEY (vesselID) REFERENCES Vessel(vesselID),
    CONSTRAINT FK_TransportCall_Facility FOREIGN KEY (facilityID) REFERENCES Facility(facilityID)
);

-- Create Dimension Table: EventLocation
CREATE TABLE IF NOT EXISTS EventLocation (
    locationID CHAR(16) PRIMARY KEY, -- SHA-256 truncated 16-character ID, primary key
    latitude DECIMAL(10, 7), -- Latitude coordinate
    longitude DECIMAL(10, 7), -- Longitude coordinate
    unlocationCode VARCHAR(20), -- UN location code
    facilityID CHAR(16), -- Foreign key to Facility
    addressID CHAR(16), -- Foreign key to Address
    CONSTRAINT FK_EventLocation_Facility FOREIGN KEY (facilityID) REFERENCES Facility(facilityID),
    CONSTRAINT FK_EventLocation_Address FOREIGN KEY (addressID) REFERENCES Address(addressID)
);

-- Create Dimension Table: DocumentReferences
CREATE TABLE IF NOT EXISTS DocumentReferences (
    documentReferenceID CHAR(16) PRIMARY KEY, -- SHA-256 truncated 16-character ID, primary key
    documentIndex INT, -- Index number of the document
    documentReferenceType VARCHAR(100), -- Type of document reference
    documentReferenceValue VARCHAR(255) -- Reference value
);

-- Create Dimension Table: Seals
CREATE TABLE IF NOT EXISTS Seals (
    sealID CHAR(16) PRIMARY KEY, -- SHA-256 truncated 16-character ID, primary key
    sealIndex INT, -- Index number of the seal
    sealNumber VARCHAR(100), -- Seal number
    sealSource VARCHAR(100), -- Source of the seal
    sealType VARCHAR(50) -- Type of seal
);

-- Create Fact Table: EquipmentEvent
CREATE TABLE IF NOT EXISTS EquipmentEvent (
    eventID CHAR(16) PRIMARY KEY, -- SHA-256 truncated 16-character ID, primary key
    eventCreatedDateTime TIMESTAMP, -- When the event was created
    eventClassifierCode VARCHAR(50), -- Classifier code for the event
    equipmentEventTypeCode VARCHAR(50), -- Equipment event type code
    equipmentReference VARCHAR(100), -- Reference to equipment
    eventDateTime TIMESTAMP, -- Actual event time
    eventType VARCHAR(100), -- Event type description
    transportCallID CHAR(16), -- Foreign key to TransportCall
    locationID CHAR(16), -- Foreign key to EventLocation
    sealID CHAR(16), -- Foreign key to Seals
    documentReferenceID CHAR(16), -- Foreign key to DocumentReferences
    CONSTRAINT FK_EquipmentEvent_TransportCall FOREIGN KEY (transportCallID) REFERENCES TransportCall(transportCallID),
    CONSTRAINT FK_EquipmentEvent_EventLocation FOREIGN KEY (locationID) REFERENCES EventLocation(locationID),
    CONSTRAINT FK_EquipmentEvent_Seals FOREIGN KEY (sealID) REFERENCES Seals(sealID),
    CONSTRAINT FK_EquipmentEvent_DocumentReferences FOREIGN KEY (documentReferenceID) REFERENCES DocumentReferences(documentReferenceID)
);