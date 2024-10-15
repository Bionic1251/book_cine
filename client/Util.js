class Util {
    static retrieveArray(data) {
        var arr = [];
        for (var key in data){
            arr.push(data[key]);
        }
        return arr;
    }

    static retrieve(data, field) {
        for (var key in data[field]){
            return data[field][key];
        }
        return null;
    }

    static retrieveByPos(data, field, pos) {
        let i = 0;
        for (var key in data[field]){
            if (i === pos) {
                return data[field][key];
            }
            i++;
        }
        return null;
    }

    static retrieveTags(tagData, item_id) {
        let arr = [];
        let itemIdDict = tagData["item_id"];
        for (let key in itemIdDict){
            if(itemIdDict[key] === item_id) {
                arr.unshift(tagData["tag"][key]);
            }
        }
        return arr;
    }

    static retrieveInternalIdByItemId(data, field, item_id) {
        for (var key in data[field]){
            if (data[field][key] === item_id) {
                return key;
            }
        }
        return null;
    }

    static arrayToString(arr) {
      return arr.join(', ');
    }

    static getItemIdByTitle(title, items) {
        for (var key in items){
            if (items[key] == title) {
                return key;
            }
        }
        return -1;
    }

    static sendRequest(address, dataToPass, successFunction) {
        $.ajax({
        url: address,
        method: "POST",
        dataType: "text",
        data: dataToPass,
        contentType: "app/json: charset=UTF-8",
        //complete: function (data) {},
        error: function (error, description, opt) {
            console.log("Error!");
            console.log(error);
            console.log(description);
            console.log(opt);
        },
        success: successFunction
    });
    }
};