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