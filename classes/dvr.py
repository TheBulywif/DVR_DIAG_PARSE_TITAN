from debug import logger

dlogger.logger.info(f"****CREATING DVR CLASS****")


class Dvr:

    def __init__(self, name, model, firmware, mcu):
        dlogger.logger.info(f"CALLING __init__() CONSTRUCTOR")
        self.name = name
        self.model = model
        self.firmware = firmware
        self.mcu = mcu

    def demographics(self):
        dlogger.logger.info(f"RETURNING DVR DEMOGRAPHCICS")
        dlogger.logger.debug(f"Name = {self.name}"
                             f"Model = {self.model}"
                             f"Firmware = {self.firmware}"
                             f"MCU = {self.mcu}")
        return self.name, self.model, self.firmware, self.mcu


dvr = Dvr()
