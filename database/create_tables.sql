-- Create Fact Table: EquipmentEvent
CREATE TABLE IF NOT EXISTS logistic_datawarehouse.EquipmentEvent (
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
    documentReferenceID CHAR(16) -- Foreign key to DocumentReferences
);

-- Create Dimension Table: DocumentReferences
CREATE TABLE IF NOT EXISTS logistic_datawarehouse.DocumentReferences (
    documentReferenceID CHAR(16) PRIMARY KEY, -- SHA-256 truncated 16-character ID, primary key
    documentIndex INT, -- Index number of the document
    documentReferenceType VARCHAR(100), -- Type of document reference
    documentReferenceValue VARCHAR(255) -- Reference value
);

-- Create Dimension Table: EventLocation
CREATE TABLE IF NOT EXISTS logistic_datawarehouse.EventLocation (
    locationID CHAR(16) PRIMARY KEY, -- SHA-256 truncated 16-character ID, primary key
    latitude DECIMAL(10, 7), -- Latitude coordinate
    longitude DECIMAL(10, 7), -- Longitude coordinate
    unlocationCode VARCHAR(20), -- UN location code
    facilityID CHAR(16), -- Foreign key to Facility
    addressID CHAR(16) -- Foreign key to Address
);

-- Create Dimension Table: Address
CREATE TABLE IF NOT EXISTS logistic_datawarehouse.Address (
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
CREATE TABLE IF NOT EXISTS logistic_datawarehouse.Facility (
    facilityID CHAR(16) PRIMARY KEY, -- SHA-256 truncated 16-character ID, primary key
    facilityCodeListProvider VARCHAR(100), -- Provider of facility codes
    facilityCode VARCHAR(50), -- Facility code
    facilityTypeCode VARCHAR(50) -- Type of facility
);

-- Create Dimension Table: TransportCall
CREATE TABLE IF NOT EXISTS logistic_datawarehouse.TransportCall (
    transportCallID CHAR(16) PRIMARY KEY, -- SHA-256 truncated 16-character ID, primary key
    carrierServiceCode VARCHAR(50), -- Carrier service code
    exportVoyageNumber INT, -- Export voyage number
    importVoyageNumber INT, -- Import voyage number
    modeOfTransport VARCHAR(50), -- Mode of transport (Air, Sea, Road)
    vesselID CHAR(16), -- Foreign key to Vessel
    facilityID CHAR(16) -- Foreign key to Facility
);

-- Create Dimension Table: Vessel
CREATE TABLE IF NOT EXISTS logistic_datawarehouse.Vessel (
    vesselID CHAR(16) PRIMARY KEY, -- SHA-256 truncated 16-character ID, primary key
    vesselCallSignNumber VARCHAR(50), -- Vessel call sign number
    vesselFlag VARCHAR(50), -- Country flag of the vessel
    vesselIMONumber VARCHAR(50), -- IMO number
    vesselName VARCHAR(255), -- Name of the vessel
    vesselOperatorCarrierCode VARCHAR(50), -- Carrier code
    vesselOperatorCarrierCodeListProvider VARCHAR(50) -- Provider of the carrier code
);

-- Create Dimension Table: Seals
CREATE TABLE IF NOT EXISTS logistic_datawarehouse.Seals (
    sealID CHAR(16) PRIMARY KEY, -- SHA-256 truncated 16-character ID, primary key
    sealIndex INT, -- Index number of the seal
    sealNumber VARCHAR(100), -- Seal number
    sealSource VARCHAR(100), -- Source of the seal
    sealType VARCHAR(50) -- Type of seal
);

-- Add Foreign Key Constraints to EquipmentEvent
ALTER TABLE logistic_datawarehouse.EquipmentEvent
ADD CONSTRAINT FK_EquipmentEvent_DocumentReferences
FOREIGN KEY (documentReferenceID)
REFERENCES logistic_datawarehouse.DocumentReferences (documentReferenceID);

ALTER TABLE logistic_datawarehouse.EquipmentEvent
ADD CONSTRAINT FK_EquipmentEvent_EventLocation
FOREIGN KEY (locationID)
REFERENCES logistic_datawarehouse.EventLocation (locationID);

ALTER TABLE logistic_datawarehouse.EquipmentEvent
ADD CONSTRAINT FK_EquipmentEvent_Seals
FOREIGN KEY (sealID)
REFERENCES logistic_datawarehouse.Seals (sealID);

ALTER TABLE logistic_datawarehouse.EquipmentEvent
ADD CONSTRAINT FK_EquipmentEvent_TransportCall
FOREIGN KEY (transportCallID)
REFERENCES logistic_datawarehouse.TransportCall (transportCallID);

-- Add Foreign Key Constraints to EventLocation
ALTER TABLE logistic_datawarehouse.EventLocation
ADD CONSTRAINT FK_EventLocation_Facility
FOREIGN KEY (facilityID)
REFERENCES logistic_datawarehouse.Facility (facilityID);

ALTER TABLE logistic_datawarehouse.EventLocation
ADD CONSTRAINT FK_EventLocation_Address
FOREIGN KEY (addressID)
REFERENCES logistic_datawarehouse.Address (addressID);

-- Add Foreign Key Constraints to TransportCall
ALTER TABLE logistic_datawarehouse.TransportCall
ADD CONSTRAINT FK_TransportCall_Vessel
FOREIGN KEY (vesselID)
REFERENCES logistic_datawarehouse.Vessel (vesselID);

ALTER TABLE logistic_datawarehouse.TransportCall
ADD CONSTRAINT FK_TransportCall_Facility
FOREIGN KEY (facilityID)
REFERENCES logistic_datawarehouse.Facility (facilityID);