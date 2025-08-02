import logging, asyncio, numpy as np, cv2
import livekit.agents as agents
from livekit.agents.llm import ChatMessage, ChatRole
from livekit.agents import Agent, AgentSession, RoomInputOptions, WorkerOptions, cli
from livekit.rtc import TrackKind, VideoStream, DataPacketKind,VideoBufferType
from dotenv import load_dotenv

# 日誌設定
load_dotenv()
logger = logging.getLogger("vision-agent")
logger.setLevel(logging.INFO)

# Terminal log
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

# File log
file_handler = logging.FileHandler("vision-agent.log", encoding="utf-8")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

class VisionAgent(Agent):
    def __init__(self):
        super().__init__(instructions="Vision agent for video analysis.")
        self._stream_task = None
        self._video_stream = None
        self._room = None

    def send_chat_message(self, content: str):
        # message = ChatMessage.create(
        #     role="assistant",  # 或 "user"，視你想怎麼顯示
        #     text=content,
        # )
        # self.update_chat_ctx(message)
        # chat_ctx = self.chat_ctx.copy()
        self.chat_ctx.add_message(role="user", text=content)
        # stream = llm_plugin.chat(chat_ctx=chat_ctx)

    async def on_enter(self):
        logger.info("🚀 Agent has entered the room.")
        self._room = agents.job.get_job_context().room
        # room = agents.job.get_job_context().room
        logger.info(f"🔍 Remote participants: {len(self._room.remote_participants)}")

        # 檢查已存在的 video track
        for p in self._room.remote_participants.values():
            for pub in p.track_publications.values():
                if pub.track and pub.track.kind == TrackKind.KIND_VIDEO:
                    logger.info(f"🎥 Found existing video track from {p.identity}")
                    self._start_stream(pub.track)

        # 訂閱後續新加入的 video track
        @self._room.on("track_subscribed")
        def on_sub(track, pub, participant):
            logger.info(f"📡 Subscribed to new track from {participant.identity} ({track.kind})")
            if track.kind == TrackKind.KIND_VIDEO:
                self._start_stream(track)

    def _start_stream(self, track):
        # 關閉舊的 stream
        if self._video_stream:
            self._video_stream.close()
        if self._stream_task and not self._stream_task.done():
            self._stream_task.cancel()

        self._video_stream = VideoStream(track)

        async def reader():
            logger.info("📽️ Start reading video stream")
            try:
                async for ev in self._video_stream:
                    if ev.frame is None:
                        continue

                    img = None

                    try:
                        # 強制轉成 RGB24 格式（OpenCV 可用）
                        frame = ev.frame.convert(VideoBufferType.RGB24)
                        raw_data = frame.data  # memoryview

                        # 轉成 ndarray（注意 shape）
                        width = frame.width
                        height = frame.height
                        img = np.frombuffer(raw_data, dtype=np.uint8).reshape((height, width, 3))
                    except Exception as e:
                        logger.warning(f"⚠️ Failed to convert frame to ndarray: {e}")
                        continue
                    
                    if img is None:
                        logger.warning("⚠️ Failed to decode image")
                        continue

                    cv2.imwrite("debug_frame.jpg", img)

                    # 模擬辨識
                    plate = "SIM123"
                    logger.info(f"🎯 Detected plate: {plate}")

                    msg = f"🎯 Detected plate: {plate}"
                    try:
                        # await self.room.local_participant.publish_data(
                        #     msg.encode("utf-8"),
                        #     kind=DataPacketKind.KIND_RELIABLE,
                        # )
                        self.send_chat_message(f"🎯 Detected plate: {plate}")
                    except Exception as e:
                        logger.error(f"❌ Failed to send message: {e}")
                    await asyncio.sleep(0.3)
            except asyncio.CancelledError:
                logger.info("⏹️ Stream reading cancelled")
            except Exception as e:
                logger.exception(f"🚨 Error during video stream: {e}")

        self._stream_task = asyncio.create_task(reader())

async def entrypoint(ctx):
    await ctx.connect()
    logger.info("🔗 Connected to LiveKit room")
    session = AgentSession()
    await session.start(
        agent=VisionAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(video_enabled=True)
    )

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
