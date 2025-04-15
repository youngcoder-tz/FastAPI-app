import pandas as pd
from transformers import DistilBertForSequenceClassification, DistilBertTokenizer
from sklearn.model_selection import train_test_split
import torch
from torch.utils.data import Dataset, DataLoader
import joblib
from pathlib import Path

class ComplaintDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __getitem__(self, idx):
        text = str(self.texts[idx])
        encoding = self.tokenizer(
            text,
            max_length=self.max_len,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label': torch.tensor(self.labels[idx], dtype=torch.long)
        }

    def __len__(self):
        return len(self.texts)

def train_model(data_path: Path, model_dir: Path):
    # Load and preprocess data
    df = pd.read_csv(data_path)
    texts = df['text'].values
    labels = df['label'].values
    
    # Split data
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        texts, labels, test_size=0.2
    )
    
    # Initialize tokenizer and model
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    model = DistilBertForSequenceClassification.from_pretrained(
        'distilbert-base-uncased',
        num_labels=len(set(labels))
    )
    
    # Create datasets
    train_dataset = ComplaintDataset(train_texts, train_labels, tokenizer, 128)
    val_dataset = ComplaintDataset(val_texts, val_labels, tokenizer, 128)
    
    # Training setup
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)
    
    # Training loop
    for epoch in range(3):  # Example: 3 epochs
        model.train()
        for batch in DataLoader(train_dataset, batch_size=16):
            # Forward pass and backpropagation
            ...
    
    # Save artifacts
    model.save_pretrained(model_dir)
    tokenizer.save_pretrained(model_dir)
    joblib.dump(set(labels), model_dir / 'label_encoder.joblib')