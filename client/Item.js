class Item {
    constructor(type, data, topics) {
        this.description = Util.retrieve(data, "description");
        this.title = Util.retrieve(data, "title");
        if (type == BOOK_DOMAIN) {
            this.cover = Util.retrieve(data,"img");
            this.authors = Util.retrieveArray(data["authors"]);
            this.goodreadsUrl = Util.retrieve(data,"url");
        } else {
            this.cover = "https://image.tmdb.org/t/p/original/" + Util.retrieve(data,"posterPath");
            this.year = Util.retrieve(data,"year");
            this.runtime = Util.retrieve(data,"runtime");
            if (isNaN(this.runtime)) {
                this.runtime = 0;
            } else {
                this.runtime = Math.floor(this.runtime);
            }
            this.imdbUrl = "https://www.imdb.com/title/" + Util.retrieve(data,"imdbId");
            this.tmdbUrl = "https://www.themoviedb.org/movie/" + Util.retrieve(data,"tmdbMovieId");
            this.movielensUrl = "https://movielens.org/movies/" + Util.retrieve(data,"item_id");
        }
        this.id = Util.retrieve(data, "item_id");
        this.topics = Util.retrieveArray(topics["tag"]);
        this.topics.sort();
        this.data = data;
        this.type = type;
    }
}