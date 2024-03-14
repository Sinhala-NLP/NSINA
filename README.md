***<span style="font-size: 3em;">:warning:</span>You must agree to the [license](https://github.com/Sinhala-NLP/NSINA?tab=License-1-ov-file#readme) and terms of use before using the dataset in this repo.***

# NSINa - A {N}ews Corpus for {Sin}hal{a}
This repository introduces **NSINA**, a comprehensive news corpus of over 500,000 articles from popular Sinhala news websites. Alongside **NSINA**, with different subsets, we also introduce three Sinhala NLP tasks [(1) News Media Identification](https://github.com/Sinhala-NLP/Sinhala-News-Media-Identification) [(2) News Category Prediction](https://github.com/Sinhala-NLP/Sinhala-News-Category-Prediction) and [(3) News Headline Generation](https://github.com/Sinhala-NLP/Sinhala-Headline-Generation). The release of **NSINA** aims to provide a solution to challenges in adapting large language models to Sinhala, offering valuable benchmarks and resources for improving NLP in the Sinhala language. **NSINA** is the largest news corpus for Sinhala. 

## Data Collection
For version 1.0, we collected news articles from 10 news media sites in Sri Lanka. Following table has the details. 

|     Source        |  Amount  |
|-------------------|----------|
| Adaderana         |  83918   |
| ITN News          |  30777   |
| Lankatruth        |  48180   |
| Divaina           |  26043   |
| Hiru News         | 130729   |
| Sinhala News LK   |  20371   |
| Lankadeepa        | 141663   |
| Vikalpa           |  14309   |
| Dinamina          |   7642   |
| Siyatha           |   3300   |
| **Total**         | **506932** |


## Data
**NSINA** is available in [HuggingFace](https://huggingface.co/datasets/sinhala-nlp/NSINA) and can be downloaded using the following code. 

```python
from datasets import Dataset
from datasets import load_dataset

nsina = Dataset.to_pandas(load_dataset('sinhala-nlp/NSINA', split='train'))
```


## Citation
If you are using the dataset or the models, please cite the following paper
~~~
﻿@article{Nsina2024,
author={Hettiarachchi, Hansi and Premasiri, Damith and Uyangodage, Lasitha and Ranasinghe, Tharindu},
title={{NSINA: A News Corpus for Sinhala}},
conference={The 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024)},
year={2024},
month={May},
}
~~~
