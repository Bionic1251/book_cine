class Item {
    constructor(type, data, topics, pos) {
        this.description = Util.retrieveByPos(data, "description", pos);
        this.title = Util.retrieveByPos(data, "title", pos);
        if (type == BOOK_DOMAIN) {
            this.cover = Util.retrieveByPos(data,"img", pos);
        } else {
            this.cover = "https://image.tmdb.org/t/p/original/" + Util.retrieveByPos(data,"posterPath", pos);
        }
        this.id = Util.retrieveByPos(data, "item_id", pos);
        if (!topics["item_id"]) {
            this.topics = Util.retrieveArray(topics["tag"]);
            return;
        }
        this.topics = Util.retrieveTags(topics, this.id);
        this.data = data;
        this.type = type;
    }
}