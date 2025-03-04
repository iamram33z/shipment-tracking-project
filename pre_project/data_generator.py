# Install required libraries
import json
import random
import uuid
from datetime import datetime, timedelta


# Define data structures
CITIES = ["København", "Oslo", "Berlin", "Paris", "London", "Colombo", "Bangkok", "Tokyo", "Seoul", "Sydney", "Melbourne", "Jakarta", "Dhaka", "Mumbai"]
COUNTRIES = ["Denmark", "Norway", "Germany", "France", "UK", "Sri Lanka", "India", "China", "Japan", "South Korea", "Thailand", "Malaysia", "Vietnam", "India"]
VESSELS = ["King of the Seas", "Ocean Explorer", "Sea Guardian", "Wave Rider"]
EVENT_TYPES = ["LOAD", "UNLOAD", "ARRIVAL", "DEPARTURE"]
SEAL_SOURCES = ["CUSTOMS", "CARRIER", "INSPECTION", "QUARANTINE", "RELEASE"]
FACILITY_CODES = ["ADT", "XYZ", "PQR", "QRS"]
STATE_REGIONS = ["N/A", "Region A", "Region B", "Region C"]
NAMES = ["John Doe", "Jane Smith", "Mike Johnson", "Sarah Johnson", "Emily Davis", "Michael Wilson", "Daniel Brown"]

def generate_random_event():
    event_id = str(uuid.uuid4())
    event_time = datetime.utcnow() - timedelta(days=random.randint(1, 365))
    
    return {
        "equipmentEvent": {
            "documentReferences": [{"documentReferenceType": "BL", "documentReferenceValue": str(uuid.uuid4())}],
            "equipmentEventTypeCode": random.choice(EVENT_TYPES),
            "equipmentReference": f"APZU{random.randint(1000000, 9999999)}",
            "eventClassifierCode": random.choice(["ACT", "EST"]),
            "eventCreatedDateTime": event_time.isoformat(),
            "eventDateTime": event_time.isoformat(),
            "eventID": event_id,
            "eventLocation": {
                "address": {
                    "city": random.choice(CITIES),
                    "country": random.choice(COUNTRIES),
                    "floor": f"{random.randint(1, 10)}F",
                    "name": random.choice(NAMES),
                    "postCode": str(random.randint(1000, 9999)),
                    "stateRegion": random.choice(STATE_REGIONS),
                    "street": "Main Street",
                    "streetNumber": str(random.randint(1, 200))
                },
                "facilityCode": random.choice(FACILITY_CODES),
                "facilityCodeListProvider": "SMDG",
                "latitude": str(round(random.uniform(-90, 90), 6)),
                "longitude": str(round(random.uniform(-180, 180), 6)),
                "locationName": "Port Terminal",
                "unlocationCode": "XYZ123"
            },
            "eventType": "EQUIPMENT",
            "seals": [{"sealNumber": str(uuid.uuid4()), "sealSource": random.choice(SEAL_SOURCES), "sealType": "STANDARD"}],
            "transportCall": {
                "carrierServiceCode": "FE1",
                "exportVoyageNumber": str(random.randint(1000, 9999)) + "S",
                "facilityCode": random.choice(FACILITY_CODES),
                "facilityCodeListProvider": "SMDG",
                "facilityTypeCode": "PORT",
                "importVoyageNumber": str(random.randint(1000, 9999)) + "N",
                "modeOfTransport": "SEA",
                "transportCallID": str(uuid.uuid4()),
                "vessel": {
                    "vesselCallSignNumber": "NCVV",
                    "vesselFlag": "DE",
                    "vesselIMONumber": str(random.randint(9000000, 9999999)),
                    "vesselName": random.choice(VESSELS),
                    "vesselOperatorCarrierCode": "MAEU",
                    "vesselOperatorCarrierCodeListProvider": "NMFTA"
                }
            }
        }
    }

def generate_json_file(filename="pre_project/events.json", num_records=1000):
    data = [generate_random_event() for _ in range(num_records)]
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Generated {num_records} records in {filename}")

if __name__ == "__main__":
    generate_json_file()