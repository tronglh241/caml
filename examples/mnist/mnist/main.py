import torch
from ignite.engine import (Events, create_supervised_evaluator,
                           create_supervised_trainer)
from ignite.handlers import ModelCheckpoint
from ignite.metrics import Accuracy, Loss
from torch.utils.tensorboard import SummaryWriter


def train(
    model,
    train_loader,
    val_loader,
    optimizer,
    criterion,
    log_interval,
    epochs,
):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(device)

    val_metrics = {
        'accuracy': Accuracy(),
        'nll': Loss(criterion),
    }

    writer = SummaryWriter(log_dir='logs')
    best_model_saver = ModelCheckpoint(
        'models',
        score_function=lambda evaluator: evaluator.state.metrics['accuracy'],
        score_name='accuracy',
        require_empty=False,
        n_saved=10,
    )

    trainer = create_supervised_trainer(model, optimizer, criterion, device=device)
    evaluator = create_supervised_evaluator(model, metrics=val_metrics, device=device)

    @trainer.on(Events.ITERATION_COMPLETED(every=log_interval))
    def log_training_loss(engine):
        print(
            f'Epoch[{engine.state.epoch}] Iteration[{engine.state.iteration}/{len(train_loader)}] '
            f'Loss: {engine.state.output:.2f}'
        )
        writer.add_scalar('training/loss', engine.state.output, engine.state.iteration)

    @trainer.on(Events.EPOCH_COMPLETED)
    def log_training_results(engine):
        evaluator.run(train_loader)
        metrics = evaluator.state.metrics
        avg_accuracy = metrics['accuracy']
        avg_nll = metrics['nll']
        print(
            f'Training Results - Epoch: {engine.state.epoch} Avg accuracy: {avg_accuracy:.2f} Avg loss: {avg_nll:.2f}'
        )
        writer.add_scalar('loss/training', avg_nll, engine.state.epoch)
        writer.add_scalar('accuracy/training', avg_accuracy, engine.state.epoch)

    @trainer.on(Events.EPOCH_COMPLETED)
    def log_validation_results(engine):
        evaluator.run(val_loader)
        metrics = evaluator.state.metrics
        avg_accuracy = metrics['accuracy']
        avg_nll = metrics['nll']
        print(
            f'Validation Results - Epoch: {engine.state.epoch} Avg accuracy: {avg_accuracy:.2f} Avg loss: {avg_nll:.2f}'
        )
        writer.add_scalar('loss/valdation', avg_nll, engine.state.epoch)
        writer.add_scalar('accuracy/valdation', avg_accuracy, engine.state.epoch)

    evaluator.add_event_handler(Events.COMPLETED, best_model_saver, {'model': model})

    # kick everything off
    trainer.run(train_loader, max_epochs=epochs)

    writer.close()

    return str(best_model_saver.last_checkpoint) if best_model_saver.last_checkpoint else None
