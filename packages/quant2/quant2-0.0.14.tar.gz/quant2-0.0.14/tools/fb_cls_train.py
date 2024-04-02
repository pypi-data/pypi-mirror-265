# PYTHONPATH=$(pwd) python tools/fb_cls_train.py
import numpy as np
import random
import sys
import time
import torch
from copy import deepcopy
from pathlib import Path
from quant.io.logging import get_logger, print_log
from quant.io.utils import load_json, save_json


def train(model, device, train_loader, criterion, optimizer, epoch, log_interval, logger):
    model.train()
    dataloader_size = len(train_loader)
    for batch_idx, (data, target) in enumerate(train_loader, 1):
        data = [e.to(device) for e in data] if isinstance(
            data, (list, tuple)) else data.to(device)
        target = [e.to(device) for e in target] if isinstance(
            target, (list, tuple)) else target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % log_interval == 0:
            print_log(
                f"Train Epoch: {epoch} [{batch_idx}/{dataloader_size}] Loss: {loss.item():.6f}", logger)


def test(model, device, test_loader, criterion, logger):
    model.eval()
    test_loss, correct = 0, 0
    with torch.no_grad():
        for data, target in test_loader:
            data = [e.to(device) for e in data] if isinstance(
                data, (list, tuple)) else data.to(device)
            target = [e.to(device) for e in target] if isinstance(
                target, (list, tuple)) else target.to(device)
            output = model(data)
            test_loss += criterion(output, target).item()
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader)
    dataset_size = len(test_loader.dataset)
    test_acc = correct / dataset_size

    print_log(
        f"\nTest set: Avg loss: {test_loss:.6f}, Acc: {correct}/{dataset_size} ({test_acc:.4f})\n", logger)
    return test_acc


def main(config):
    _config = deepcopy(config)
    data, model, loss, optimizer, scheduler, runtime = \
        config["data"], config["model"], config["loss"], config["optimizer"], config["scheduler"], config["runtime"]

    seed = runtime.get("seed", 1)
    epochs = runtime.get("epochs", 90)
    device = runtime.get("device", "cuda")
    log_interval = runtime.get("log_interval", 10)

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    if device == "cuda" and torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")

    dataset_type = data.pop("type")
    data_root = Path(data["data_root"])
    if dataset_type == "ClassificationDataset":
        from quant.football.data.dataset import ClassificationDataset
        train_dataset = ClassificationDataset(data_root / data["train_file"])
        test_dataset = ClassificationDataset(data_root / data["test_file"])
    elif dataset_type == "FootballDataset":
        from quant.football.data.dataset import FootballDataset
        train_dataset = FootballDataset(data_root / data["train_file"])
        test_dataset = FootballDataset(data_root / data["test_file"])
    else:
        raise NotImplementedError(f"Not supported <{dataset_type}>.")

    train_loader = torch.utils.data.DataLoader(
        train_dataset, batch_size=data["batch_size"], shuffle=True
    )
    test_loader = torch.utils.data.DataLoader(
        test_dataset, batch_size=128
    )

    model_type = model.pop("type")
    if model_type == "STNetV1":
        from quant.football.models.stnet import STNetV1
        model = STNetV1(**model).to(device)
    elif model_type == "STNetV2":
        from quant.football.models.stnet import STNetV2
        model = STNetV2(**model).to(device)
    elif model_type == "STNetV3":
        from quant.football.models.stnet import STNetV3
        model = STNetV3(**model).to(device)
    else:
        raise NotImplementedError(f"Not supported <{model_type}>.")

    loss_type = loss.pop("type")
    if loss_type == "CrossEntropyLoss":
        from torch.nn import CrossEntropyLoss
        criterion = CrossEntropyLoss(**loss).to(device)
    else:
        raise NotImplementedError(f"Not supported <{loss_type}>.")

    optimizer_type = optimizer.pop("type")
    if optimizer_type == "SGD":
        from torch.optim import SGD
        optimizer = SGD(model.parameters(), **optimizer)
    elif optimizer_type == "AdamW":
        from torch.optim import AdamW
        optimizer = AdamW(model.parameters(), **optimizer)
    else:
        raise NotImplementedError(f"Not supported <{optimizer_type}>.")

    scheduler_type = scheduler.pop("type")
    if scheduler_type == "StepLR":
        from torch.optim.lr_scheduler import StepLR
        scheduler = StepLR(optimizer, **scheduler)
    else:
        raise NotImplementedError(f"Not supported <{scheduler_type}>.")

    out_dir = Path("runs") / time.strftime("%m%d%H%M%S")
    out_dir.mkdir(parents=True, exist_ok=True)

    logger = get_logger(__name__, False, out_dir / "log.txt")

    save_json(out_dir / "config.json", _config, indent=4)

    best_acc, best_epoch = 0.0, -1
    for epoch in range(1, epochs + 1):
        train(model, device, train_loader, criterion, optimizer,
              epoch, log_interval, logger)
        curr_acc = test(model, device, test_loader, criterion,
                        logger)
        if curr_acc > best_acc:
            best_acc, best_epoch = curr_acc, epoch
            torch.save(model.state_dict(), out_dir / f"model{epoch:03d}.pt")
        scheduler.step()
    torch.save(model.state_dict(), out_dir / "last.pt")

    print_log("[best model]", logger)
    print_log(f"\noutput dir: {out_dir}", logger)
    print_log(f"{best_acc=:.4f}, {best_epoch=:03d}\n", logger)

    print_log("[check train dataset]", logger)
    check_loader = torch.utils.data.DataLoader(train_dataset, batch_size=128)
    acc_train = test(model, device, check_loader, criterion, logger)
    return best_acc, acc_train


config = dict(
    data=dict(
        type="FootballDataset",
        data_root="/datasets/table20240326_v0401_2201to2310_label_s5whole",
        train_file="20240402002149.dat",
        test_file="20240402002205.dat",
        batch_size=128),
    model=dict(
        type="STNetV3",
        in_features=98,
        hidden_features=384,
        out_features=10,
        n_layers=1,
        bias=True,
        drop=0.,
        enable_skip=False,
        num_embeddings=2753,
        embedding_dim=50),
    loss=dict(type="CrossEntropyLoss", reduction="mean"),
    optimizer=dict(
        type="SGD",
        lr=0.2,
        momentum=0.9,
        weight_decay=0.0001),
    scheduler=dict(
        type="StepLR",
        step_size=10,
        gamma=0.1),
    runtime=dict(
        seed=1,
        epochs=30,
        device="cuda",
        log_interval=50))


if __name__ == "__main__":
    kwargs = {}
    for arg in sys.argv[1:]:
        key, value = arg.split("=")
        kwargs[key] = eval(value)

    if "config" in kwargs:
        config = load_json(kwargs["config"])

    for key, value in kwargs.items():
        names = key.split(".")
        d = config
        for name in names[:-1]:
            d = d[name]
        d[names[-1]] = value

    main(config)
