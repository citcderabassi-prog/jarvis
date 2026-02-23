import os
import subprocess
import sys
import urllib.request

MODEL_DIR = "E:/models"
MODEL_PATH = os.path.join(MODEL_DIR, "TinyLlama.gguf")

# Official GGUF (TheBloke)
MODEL_URL = "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf"


# ================= STEP 1 =================
def install_engine():
    print("🔧 Installing llama-cpp-python...")

    subprocess.check_call([
        sys.executable, "-m", "pip",
        "install",
        "--upgrade",
        "--force-reinstall",
        "--no-cache-dir",
        "llama-cpp-python"
    ])

    print("✅ Engine installed successfully.\n")


# ================= STEP 2 =================
def download_model():
    print("📦 Preparing model directory...")

    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    if os.path.exists(MODEL_PATH):
        print("✅ Model already exists.")
        return

    print("⬇ Downloading TinyLlama GGUF model...")
    print("This may take several minutes...\n")

    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)

    print("\n✅ Model downloaded successfully.")


# ================= RUN SETUP =================
if __name__ == "__main__":
    install_engine()
    download_model()
    print("\n🚀 Setup complete. You can now run jarvis_gui.py")