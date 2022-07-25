from huedoo.hue_api.routes.device_settings import DeviceSetting
from .switchable import Switchable


class Dimmable(Switchable):
    """
    Turn something on and off with brightness
    """
    @property
    def brightness(self) -> float:
        self.refresh()
        return self.resource.dimming.brightness

    def set_brightness(self, brightness: float, force_on: bool = True, **kwargs):
        """
        Set the brigtness of a light
        """
        if brightness > 100:
            brightness = 100

        if brightness <= 0:
            self.turn_off()
            return

        if force_on:
            # turns on the light and sets the brightness
            self.turn_on(DeviceSetting.BRIGHTNESS(brightness), **kwargs)
            return
        else:
            # sets brightness but doesn't change the light on/off
            self.bridge.set_device(
                resource_type=self.resource.type,
                id=self.resource.id,
                device_settings=[
                    DeviceSetting.BRIGHTNESS(brightness)
                ],
                **kwargs
            )
