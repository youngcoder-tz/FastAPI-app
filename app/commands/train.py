import click
from pathlib import Path

@click.command()
@click.option('--data-path', required=True, type=Path)
@click.option('--output-dir', required=True, type=Path)
def train_model(data_path: Path, output_dir: Path):
    """Train new complaint classification model"""
    from app.services.model_training import train_model
    train_model(data_path, output_dir)