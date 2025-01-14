***<span style="font-size: 3em;">:warning:</span>You must agree to the [license](https://github.com/Sinhala-NLP/NSINA?tab=License-1-ov-file#readme) and terms of use before using the dataset in this repo.***

# NSINa - A {N}ews Corpus for {Sin}hal{a}
This repository introduces **NSINA**, a comprehensive news corpus of over 500,000 articles from popular Sinhala news websites. Alongside **NSINA**, with different subsets, we also introduce three Sinhala NLP tasks [(1) News Media Identification](https://github.com/Sinhala-NLP/Sinhala-News-Media-Identification) [(2) News Category Prediction](https://github.com/Sinhala-NLP/Sinhala-News-Category-Prediction) and [(3) News Headline Generation](https://github.com/Sinhala-NLP/Sinhala-Headline-Generation). The release of **NSINA** aims to provide a solution to challenges in adapting large language models to Sinhala, offering valuable benchmarks and resources for improving NLP in the Sinhala language. **NSINA** is the largest news corpus for Sinhala. 

## Data Collection

For **version 1.0**, we collected news articles from ten news media sites in Sri Lanka. The following table has the details. 

|     Source        |  Amount  |
|-------------------|----------|
| Adaderana  *( <https://sinhala.adaderana.lk/> )*       |  83918   |
| ITN News  *( <https://www.itnnews.lk/> )*       |  30777   |
| Lankatruth  *( <https://lankatruth.com/si/> )*        |  48180   |
| Divaina   *( <https://divaina.lk/> )*         |  26043   |
| Hiru News  *( <https://www.hirunews.lk/> )*        | 130729   |
| Sinhala News LK *( <https://sinhala.news.lk/> )*   |  20371   |
| Lankadeepa  *( <https://www.lankadeepa.lk/> )*       | 141663   |
| Vikalpa   *( <https://www.vikalpa.org/> )*         |  14309   |
| Dinamina   *( <https://www.dinamina.lk/> )*        |   7642   |
| Siyatha  *( <https://siyathanews.lk/> )*          |   3300   |
| **Total**         | **506932** |

One of the .json files is shown below. 

```json
{
       "Source": "hirunews",
       "Timestamp": "Saturday, 02 May 2020 - 7:38",
       "Headline": "ශ්‍රී ලංකා එංගලන්ත ක්‍රිකට් තරගාවලියට නව කාලසටහනක්",
       "News Content": "කොවිඩ් -19 ගෝලීය වසංගතය හේතුවෙන් අතරමඟ දී අත්හිටුවනු ලැබූ එංගලන්ත ක්‍රිකට් පිළේ ශ්‍රී ලංකා සංචාරය සඳහා නව කාලසටහනක් සකස් කර තිබෙනවා. ඒ අනුව ලබන වසරේ ජනවාරි මාසයේ  එංගලන්ත පිළ නැවතත් ශ්‍රී ලංකාවට පැමිණීමට නියමිත බවයි ශ්‍රී ලංකා ක්‍රිකට් ප්‍රධාන විධායක ඈෂ්ලි ද සිල්වා ප්‍රකාශ කළේ. පසුගිය මාර්තු මාසයේ දිවයිනට පැමිණි එංගලන්ත කණ්ඩායම කොරෝනා වෛරස් ගෝලීය වසංගතය හේතුවෙන් දින 10කට පසු යළි සිය රට බලා නික්මුණේ පළමු ටෙස්ට් තරඟය ආරම්භවීමට සතියක් තිබියදියි.",
       "URL": "https://www.hirunews.lk/sports/239889/ශ්‍රී-ලංකා-එංගලන්ත-ක්‍රිකට්-තරගාවලියට-නව-කාලසටහනක්",
       "Category": "Sports",
       "Parent URL": "https://www.hirunews.lk/sports/all-news.php?pageID=100"
}
```


## Data

**Version 1.0**
All the .json files mentioned above were concatenated to create the final dataset. **NSINA** is available in [HuggingFace](https://huggingface.co/datasets/sinhala-nlp/NSINA) and can be downloaded using the following code. 

```python
from datasets import Dataset
from datasets import load_dataset

nsina = Dataset.to_pandas(load_dataset('sinhala-nlp/NSINA', split='train'))
```


## Citation
If you are using the dataset or the models, please cite the following paper.

~~~
﻿@inproceedings{Nsina2024,
author={Hettiarachchi, Hansi and Premasiri, Damith and Uyangodage, Lasitha and Ranasinghe, Tharindu},
title={{NSINA: A News Corpus for Sinhala}},
booktitle={The 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024)},
year={2024},
month={May},
}
~~~
