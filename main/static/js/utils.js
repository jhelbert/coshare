// removes first occurrence of x in array, using `equals`
Array.prototype.removeSomething = function(x) {
    var index = -1;
    for (var i in this) {
        if (index >= 0) {
            continue;
        }
        if (this[i].equals(x)) {
            index = i;
        }
    }

    if (index >= 0) {
        this.splice(index, 1);
        return true;
    }
    return false;
};