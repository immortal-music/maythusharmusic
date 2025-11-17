FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .

# (Optional) သင့်မှာ setup.py ဒါမှမဟုတ် setup.cfg files တွေ သုံးထားသေးရင် 
# သူတို့ကိုပါ ဒီနေရာမှာ ကူးထည့်ပေးရပါမယ်။
# COPY setup.py .
# COPY setup.cfg .

# Install system dependencies, Deno, and Python packages in a single layer
RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        ffmpeg \
        curl \
        unzip \
        git \
    # Install Deno
    && curl -fsSL https://deno.land/install.sh | sh \
    && ln -s /root/.deno/bin/deno /usr/local/bin/deno \
    # Install Python dependencies
    && pip3 install -U pip \
    # requirements.txt အစား "pip3 install ." ကို အသုံးပြုပါ
    && pip3 install -U . --no-cache-dir \
    # Clean up apt cache
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code
COPY . .

# Set the default command
CMD ["bash", "start"]
