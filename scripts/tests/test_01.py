import torch

print(torch.cuda.is_available())
print(torch.backends.cudnn.version())
print("GPU:", torch.cuda.get_device_name(0))
