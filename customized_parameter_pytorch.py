# -*- coding: utf-8 -*-
import torch
from torch.autograd import Variable
import torch.optim as optim

x = Variable(torch.FloatTensor([1, 2, 3]))
y = Variable(torch.FloatTensor([4, 5]))


class MLP(torch.nn.Module):
    def __init__(self):
        super(MLP, self).__init__()
        self.linear1 = torch.nn.Linear(3, 5)
        self.relu = torch.nn.ReLU()
        self.linear2 = torch.nn.Linear(5, 2)
        # the para to be added and updated in train phase, note that NO cuda() at last
        self.coefficient = torch.nn.Parameter(torch.Tensor([1.55]))

    def forward(self, x):
        x = self.linear1(x)
        x = self.relu(x)
        print("xxx", self.coefficient.shape)
        x = self.coefficient * x
        x = self.linear2(x)

        return x


model = MLP()

loss_fn = torch.nn.MSELoss(size_average=False)
optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

for t in range(500):
    y_pred = model(x)
    loss = loss_fn(y_pred, y)
    # print(t, loss.data[0])
    model.zero_grad()
    loss.backward()
    optimizer.step()

print(model(x))
