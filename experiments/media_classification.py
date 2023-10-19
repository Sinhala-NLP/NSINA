import pandas as pd
from sklearn.model_selection import train_test_split
import torch

from experiments.label_encoder import encode, decode
from transformer_model.evaluation import macro_f1, weighted_f1, print_stat
from transformer_model.model_args import ClassificationArgs
from transformer_model.run_model import ClassificationModel


full = pd.read_json("NSINa.json")

# Number of samples to take from each category
sample_size = 10000


# Define a function to sub-sample from each category
def sub_sample(group):
    return group.sample(min(len(group), sample_size))


# Group the DataFrame by 'Category' and apply the sub-sampling function
subsampled_df = full.groupby('Source', group_keys=False).apply(sub_sample)

# Reset the index of the resulting DataFrame
subsampled_df = subsampled_df.reset_index(drop=True)

subsampled_df = subsampled_df.rename(columns={'News Content': 'text', 'Source': 'labels'}).dropna()

subsampled_df = subsampled_df[["text", "labels"]]
subsampled_df['labels'] = encode(subsampled_df["labels"])

train, test = train_test_split(subsampled_df, test_size=0.2)

model_args = ClassificationArgs()
model_args.best_model_dir = "media_classification_outputs/sinbert/best_model"
model_args.eval_batch_size = 16
model_args.evaluate_during_training = True
model_args.evaluate_during_training_steps = 1000
model_args.evaluate_during_training_verbose = True
model_args.logging_steps = 1000
model_args.learning_rate = 2e-5
model_args.manual_seed = 777
model_args.max_seq_length = 256
model_args.model_type = "roberta"
model_args.model_name = "NLPC-UOM/SinBERT-large"
model_args.num_train_epochs = 5
model_args.output_dir = "media_classification_outputs/sinbert/"
model_args.overwrite_output_dir = True
model_args.save_steps = 1000
model_args.train_batch_size = 8
model_args.wandb_project = "NSINa_media_classification"
model_args.regression = False


model = ClassificationModel(model_args.model_type, model_args.model_name, num_labels=10, use_cuda=torch.cuda.is_available(),
                     args=model_args)
train, dev = train_test_split(train, test_size=0.1)


model.train_model(train, eval_df=dev, macro_f1=macro_f1, weighted_f1=weighted_f1)
model = ClassificationModel(model_args.model_type, model_args.best_model_dir, num_labels=10,
                     use_cuda=torch.cuda.is_available(), args=model_args)

test_sentences = test['text'].tolist()
predictions, raw_outputs = model.predict(test_sentences)

test['predictions'] = predictions

test['predictions'] = decode(test['predictions'])
test['labels'] = decode(test['labels'])

print_stat(test, 'labels', 'predictions')




