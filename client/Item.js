class Item {
    constructor(type, data, topics) {
        this.description = Util.retrieve(data, "description");
        this.title = Util.retrieve(data, "title");
        if (type == BOOK_DOMAIN) {
            this.cover = Util.retrieve(data,"img");
        } else {
            this.cover = "https://image.tmdb.org/t/p/original/" + Util.retrieve(data,"posterPath");
        }
        this.id = Util.retrieve(data, "item_id");
        this.topics = Util.retrieveArray(topics["tag"]);
        this.data = data;
        this.type = type;
    }
}