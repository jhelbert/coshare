/**
 * ADT representing an Album
 *
 * @name - string of function name
 * @id - integer that is database id
 */
var Album = function(id,name) {
    this.id  = id;
    this.name = name;
    this.is_auto = false;
    this.output = []
<<<<<<< HEAD
    staticNames = ["Recently Favorited", "Recently Added", "All Added", "All Favorites", "Favorites", "All Content", "Tasks"];
=======
    staticNames = ["Recently Favorited", "Recently Added", "All Added", "Favorites", "All Content", "Tasks"];
>>>>>>> 953320664c89c1f37e985ae9e8f0d47b19c26846

    /*
    (function () {
        for (string in staticNames){
            if (this.name == string){
                return this.userGenerated = false;
            }
        }
        return this.userGenerated = true;
    })();*/

    this.is_user_generated = function () {
        for (i in staticNames){
            if (this.name === staticNames[i]){
                return false;
            }
        }
        return true;
    }

    // TODO: using this variable lends to rep-exposure; fix it.

    // TODO: create checkrep?

    /** returns name of album */
    this.get_name = function() {
        return this.name;

        // TODO: interface with server
        // caching?
    }

    this.get_contents = function() {

        
        return this.output;


        // TODO: interface with server
        // caching?
    }

    /** sets new name for this album */
    this.set_name = function(name) {
        this.name = name;

        // TODO: interface with server

    }

    /** adds @new_content to the album, if not already present */
    this.add_content = function(id,src,size) {
        var content = new Content(id,src,size);
        this.output.push(content);

        // TODO: interface with server
    }

    /** removes @content from this album, if present */
    this.remove_content = function(content) {
        // current does nothing
        var index = this.output.indexOf(content);
        if (index >= 0) {
            this.output.splice(index, 1);
        }


        // TODO: interface with server
    }

    /** 
     * @return true iff @other has same id as album, 
     *         false otherwise
     */
    this.equals = function(other) {
        return this.id === other.id;
    }

    this.can_rename = function() {
        return !this.is_auto;
    }

    this.can_remove = function() {
        return !this.is_auto;
    }

    this.can_edit_content = function() {
        return !this.is_auto;
    }
}
