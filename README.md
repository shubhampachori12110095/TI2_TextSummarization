
# Text Summarization on TED Talks

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

* `make_datafiles_for_pgn/`: código para converter os dados de entrada para o formato esperado pelo pointer-generator network. Disponível [aqui](https://github.com/dondon2475848/make_datafiles_for_pgn). É incluído junto apenas para facilitar.

Pasta `summarization/`:

* `pgn/`: diretório com as coisas necessárias para rodar o pointer-generator networks.
    * `pointer-generator/`: código fonte do algoritmo para Python 3, disponível [aqui](https://github.com/becxer/pointer-generator/). A [versão original](https://github.com/abisee/pointer-generator)) do autor é em Python2. É incluído junto apenas para facilitar.
    * `pretrained_model/`: deve conter o modelo pré-treinado disponibilizado junto com o código. Veja instruções abaixo para saber onde obtê-lo.
    * `vocab`: vocabulário usado pelo algoritmo. Disponível [aqui](https://github.com/JafferWilson/Process-Data-of-CNN-DailyMail). Incluído junto apenas para facilitar. Atualmente usa o vocabulário do dataset CNN-DailyMail, pois para usar outro seriam necessárias alterações na rede e retreinar do zero. No futuro, quem sabe, podemos utilizar um vocabulário só com as palavras dos TED Talks.

* `summarization.py`: arquivo usado para gerar os resumos. Usa 2 abordagens diferentes.
    * Abordagem extrativa: TextRank (mais informações abaixo)
    * Abordagem abstrativa: Pointer-generator Networks (mais informações abaixo)

Pasta `rouge_evaluation`:

* `textRankEvail/`:
    * `reference/`: resumos de referência, obtidos do dataset.
    * `system/`: resumos gerados pelo textrank.
* `pointerGenEvail/`:
    * `reference/`: resumos de referência, obtidos do dataset.
    * `system/`: resumos gerados pelo pointer-generator.

* `prepare_to_rouge.py`: script que extrai os resumos de referência do dataset e também converte os resumos gerados para o formato esperado pelo Rouge (uma sentença por linha)
* `generalize_results.py`: calcula a média dos resultados por algoritmo (o Rouge 2.0 só calcula para cada resumo, individualmente)

---

## Como rodar

### Preparando os dados

* Extraia o conteúdo de `data/final_dataset.zip` na própria pasta.

* Baixe o [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/). Ele é usado pelo script `/preparation/make_datafiles_for_pgn/make_datafiles.py` para tokenizar os dados de entrada.

* Adicione o Stanford CoreNLP ao classpath:

```sh
export CLASSPATH=/<path_to_the_folder_you_extracted>/stanford-corenlp-<version>.jar
```

* Execute o script `preparation/prepare_data_to_algorithms.py`. Isso irá popular as pastas `data/text_input` e `data/bin_input`.

```sh
cd preparation
python prepare_data_to_algorithms.py
```

### Executando os algoritmos

* Baixe o modelo pré-treinado do Pointer-Generator Network, disponibilizado pelo autor junto com o código [aqui](https://github.com/abisee/pointer-generator). Ele é utilizado pois treinar o modelo desde o início levaria muito tempo.

* Execute o arquivo `summarization/summarization.py`. Os resumos gerados serão salvos em `rouge_evaluation/system`.

```sh
cd summarization
python summarization.py
```

### Avaliação

* Instale o [Rouge 2.0](https://github.com/kavgan/ROUGE-2.0/blob/master/docs/usage-documentation.md). Extraia em alguma pasta

* Adicione o jar ao classpath:

```sh
export CLASSPATH=/<path_to_the_folder_you_extracted>/rouge2-xx.jar
```

* Execute o jar da pasta `rouge_evaluation/textRankEval/`:

```sh
cd rouge_evaluation/textRankEvail
java -jar <path_to_your_rouge2_jar>
```

* Execute o jar da pasta `rouge_evaluation/pointerGenEval/`:

```sh
cd rouge_evaluation/pointerGenEval
java -jar <path_to_your_rouge2_jar>
```

* Execute o arquivo `rouge_evaluation/generalize_results.py` para calcular a média dos resultados por algoritmo (o Rouge 2.0 só calcula as medidas individuais por resumo). Além disso, esse script corrige um pequeno problema nos CSVs `results.csv`: por algum motivo (locale?) o ponto decimal dos resultados gerados é escrito com ',', o que deixa o CSV com a formatação errada.

```sh
cd rouge_evaluation
python generalize_results.py
```

## Sources

| What | Where |
| :--- | :--- |
| TED Talks Dataset | https://www.kaggle.com/rounakbanik/ted-talks |
| Pointer-Generator-Networks source code | https://github.com/abisee/pointer-generator |
| Pointer-Generator-Networks paper | https://arxiv.org/abs/1704.04368 |
| TextRank source code | https://github.com/summanlp/textrank |
| TextRank paper |https://arxiv.org/pdf/1602.03606.pdf |