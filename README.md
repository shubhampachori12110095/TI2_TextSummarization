
# Text Summarization on TED Talks

Dataset original: https://www.kaggle.com/rounakbanik/ted-talks

## Preparação dos dados

Pasta `preparation/`:

* `clean_dataset.ipynb` ou `clean_dataset.py`: usado para extrair do dataset original os dados que usamos no experimento.

## Sumarização

Pasta `summarization/`:

* `tedtalks.zip`: é apenas uma conveniência para evitar ter que fazer a etapa de preparação dos dados. Contém os dados já prontos pra uso.
    * `tedtalks.csv`: transcrições e resumos de referência.

* `summarization.py`: arquivo usado para gerar os resumos. Usa 2 abordagens diferentes.
    * Abordagem extrativa: TextRank.  [Artigo](https://arxiv.org/pdf/1602.03606.pdf)  [Implementação](https://github.com/summanlp/textrank)
    
    <!-- * TODO (Pointer-generator) -->

    * Os resumos gerados são salvos em `rouge_evaluation/system`.

## Avaliação

<!-- Ainda estou organizando as pastas, as instruções estão aqui
https://github.com/kavgan/ROUGE-2.0/blob/master/docs/usage-documentation.md -->