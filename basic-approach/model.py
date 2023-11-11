import torch
import pytorch_lightning as pl
from torch import nn
from torchvision.models import mobilenet_v3_small, MobileNet_V3_Small_Weights


class MyLightningModel(pl.LightningModule):
    def __init__(self, hparams):
        super(MyLightningModel, self).__init__()
        self.save_hyperparameters(hparams)  # Logger will log them

        self.pretrained_model = mobilenet_v3_small(weights=MobileNet_V3_Small_Weights.DEFAULT)
        self.after_pretrained = nn.Sequential(
            nn.LazyLinear(out_features=hparams["latent_space_size"])
        )

        self.loss_fn = nn.TripletMarginWithDistanceLoss(distance_function=nn.PairwiseDistance())

        # Usd for printing layer shapes in model summary
        self.example_input_array = torch.Tensor(self.hparams["batch_size"], 3, 3, hparams["img_height"],
                                                hparams["img_width"])

    def forward(self, x):
        # x shape: (batch, triplet_item, channel, x, y)

        anchor_batch = x[:, 0]
        anchor_logits = self.pretrained_model(anchor_batch)
        anchor_logits = self.after_pretrained(anchor_logits)

        positive_batch = x[:, 1]
        positive_logits = self.pretrained_model(positive_batch)
        positive_logits = self.after_pretrained(positive_logits)

        negative_batch = x[:, 2]
        negative_logits = self.pretrained_model(negative_batch)
        negative_logits = self.after_pretrained(negative_logits)

        latent_space = {
            "anchor": anchor_logits,
            "positive": positive_logits,
            "negative": negative_logits
        }
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
        latent_space = self.forward(batch)
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
        x = batch
        return self.forward(x)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.hparams["learning_rate"])
