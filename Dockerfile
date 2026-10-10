FROM runpod/base:1.4.0-cuda1281-ubuntu2404

RUN ln -sf $(which python3.10) /usr/local/bin/python && \
    ln -sf $(which python3.10) /usr/local/bin/python3

# OmniLottie inference code (git submodule)
COPY OmniLottie/ /OmniLottie/

# Install dependencies
COPY requirements.txt /requirements.txt
RUN uv pip install --upgrade -r /requirements.txt -r /OmniLottie/requirements.txt --torch-backend cu128 --no-cache-dir --system

# Add files
COPY handler.py /handler.py

# Run the handler
CMD ["python", "-u", "/handler.py"]
