from enum import Enum, auto
from datetime import datetime
import tinytuya
from dotenv import load_dotenv
import os

class PriseState(Enum):
    UNKNOWN = -1
    OFF = 0
    ON = 1
    DESKTOP_ON = 2

    @property
    def message(self) -> str:
        return {
            PriseState.UNKNOWN: "État inconnu",
            PriseState.OFF: "La prise est éteinte",
            PriseState.ON: "La prise est allumée",
            PriseState.DESKTOP_ON: "Ordinateur allumé.",
        }[self]

class Prise:

    def __init__(self, name: str="Prise ordinateur"):
        load_dotenv()

        self.name: str = name
        self.id = os.getenv("DEVICE_ID")
        self.ip = os.getenv("DEVICE_IP")
        self.key = os.getenv("LOCAL_KEY")
        self.device = tinytuya.OutletDevice(
            self.id,
            self.ip,
            self.key
        )
        self.device.set_version(3.3)

        self.status: PriseState = PriseState.UNKNOWN

        self.updated_at: datetime | None = None
    
    def get_status(self) -> PriseState:
        data = self.device.status()
        print(data)
        if 'dps' not in data:
            raise Exception(data["Error"])
        elif data['dps']['1'] == True:
            if self.status == PriseState.DESKTOP_ON:
                return PriseState.DESKTOP_ON
            return PriseState.ON
        elif data['dps']['1'] == False:
            return PriseState.OFF
        else :
            return PriseState.UNKNOWN
    
    def set_status(self, status: PriseState) -> dict:
        if status == self.get_status():
            return {"status": self.status.value, "message": "No change needed"}
        else:
            if status == PriseState.OFF:
                try:
                    self.device.turn_off()
                except Exception as e:
                    print("Error turning off the device:", e)
                    return {"status": PriseState.UNKNOWN, "message": e}
                self.status = PriseState.OFF

            elif status == PriseState.ON:
                try:
                    self.device.turn_on()
                except Exception as e:
                    print("Error turning on the device:", e)
                    return {"status": PriseState.UNKNOWN, "message": e}
                self.status = PriseState.ON

            elif status == PriseState.DESKTOP_ON:
                self.status = PriseState.DESKTOP_ON

            self.updated_at = datetime.now()

            return {"status": self.status.value, "message": self.status.message}

            