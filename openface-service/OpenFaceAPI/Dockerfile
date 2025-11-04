# ./OpenFaceAPI/Dockerfile
FROM python:3.12-slim

# Set up basic utilities (only once)
RUN apt-get update && apt-get install -y git curl vim && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Copy dependency list
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the app code (optional for devcontainer)
COPY . .

CMD ["bash"]
