# gestures.py
import asyncio
from furhat_realtime_api import AsyncFurhatClient


class GestureController:
    def __init__(self, furhat: AsyncFurhatClient):
        self.furhat = furhat

    async def hear_speech(self):
        await self.furhat.request_face_params({"EYEBROW_UP": 1.0})

        await asyncio.sleep(2.1)
        await self.furhat.request_face_reset()

    async def listening(self, duration: float = 2.0):
        await self.furhat.request_gesture_start(
            name="BrowRaise",
            intensity=0.8,
            duration=duration,
        )

        await self.furhat.request_gesture_start(
            name="Smile",
            intensity=0.6,
            duration=duration,
        )

    async def normal(self):
        await self.furhat.request_gesture_start(
            name="BrowRaise",
            intensity=0.0,
            duration=0.4,
        )
        await self.furhat.request_gesture_start(
            name="Smile",
            intensity=0.0,
            duration=0.4,
        )

        await asyncio.sleep(0.5)

    async def sleep(self):
        await self.furhat.request_face_params(
            {"EYE_BLINK_LEFT": 1, "EYE_BLINK_RIGHT": 1}
        )

    async def wakeUp(self):
        await self.furhat.request_face_params(
            {"EYE_BLINK_LEFT": 0, "EYE_BLINK_RIGHT": 0}
        )

    async def reset_head(self):
        await self.furhat.request_face_headpose(
            yaw=0.0,
            pitch=0.0,
            roll=0.0,
            relative=False,
        )
        await asyncio.sleep(0.4)
