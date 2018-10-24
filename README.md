
# Text Summarization on TED Talks

---

## Estrutura do projeto

`data/`:

* `final_dataset.zip`: é apenas uma conveniência para pular uma etapa da preparação dos dados. Contém os dados já extraídos do dataset original.
    * `final_datasets.csv`: transcrições e resumos de referência.

* `text_input/`: pasta que contém os arquivos usados como entrada para o algoritmo TextRank. Os arquivos em si são gerados pelo script `preparation/prepare_data_to_algorithms.py`. Infelizmente não é possível disponibilizar os arquivos prontos devido ao tamanho.

`preparation/`:

* `clean_dataset.ipynb` ou `clean_dataset.py`: script usado para extrair do dataset original os dados que usamos no experimento. Não é necessário executar, o resultado já se encontra em `data/final_dataset.zip`.

* `prepare_data_to_algorithms.py`: script que converte os dados do dataset (`data/final_dataset.csv`) para o formato que os algoritmos requerem (uma sentença por linha).

`summarization/`:

* `pgn/`: diretório com as coisas necessárias para rodar o pointer-generator networks.
    * `pointer-generator/`: deve conter o código fonte do algoritmo em Python 3, disponível [aqui](https://github.com/becxer/pointer-generator/). A [versão original](https://github.com/abisee/pointer-generator)) do autor é em Python 2, mas aqui usamos a 3.
    * `pretrained_model/`: deve conter o modelo pré-treinado disponibilizado junto com o código, [aqui](https://github.com/becxer/pointer-generator/).
    * `make_datafiles_for_pgn/`: deve conter o código para converter os dados de entrada para o formato esperado pelo pointer-generator network. Disponível [aqui](https://github.com/dondon2475848/make_datafiles_for_pgn).
    * `vocab`: vocabulário usado pelo algoritmo. Disponível [aqui](https://github.com/JafferWilson/Process-Data-of-CNN-DailyMail). Incluído junto apenas para facilitar. Atualmente o código usa o vocabulário do dataset CNN-DailyMail, pois para usar outro seriam necessárias alterações no modelo do pointer-generator e retreinar do zero. No futuro, quem sabe, podemos utilizar um vocabulário só com as palavras dos TED Talks.

* `summarization.py`: arquivo usado para gerar os resumos. Usa 2 abordagens diferentes.
    * Abordagem extrativa: TextRank (mais informações abaixo)
    * Abordagem abstrativa: Pointer-generator Networks (mais informações abaixo)

`rouge_evaluation/`:

* `textRankEval/`:
    * `reference/`: resumos de referência, obtidos do dataset.
    * `system/`: local onde são salvos os resumos gerados pelo textrank.
    * `generated_summaries.zip`: resumos gerados pelo textrank, para quem não quiser executar.
    * `rouge.properties`: configurações do Rouge (que variações rodar, stopwords, etc).
    * `final_results.txt`: resultado do Rouge.
* `pointerGenEval/`:
    * `reference/`: resumos de referência, obtidos do dataset.
    * `system/`: local onde são salvos os resumos gerados pelo pointer-generator.
    * `generated_summaries.zip`: resumos gerados pelo ṕointer-generator, para quem não quiser executar.
    * `rouge.properties`: configurações do Rouge (que variações rodar, stopwords, etc).
    * `final_results.txt`: resultado do Rouge.

* `prepare_to_evaluation.py`: script que extrai os resumos de referência do dataset e também converte todos os resumos (de referência e gerados) para o formato esperado pelo Rouge (uma sentença por linha).
* `generalize_results.py`: calcula a média dos resultados por algoritmo (o Rouge 2.0 só calcula para cada resumo, individualmente)

---

## Como rodar

### Preparando os dados

* Extraia o conteúdo de `data/final_dataset.zip` na própria pasta.

* Execute o script `preparation/prepare_data_to_algorithms.py`. Isso irá popular a pastas `data/text_input`.

```sh
cd preparation
python prepare_data_to_algorithms.py
```

### Executando os algoritmos

* Baixe o código do Pointer-Generator, disponível [aqui](https://github.com/becxer/pointer-generator/) e extraia na pasta `summarization/pgn/pointer-generator/`.

* O Pointer-Generator é um tanto chato quanto ao formato das entradas. É necessário que os textos estejam em formato binário. Felizmente, há um código que faz essa conversão, disponível [aqui](https://github.com/dondon2475848/make_datafiles_for_pgn). Baixe esse código e extraia na pasta `summarization/pgn/make_datafiles_for_pgn/`.
    * Baixe o [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/). Ele é usado por esse script para tokenizar os dados de entrada.

    * Adicione o Stanford CoreNLP ao classpath:

    ```sh
    export CLASSPATH=/<path_to_the_folder_you_extracted>/stanford-corenlp-<version>.jar
    ```

* Baixe o modelo pré-treinado do Pointer-Generator Network, disponibilizado pelo autor junto com o código [aqui](https://github.com/abisee/pointer-generator). Utilizamos ele pois treinar o modelo desde o início levaria muito tempo.

* Execute o arquivo `summarization/summarization.py`. Os resumos gerados serão salvos em `rouge_evaluation/textRankEval/system/` e `rouge_evaluation/pointerGenEval/system/`.

```sh
cd summarization
python summarization.py
```

### Avaliação

* Instale o [Rouge 2.0](https://github.com/kavgan/ROUGE-2.0/blob/master/docs/usage-documentation.md) aonde preferir.

* Adicione o jar ao classpath:

```sh
export CLASSPATH=/<path_to_the_folder_you_extracted>/rouge2-xx.jar
```

* Execute o arquivo `rouge_evaluation/prepare_to_evaluation.py`. Ele faz duas coisas: encontra os respectivos resumos de referência no dataset e formata todos os resumos (gerados e de referência) no formato que o Rouge requer (uma sentença por linha).

```sh
cd rouge_evaluation
python prepare_to_evaluation.py
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