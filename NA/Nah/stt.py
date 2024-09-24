import os

#https://github.com/collabora/WhisperLive/tree/v0.5.0

if "OMP_NUM_THREADS" not in os.environ:
    os.environ["OMP_NUM_THREADS"] = str(1)

from whisper_live.server import TranscriptionServer
server = TranscriptionServer()
server.run(
    "0.0.0.0",
    port=9090,
    backend="faster_whisper",
    faster_whisper_custom_model_path=None,
    whisper_tensorrt_path=None,
    trt_multilingual=False,
    single_model=not True,
)





from whisper_live.client import TranscriptionClient
client = TranscriptionClient(
  "localhost",
  9090,
  lang="en",
  translate=False,
  model="small",
  use_vad=False,
  save_output_recording=True,                         # Only used for microphone input, False by Default
  output_recording_filename="./output_recording.wav"  # Only used for microphone input
)