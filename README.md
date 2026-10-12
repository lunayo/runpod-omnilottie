# runpod-omnilottie

RunPod serverless worker that generates a Lottie animation from a text prompt with [OmniLottie](https://huggingface.co/OmniLottie/OmniLottie). Needs a GPU with ~16 GB VRAM.

Inference code comes from [OpenVGLab/OmniLottie](https://github.com/OpenVGLab/OmniLottie), included as a git submodule in `OmniLottie/`. Clone with `git clone --recurse-submodules`.

## Run locally

```bash
git submodule update --init
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r OmniLottie/requirements.txt
python handler.py
python handler.py --rp_serve_api
```

Test the local API:

```bash
curl -X POST http://localhost:8000/runsync \
  -H "Content-Type: application/json" \
  -d @test_input.json
```

## Build

```bash
docker build --platform linux/amd64 -t runpod-test .
```

## Deploy to RunPod

```bash
docker tag runpod-test <dockerhub-user>/runpod-test:latest
docker push <dockerhub-user>/runpod-test:latest
```

Create a Serverless endpoint in the RunPod console with that image. Then call it:

```bash
curl -X POST https://api.runpod.ai/v2/<endpoint-id>/runsync \
  -H "Authorization: Bearer $RUNPOD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"prompt": "a bouncing red ball"}}'
```

Response: `{"lottie": {...lottie json...}}` or `{"error": "..."}`.

## Preview

Save the `lottie` field to a file and drop it into [LottieFiles Preview](https://lottiefiles.com/preview):

```bash
curl -s -X POST http://localhost:8000/runsync \
  -H "Content-Type: application/json" \
  -d @test_input.json | jq '.output.lottie' > out.json
```
