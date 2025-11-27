import asyncio
import random
from typing import Optional
from furhat_realtime_api import AsyncFurhatClient


class HeadMotionController:
    def __init__(self, furhat: AsyncFurhatClient) -> None:
        if AsyncFurhatClient is None:
            raise RuntimeError(
                "furhat_realtime_api must be installed to use HeadMotionController"
            )
        self.furhat = furhat
        self._stop = False

    def stop(self) -> None:
        """Signal all running behaviours to terminate on their next iteration."""
        self._stop = True

    async def enable_microexpressions(
        self, visibility: bool = True, microexpressions: bool = True
    ) -> None:
        await self.furhat.request_face_config(
            "adult - James", visibility, microexpressions
        )

    async def random_glance_away(
        self,
        min_interval: float = 10.0,
        max_interval: float = 15.0,
        yaw_range: float = 15.0,
        pitch_range: float = 5.0,
    ) -> None:
        while not self._stop:
            delay = random.uniform(min_interval, max_interval)
            await asyncio.sleep(delay)
            # Randomly choose direction and magnitude for yaw (left/right) and
            # pitch (up/down).  Roll is kept at zero for glances away.
            yaw = random.choice([-1, 1]) * random.uniform(0, yaw_range)
            pitch = random.choice([-1, 1]) * random.uniform(0, pitch_range)
            await self.furhat.request_face_headpose(
                yaw=yaw,
                pitch=pitch,
                roll=0.0,
                relative=True,
            )
        # Optionally reset the head pose when stopping
        await self.furhat.request_face_headpose(
            yaw=0.0, pitch=0.0, roll=0.0, relative=False
        )

    async def nap_head_movement(
        self,
        min_interval: float = 3.0,
        max_interval: float = 6.0,
        amplitude: float = 5.0,
        duration: float = 2.0,
    ) -> None:
        while not self._stop:
            delay = random.uniform(min_interval, max_interval)
            await asyncio.sleep(delay)
            # Compute random offsets for roll and pitch.  Yaw is kept at zero
            # because the nap movement is mostly nodding and tilting.
            roll_offset = amplitude * random.choice([-1, 1]) * random.uniform(0.5, 1.0)
            pitch_offset = amplitude * random.choice([-1, 1]) * random.uniform(0.5, 1.0)
            await self.furhat.request_face_headpose(
                yaw=0.0,
                pitch=pitch_offset,
                roll=roll_offset,
                relative=True,
            )
            # Hold the position for the given duration
            await asyncio.sleep(duration)
            # Reset the head pose smoothly back to neutral
            await self.furhat.request_face_headpose(
                yaw=0.0, pitch=0.0, roll=0.0, relative=False
            )

    async def blink_or_avert_gaze(
        self,
        min_interval: float = 4.0,
        max_interval: float = 8.0,
    ) -> None:
        gestures = ["Blink", "GazeAversion"]
        while not self._stop:
            await asyncio.sleep(random.uniform(min_interval, max_interval))
            gesture_name = random.choice(gestures)
            await self.furhat.request_gesture_start(name=gesture_name)

    async def attend_cycle(
        self,
        cycle_time: float = 10.0,
        locations: Optional[list] = None,
    ) -> None:
        idx = 0
        while not self._stop:
            if locations:
                x, y, z = locations[idx % len(locations)]
                await self.furhat.request_attend_location(x=x, y=y, z=z)
                idx += 1
            else:
                # If no locations specified, alternate between attending the closest user and nobody
                if idx % 2 == 0:
                    await self.furhat.request_attend_user(user_id="closest")
                else:
                    await self.furhat.request_face_reset()
                idx += 1
            await asyncio.sleep(cycle_time)

        await self.furhat.request_face_reset()

    async def run_concurrent_behaviours(self) -> None:
        await self.enable_microexpressions(visibility=True, microexpressions=True)
        await asyncio.gather(
            self.random_glance_away(),
            self.nap_head_movement(),
            self.blink_or_avert_gaze(),
        )


async def main() -> None:
    host = "127.0.0.1"  # Change to your robot's IP address if needed
    auth_key = None  # Specify an authentication key if your robot requires it

    furhat = AsyncFurhatClient(host, auth_key=auth_key)
    await furhat.connect()
    controller = HeadMotionController(furhat)

    # Run the default behaviours until the program is cancelled
    try:
        await controller.run_concurrent_behaviours()
    except asyncio.CancelledError:
        pass
    finally:
        controller.stop()
        await furhat.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Graceful shutdown on Ctrl+C
        pass
