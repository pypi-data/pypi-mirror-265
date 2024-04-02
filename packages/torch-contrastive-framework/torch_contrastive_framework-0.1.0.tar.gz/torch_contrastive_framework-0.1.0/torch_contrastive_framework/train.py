import torch

DETECTED_DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def simCLR_criterion(batch1, batch2, temp=0.1):
    batch_size = batch1.size(0)
    x = torch.cat([batch1, batch2], dim=0)
    x = x / x.norm(dim=1)[:, None]
    x = torch.mm(x, x.t())
    x = torch.exp(x / temp)
    sums = x.sum(dim=0)
    x = torch.cat((torch.diagonal(x, offset=batch_size, dim1=1, dim2=0), torch.diagonal(x, offset=batch_size, dim1=0, dim2=1)))
    return -torch.log(x / (sums-x)).mean()

    
def simCLR_train_iteration(model, train_loader, projector, augment, optimizer, scheduler, criterion=simCLR_criterion, logger=None, device=DETECTED_DEVICE):
    model.train()
    total_loss = 0
    for batch in train_loader:
        optimizer.zero_grad()
        batch = batch.to(device)
        batch1, batch2 = augment(batch), augment(batch)
        h1, h2 = model(batch1), model(batch2)
        z1, z2 = projector(h1), projector(h2)
        loss = criterion(z1, z2)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    scheduler.step()
    mean_loss = total_loss / len(train_loader)
    if logger is not None:
        logger.log('train_loss', mean_loss)
    return mean_loss 

if __name__ == '__main__':
    import time
    start = time.time()
    batch_size = 12500
    temp = 0.1
    
    b1 = torch.stack([torch.arange(start=(i*batch_size)+1, end=((i+1)*batch_size)+1) for i in range(batch_size)])
    b2 = (0.5 * b1) + 3
    b1 = b1.to('cuda')
    b2 = b2.to('cuda')

    print(simCLR_criterion(b1, b2, temp))
    # print(simCLR_criterion(torch.tensor([
    #     [1.0, 0.0, 1.0],
    #     [-0.5, 0.866, 0.0],
    #     [-0.5, -0.866, 0.0],
    # ]), torch.tensor([
    #     [1.0, 0.0, 0.0],
    #     [-0.5, 0.866, 0.0],
    #     [-0.5, -0.866, 0.0],
    # ]), temp))

    print('Time:', (time.time() - start)*1000)
