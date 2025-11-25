import torch
import os

print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"Device count: {torch.cuda.device_count()}")

if torch.cuda.is_available():
    print(f"Current device name: {torch.cuda.get_device_name(0)}")
    print(f"Is the current device set to CUDA? {torch.backends.cuda.is_built()}")
else:
    print("---")
    print("CRITICAL: CUDA is NOT available. This is why you are using the CPU.")
    print("You need to install the correct PyTorch version for your CUDA driver.")

    # QUICK SCRIPT to check if CUDA is available (if the GPU is being used) and if the correct version of PyTorch is installed.
