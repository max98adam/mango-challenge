import torch
import pytorch_lightning as pl
from torch import nn
from torchvision.models import squeezenet1_1, SqueezeNet1_1_Weights


class MyLightningModel(pl.LightningModule):
    def __init__(self, hparams):
        super(MyLightningModel, self).__init__()
        self.save_hyperparameters(hparams)  # Logger will log them

        self.pretrained_model = squeezenet1_1(weights=SqueezeNet1_1_Weights.DEFAULT)
        self.after_pretrained = nn.Sequential(
            nn.LazyLinear(out_features=hparams["latent_space_size"])
        )

        self.loss_fn = nn.TripletMarginWithDistanceLoss(distance_function=nn.PairwiseDistance())

        # Usd for printing layer shapes in model summary
        self.example_input_array = torch.Tensor(self.hparams["batch_size"], 3, hparams["img_height"],
                                                hparams["img_width"])

    def forward(self, x):
        pretrained_out = self.pretrained_model(x)
        latent_space = self.after_pretrained(pretrained_out)
        return latent_space

    def log_metrics(self, metrics, stage, epoch):
        for name, value in metrics.items():
            self.log(f"{stage}_{name}", metrics[name], on_step=False, on_epoch=True, prog_bar=True)

        # X axis on Tensorboard plots
        self.log("step", float(epoch), on_step=False, on_epoch=True, prog_bar=False)

    def log_plot(self, stage, name, fig):
        tb_image = self.plot_to_tensorboard_image(fig)
        tensorboard = self.logger.experiment
        tensorboard.add_image(f'{stage}_{name}', tb_image, self.current_epoch + 1)

    def evaluate(self, batch, stage=None):
        # batch shape: (batch, triplet_item, channel, x, y)

        anchor_batch = batch[:, 0]
        anchor_logits = self.forward(anchor_batch)

        positive_batch = batch[:, 1]
        positive_logits = self.forward(positive_batch)

        negative_batch = batch[:, 2]
        negative_logits = self.forward(negative_batch)

        latent_space = {
            "anchor": anchor_logits,
            "positive": positive_logits,
            "negative": negative_logits
        }

        loss = self.loss_fn(latent_space["anchor"], latent_space["positive"], latent_space["negative"])

        # Compute metrics
        metrics = {
            "loss": loss,
        }

        # Log metrics, used by Tensorboard
        if stage is not None:
            self.log_metrics(metrics, stage, self.current_epoch + 1)

        return metrics

    # Training
    def training_step(self, batch, batch_idx):
        metrics = self.evaluate(batch, "train")
        return metrics["loss"]

    def predict_step(self, batch, batch_idx):
        return self.forward(batch)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.hparams["learning_rate"])
