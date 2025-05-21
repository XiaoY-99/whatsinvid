import torch
import torch.nn as nn
import torch.optim as optim
import time

#######################################
# A GPU Benchmark Script
# This script is designed to test the performance of a GPU using PyTorch.
# It creates a simple convolutional neural network (CNN) and trains it on random data.
# The script will print the device being used (CPU or GPU), the cuDNN version, and the training time.
# It also prints the loss at each epoch.  
#######################################

# Check device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)
print("cuDNN version:", torch.backends.cudnn.version())

# Define a small CNN
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.net = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(64 * 16 * 16, 100),
            nn.ReLU(),
            nn.Linear(100, 10)
        )

    def forward(self, x):
        return self.net(x)

model = SimpleCNN().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters())

# Random data: 1000 samples of 3x32x32 images
x = torch.randn(1000, 3, 32, 32).to(device)
y = torch.randint(0, 10, (1000,)).to(device)

# Train for a few epochs
epochs = 5
print(f"Training for {epochs} epochs...")
start = time.time()

for epoch in range(epochs):
    outputs = model(x)
    loss = criterion(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}")

end = time.time()
print(f"Training completed in {end - start:.2f} seconds")
