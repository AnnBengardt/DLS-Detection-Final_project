from detect import run


run(weights='data/models/yoloTrained.pt', source="data/test-video.mp4", device="cpu", project="data", name="outputs", exist_ok=True)