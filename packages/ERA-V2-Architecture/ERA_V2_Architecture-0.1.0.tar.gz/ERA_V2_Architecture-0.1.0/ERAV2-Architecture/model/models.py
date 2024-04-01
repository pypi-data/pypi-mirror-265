import torch
import torch.nn as nn
import torch.nn.functional as F
from torchsummary import summary

class Models:
    """
    In this class, we organize our neural network architectures as nested/inner classes.
    This approach groups related functionalities and creates an organized and encapsulated
    code structure. Each neural network architecture is defined as an inner class within
    this Models class. This allows for easy instantiation and clear hierarchy of neural
    network models, each with its distinct architecture and characteristics.
    """
    @staticmethod
    def evaluate_model(model_class, input_size=(3, 32, 32)):
        """
        Static method to evaluate the model architecture.
        This method will print a summary of the model showing the layers and parameters.

        Parameters:
        model_class (class): The inner class representing the neural network architecture to evaluate.
        input_size (tuple): The size of the input to the model. Default is (1, 28, 28) for MNIST dataset.
        """
        # Check for CUDA availability and set the device accordingly
        use_cuda = torch.cuda.is_available()
        device = torch.device("cuda" if use_cuda else "cpu")

        # Initialize the model from the inner class and move to the appropriate device
        model = model_class().to(device)

        # Print the summary of the model
        summary(model, input_size=input_size)



    class NetA(nn.Module):
        """
        Inner class representing an initial neural network architecture.
        """
        def __init__(self):
            super(Models.NetA, self).__init__()
            # Convolutional layers
            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 1     32     1   1    3      30     1    0  3
            self.convblock1 = nn.Sequential(
              nn.Conv2d(3, 32, 3),
              nn.BatchNorm2d(32),
              nn.ReLU(),
              nn.Dropout(0.1)
            )

            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 3     30    1    1    5      30     1    1  3
            self.convblock2 = nn.Sequential(
              nn.Conv2d(32, 16, 3,padding=1),
              nn.BatchNorm2d(16),
              nn.ReLU(),
              nn.Dropout(0.1)
            )
            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 5      30    1   1    5      30     1    0  1
            self.convblock3 = nn.Sequential(
              nn.Conv2d(16, 16, kernel_size=1),
              nn.BatchNorm2d(16),
              nn.ReLU(),
              nn.Dropout(0.1)
            )

            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 5     30    1    2    6      15     2    0  2
            self.pool1 = nn.MaxPool2d(2, 2)

            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            #  6    15     2   1    10     15     2   1  3
            self.convblock4 = nn.Sequential(
              nn.Conv2d(16, 16, 3,padding=1),
              nn.BatchNorm2d(16),
              nn.ReLU(),
              nn.Dropout(0.1)
            )
            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 10    15     2   1    14     15     2    1  3
            self.convblock5 = nn.Sequential(
              nn.Conv2d(16, 32, 3,padding=1),
              nn.BatchNorm2d(32),
              nn.ReLU(),
              nn.Dropout(0.1)
            )
            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 14    15     2   1    18     15     2    1  3
            self.convblock6 = nn.Sequential(
              nn.Conv2d(32, 32, 3,padding=1),
              nn.BatchNorm2d(32),
              nn.ReLU(),
              nn.Dropout(0.1)
            )
            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 18    15     2   1    18     15     2    0  1
            self.convblock7 = nn.Sequential(
              nn.Conv2d(32, 32, kernel_size=1),
              nn.BatchNorm2d(32),
              nn.ReLU(),
              nn.Dropout(0.1)
            )

            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 18    15     2   2    20     7      4  0  2
            self.pool2 = nn.MaxPool2d(2, 2)

            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 20    7     4    1    28     5      4    0  3
            self.convblock8 = nn.Sequential(
              nn.Conv2d(32, 16, 3),
              nn.BatchNorm2d(16),
              nn.ReLU(),
              nn.Dropout(0.1)
            )
            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 28    5     4    1    36     3     4     0  3
            self.convblock9 = nn.Sequential(
              nn.Conv2d(16, 32, 3),
              nn.BatchNorm2d(32),
              nn.ReLU(),
              nn.Dropout(0.1)
            )
            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 36    3     4    1    44     1     4     0  3
            self.convblock10 = nn.Sequential(
              nn.Conv2d(32, 32, 3),
              nn.BatchNorm2d(32),
              nn.ReLU(),
              nn.Dropout(0.1)
            )
            self.global_avg_pool = nn.AdaptiveAvgPool2d((1,1))  # Global pooling to reduce parameters

            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 44    2     4    1    44     1     4     0  1
            self.convblock11 = nn.Sequential(
              nn.Conv2d(32, 10, kernel_size=1)
            )

        def forward(self, x):
            x = self.convblock1(x)
            x = self.convblock2(x)
            x = self.convblock3(x)  # 1x1 conv
            x = self.pool1(x)

            x = self.convblock4(x)
            x = self.convblock5(x)
            x = self.convblock6(x)
            x = self.convblock7(x)  # 1x1 conv
            x = self.pool2(x)

            x = self.convblock8(x)
            x = self.convblock9(x)
            x = self.convblock10(x)

            x = self.global_avg_pool(x)
            x = self.convblock11(x)  # Final 1x1 conv

            # Flatten for the final output
            x = x.view(x.size(0), -1)
            return F.log_softmax(x, dim=-1)



    class NetB(nn.Module):
        """
        Inner class representing an initial neural network architecture.
        """
        def __init__(self):
            super(Models.NetB, self).__init__()
            # Convolutional layers
            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 1     32     1   1    3      30     1    0  3
            self.convblock1 = nn.Sequential(
              nn.Conv2d(3, 32, 3),
              nn.ReLU(),
              nn.Dropout(0.2)
            )

            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 3     30    1    1    5      30     1    1  3
            self.convblock2 = nn.Sequential(
              nn.Conv2d(32, 16, 3,padding=1),
              nn.ReLU(),
              nn.Dropout(0.2)
            )
            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 5      30    1   1    5      30     1    0  1
            self.convblock3 = nn.Sequential(
              nn.Conv2d(16, 16, kernel_size=1),
              nn.ReLU()
            )

            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 5     30    1    2    6      15     2    0  2
            self.pool1 = nn.MaxPool2d(2, 2)

            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            #  6    15     2   1    10     15     2   1  3
            self.convblock4 = nn.Sequential(
              nn.Conv2d(16, 16, 3,padding=1),
              nn.ReLU(),
              nn.Dropout(0.2),
              nn.LayerNorm(normalized_shape=[16, 15, 15])
            )
            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 10    15     2   1    14     15     2    1  3
            self.convblock5 = nn.Sequential(
              nn.Conv2d(16, 16, 3,padding=1),
              nn.ReLU(),
              nn.Dropout(0.1),
              nn.LayerNorm(normalized_shape=[16, 15, 15])
            )
            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 14    15     2   1    18     15     2    1  3
            self.convblock6 = nn.Sequential(
              nn.Conv2d(16, 32, 3,padding=1),
              nn.ReLU(),
              nn.Dropout(0.1)

            )
            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 18    15     2   1    18     15     2    0  1
            self.convblock7 = nn.Sequential(
              nn.Conv2d(32, 32, kernel_size=1),
              nn.ReLU()
            )

            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 18    15     2   2    20     7      4  0  2
            self.pool2 = nn.MaxPool2d(2, 2)

            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 20    7     4    1    28     5      4    0  3
            self.convblock8 = nn.Sequential(
              nn.Conv2d(32, 16, 3),
              nn.ReLU(),
              nn.Dropout(0.1),
              nn.LayerNorm(normalized_shape=[16, 5, 5])
            )
            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 28    5     4    1    36     3     4     0  3
            self.convblock9 = nn.Sequential(
              nn.Conv2d(16, 32, 3),
              nn.ReLU(),
              nn.Dropout(0.1),
              nn.LayerNorm(normalized_shape=[32, 3, 3])
            )
            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 36    3     4    1    44     1     4     0  3
            self.convblock10 = nn.Sequential(
              nn.Conv2d(32, 32, 3),
              nn.ReLU(),
              nn.Dropout(0.1),
              nn.LayerNorm(normalized_shape=[32, 1, 1])
            )
            self.global_avg_pool = nn.AdaptiveAvgPool2d((1,1))  # Global pooling to reduce parameters

            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 44    2     4    1    44     1     4     0  1
            self.convblock11 = nn.Sequential(
              nn.Conv2d(32, 10, kernel_size=1)
            )

        def forward(self, x):
            x = self.convblock1(x)
            x = self.convblock2(x)
            x = self.convblock3(x)  # 1x1 conv
            x = self.pool1(x)

            x = self.convblock4(x)
            x = self.convblock5(x)
            x = self.convblock6(x)
            x = self.convblock7(x)  # 1x1 conv
            x = self.pool2(x)

            x = self.convblock8(x)
            x = self.convblock9(x)
            x = self.convblock10(x)

            x = self.global_avg_pool(x)
            x = self.convblock11(x)  # Final 1x1 conv

            # Flatten for the final output
            x = x.view(x.size(0), -1)
            return F.log_softmax(x, dim=-1)



    class NetC(nn.Module):
        """
        Inner class representing an initial neural network architecture.
        """
        def __init__(self):
            super(Models.NetC, self).__init__()
            self.gn_group_count = 8


            # Convolutional layers
            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 1     32     1   1    3      30     1    0  3
            self.convblock1 = nn.Sequential(
              nn.Conv2d(3, 32, 3),
              nn.GroupNorm(self.gn_group_count,32),
              nn.ReLU(),
              nn.Dropout(0.1)
            )

            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 3     30    1    1    5      30     1    1  3
            self.convblock2 = nn.Sequential(
              nn.Conv2d(32, 16, 3,padding=1),
              nn.GroupNorm(self.gn_group_count,16),
              nn.ReLU(),
              nn.Dropout(0.1)
            )
            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 5      30    1   1    5      30     1    0  1
            self.convblock3 = nn.Sequential(
              nn.Conv2d(16, 16, kernel_size=1),
              nn.GroupNorm(self.gn_group_count,16),
              nn.ReLU(),
              nn.Dropout(0.1)
            )

            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 5     30    1    2    6      15     2    0  2
            self.pool1 = nn.MaxPool2d(2, 2)

            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            #  6    15     2   1    10     15     2   1  3
            self.convblock4 = nn.Sequential(
              nn.Conv2d(16, 16, 3,padding=1),
              nn.GroupNorm(self.gn_group_count,16),
              nn.ReLU(),
              nn.Dropout(0.1)
            )
            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 10    15     2   1    14     15     2    1  3
            self.convblock5 = nn.Sequential(
              nn.Conv2d(16, 32, 3,padding=1),
              nn.GroupNorm(self.gn_group_count,32),
              nn.ReLU(),
              nn.Dropout(0.1)
            )
            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 14    15     2   1    18     15     2    1  3
            self.convblock6 = nn.Sequential(
              nn.Conv2d(32, 32, 3,padding=1),
              nn.GroupNorm(self.gn_group_count,32),
              nn.ReLU(),
              nn.Dropout(0.1)
            )
            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 18    15     2   1    18     15     2    0  1
            self.convblock7 = nn.Sequential(
              nn.Conv2d(32, 32, kernel_size=1),
              nn.GroupNorm(self.gn_group_count,32),
              nn.ReLU(),
              nn.Dropout(0.1)
            )

            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 18    15     2   2    20     7      4  0  2
            self.pool2 = nn.MaxPool2d(2, 2)

            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 20    7     4    1    28     5      4    0  3
            self.convblock8 = nn.Sequential(
              nn.Conv2d(32, 16, 3),
              nn.GroupNorm(self.gn_group_count,16),
              nn.ReLU(),
              nn.Dropout(0.1)
            )
            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 28    5     4    1    36     3     4     0  3
            self.convblock9 = nn.Sequential(
              nn.Conv2d(16, 32, 3),
              nn.GroupNorm(self.gn_group_count,32),
              nn.ReLU(),
              nn.Dropout(0.1)
            )
            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 36    3     4    1    44     1     4     0  3
            self.convblock10 = nn.Sequential(
              nn.Conv2d(32, 32, 3),
              nn.GroupNorm(self.gn_group_count,32),
              nn.ReLU(),
              nn.Dropout(0.1)
            )
            self.global_avg_pool = nn.AdaptiveAvgPool2d((1,1))  # Global pooling to reduce parameters

            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 44    2     4    1    44     1     4     0  1
            self.convblock11 = nn.Sequential(
              nn.Conv2d(32, 10, kernel_size=1)
            )

        def forward(self, x):
            x = self.convblock1(x)
            x = self.convblock2(x)
            x = self.convblock3(x)  # 1x1 conv
            x = self.pool1(x)

            x = self.convblock4(x)
            x = self.convblock5(x)
            x = self.convblock6(x)
            x = self.convblock7(x)  # 1x1 conv
            x = self.pool2(x)

            x = self.convblock8(x)
            x = self.convblock9(x)
            x = self.convblock10(x)

            x = self.global_avg_pool(x)
            x = self.convblock11(x)  # Final 1x1 conv

            # Flatten for the final output
            x = x.view(x.size(0), -1)
            return F.log_softmax(x, dim=-1)


    class NetD(nn.Module):
        """
        Inner class representing an initial neural network architecture.
        """
        def __init__(self):
            super(Models.NetD, self).__init__()

            # Convolutional layers
            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 1     32     1   2    3      15     2    0  3
            self.convblock1 = nn.Sequential(
              nn.Conv2d(in_channels = 3, out_channels = 256, kernel_size = 3, stride=2, padding=0),
              nn.ReLU(),
              nn.Dropout(0.2)
            )

            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 3     15    2    2    7      7     4     0   3
            self.convblock2 = nn.Sequential(
              nn.Conv2d(in_channels = 256, out_channels = 128, kernel_size = 3, stride=2, padding=0, groups = 128),
              nn.ReLU(),
              nn.Dropout(0.2),

               # Pointwise convolution: expanding the number of channels
              nn.Conv2d(128, 128, kernel_size=1),  # Increase the channel depth from 32 to 128
              nn.ReLU(),
              nn.Dropout(0.1)

            )
            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 7     7     4    2    31     3     8,    1  3
            self.convblock3 = nn.Sequential(
              nn.Conv2d(in_channels = 128, out_channels = 64, kernel_size = 3,  stride=2, padding=3, dilation= 3),
              nn.ReLU(),
              nn.Dropout(0.1)
            )

            #R_in, N_in, j_in, S, R_out, N_out, J_out, P, K
            # 31    3     8    1    47     1      8    0, 3
            self.convblock4 = nn.Sequential(
              #nn.Conv2d(64, 16, 3,stride=1, padding=0)
              nn.Conv2d(in_channels=64, out_channels=16, kernel_size=3, stride=2, padding=2, dilation=2),
              nn.ReLU(),
              nn.Dropout(0.1)
            )


            self.global_avg_pool = nn.AdaptiveAvgPool2d((1,1))  # Global pooling to reduce parameters

            self.fc = nn.Linear(16, 10)

        def forward(self, x):
            x = self.convblock1(x)
            x = self.convblock2(x)
            x = self.convblock3(x)  # 1x1 conv
            x = self.convblock4(x)

            x = self.global_avg_pool(x)
            x = x.view(x.size(0), -1)  # Correct reshaping for batch size
            x = self.fc(x)
            return F.log_softmax(x, dim=-1)