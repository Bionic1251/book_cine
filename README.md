# BookCine

**BookCine** is a cross-domain conversational recommender system, which suggests books and movies to users.

## Getting Started

To run **the server** in development mode:
```bash
% cd server
% export FLASK_APP=server
% flask run
```

To run **the client**, open *client/index.html*

## Required Datasets

The datasets necessary to run the system are as follows:
Movies: https://grouplens.org/datasets/movielens/tag-genome-2021/
Books: https://grouplens.org/datasets/book-genome/

## Corresponding Publications

The datasets are presented in the following publications:
- [Kotkov, D., Medlar, A., Maslov, A., Satyal, U. R., Neovius, M., and Glowacka, D. (2022, March). The tag genome dataset for books. In Proceedings of the 2022 Conference on Human Information Interaction and Retrieval (pp. 353-357).](https://doi.org/10.1145/3498366.3505833)
- [[Kotkov et al., 2021] Kotkov, D., Maslov, A., and Neovius, M. (2021). Revisiting the tag relevance prediction problem. In Proceedings of the 44th International ACM SIGIR conference on Research and Development in Information Retrieval.](https://doi.org/10.1145/3404835.3463019)
- [[Vig et al., 2012] Vig, J., Sen, S., and Riedl, J. (2012). The tag genome: Encoding community knowledge to support novel interaction. ACM Trans. Interact. Intell. Syst., 2(3):13:1–13:44.](https://dl.acm.org/doi/abs/10.1145/2362394.2362395)
