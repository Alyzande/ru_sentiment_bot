# quick_test.py
print("Testing basic imports...")
try:
    import torch
    import transformers
    print("✓ Successfully imported PyTorch and Transformers!")
    print(f"PyTorch version: {torch.__version__}")
    
    # Quick test to see if we can use the GPU (optional, but cool)
    print(f"Is GPU available? {torch.cuda.is_available()}")
    
except ImportError as e:
    print(f"✗ Import failed: {e}")