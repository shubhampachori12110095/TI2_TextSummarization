
# Text Summarization on TED Talks

Dataset original: https://www.kaggle.com/rounakbanik/ted-talks. (não é necessário baixar)

---

## Estrutura do projeto

Pasta `data/`:

* `final_dataset.zip`: é apenas uma conveniência para pular uma etapa da preparação dos dados. Contém os dados já extraídos do dataset original.
    * `final_datasets.csv`: transcrições e resumos de referência.

* `text_input/`: pasta que contém os arquivos usados como entrada para o algoritmo TextRank. Os arquivos em si são gerados pelo script `preparation/prepare_data_to_algorithms.py`. Infelizmente não é possível disponibilizar os arquivos prontos devido ao tamanho.

* `bin_input/`: pasta que contém os arquivos usados como entrada para o algoritmo Pointer-generator. Os arquivos em si são gerados pelo script `preparation/prepare_data_to_algorithms.py`. Infelizmente não é possível disponibilizar os arquivos prontos devido ao tamanho.

Pasta `preparation/`:

* `clean_dataset.ipynb` ou `clean_dataset.py`: script usado para extrair do dataset original os dados que usamos no experimento. Não é necessário executar, o resultado já se encontra em `data/final_dataset.zip`.

* `prepare_data_to_algorithms.py`: script que converte os dados do dataset (`data/final_dataset.csv`) para o formato que cada algoritmo requer.

* `make_datafiles_for_pgn/`: código para converter os dados de entrada para o formato esperado pelo pointer-generator network. Disponível [aqui](https://github.com/dondon2475848/make_datafiles_for_pgn) e incluído junto apenas para facilitar.

Pasta `summarization/`:

* `pgn/`: diretório com as coisas necessárias para rodar o pointer-generator networks.
    * `pointer-generator/`: código fonte do algoritmo, disponível [aqui](https://github.com/abisee/pointer-generator) (Python2) ou [aqui](https://github.com/becxer/pointer-generator/) (Python3). Incluído junto apenas para facilitar.
    * `pretrained_model/`: deve conter o modelo pré-treinado disponibilizado junto com o código. Veja instruções abaixo para saber onde obtê-lo.
    * `vocab`: vocabulário usado pelo algoritmo. Disponível [aqui](https://github.com/JafferWilson/Process-Data-of-CNN-DailyMail). Incluído junto apenas para facilitar. Atualmente usa o vocabulário do dataset CNN-DailyMail, pois para usar outro seriam necessárias alterações na rede e retreinar do zero. No futuro, quem sabe, podemos utilizar um vocabulário só com as palavras dos TED Talks.

* `summarization.py`: arquivo usado para gerar os resumos. Usa 2 abordagens diferentes.
    * Abordagem extrativa: TextRank.  [Artigo](https://arxiv.org/pdf/1602.03606.pdf)  [Implementação](https://github.com/summanlp/textrank)
    
    * Abordagem abstrativa: Pointer-generator Networks. [Artigo](https://arxiv.org/abs/1704.04368)   [Implementação](https://github.com/abisee/pointer-generator)

Pasta `rouge_evaluation`:

* TODO
<!-- * Os resumos gerados são salvos em `rouge_evaluation/system`. -->

---

## Como rodar

### Preparando os dados

* Extraia o conteúdo de `data/final_dataset.zip` na própria pasta.

* Baixar o [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/). Ele é usado pelo script `/preparation/make_datafiles_for_pgn/make_datafiles.py` para tokenizar os dados de entrada.

* Adicione o StanfordCoreNLP ao classpath:

```
export CLASSPATH=/<path_to_the_folder_you_extracted>/stanford-corenlp-<version>.jar
```

* Execute o script `preparation/prepare_data_to_algorithms.py`. Isso irá popular as pastas `data/text_input` e `data/bin_input`.

### Executando os algoritmos

* Baixe o modelo pré-treinado do PLN, disponibilizado pelo autor junto com o código [aqui](https://github.com/abisee/pointer-generator). Ele é utilizado pois treinar o modelo desde o início levaria muito tempo.

### Avaliação

<!-- Ainda estou organizando as pastas, as instruções estão aqui
https://github.com/kavgan/ROUGE-2.0/blob/master/docs/usage-documentation.md -->