import torch
device = torch.device('cuda')
a=torch.tensor([[1., -1.], [1., -1.]]).cuda()
print(a.is_cuda)
