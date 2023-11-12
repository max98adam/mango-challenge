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
        self.after_concat_with_metadata = nn.Sequential(
            nn.LazyLinear(out_features=hparams["latent_space_size"])
        )

        self.loss_fn = nn.TripletMarginWithDistanceLoss(distance_function=nn.PairwiseDistance())

        # Usd for printing layer shapes in model summary
        self.example_input_array = torch.Tensor(self.hparams["batch_size"], 3, hparams["img_height"],
                                                hparams["img_width"])

    def forward(self, img, metadata):
        pretrained_out = self.pretrained_model(img)
        reduced_pretrained_out = self.after_pretrained(pretrained_out)

        print(metadata)

        concat = torch.cat(reduced_pretrained_out, metadata_encoded)
        latent_space = self.after_concat_with_metadata(concat)
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

    def evaluate(self, x, stage=None):
        triplet_img, triplet_metadata = x
        # triplet_img shape: (batch, triplet_item, channel, x, y)

        anchor_batch = triplet_img[:, 0]
        anchor_logits = self.forward(anchor_batch, triplet_metadata[0])

        positive_batch = triplet_img[:, 1]
        positive_logits = self.forward(positive_batch, triplet_metadata[1])

        negative_batch = triplet_img[:, 2]
        negative_logits = self.forward(negative_batch, triplet_metadata[2])

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
    def training_step(self, x, batch_idx):
        metrics = self.evaluate(x, "train")
        return metrics["loss"]

    def predict_step(self, batch, batch_idx):
        return self.forward(batch)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.hparams["learning_rate"])
