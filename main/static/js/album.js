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
    staticNames = ["Recently Favorited", "Recently Added", "All Added", "All Favorites", "Favorites", "All Content", "Tasks"];

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
    this.add_content = function(id,src,size,is_new) {
        var content = new Content(id,src,size);
        this.output.push(content);
        if (is_new) {
              $.ajax({
                        type: "POST",
                        url: "/ajax/add_content/",
                        data: { album_id: this.id, pic_id:id }
                }).done(function( msg ) {
                    //refresh_last_modified(side);
              });
        }
        // TODO: interface with server
    }

    /** removes @content from this album, if present */
    this.remove_content = function(content) {
        // current does nothing
        var index = this.output.indexOf(content);
        var srcs = [];
        for (var i = 0; i < this.output.length; i++) {
            srcs.push(this.output[i].src);
            if (content.src == this.output[i].src) {
                this.output.splice(i, 1);
                console.log(i);
            }
        }
        console.log(srcs);
        console.dir(this.output);
        console.log(content);
        console.log(index);
        if (index >= 0) {
            this.output.splice(index, 1);
        }

        $.ajax({
                        type: "POST",
                        url: "/ajax/remove_content/",
                        data: { album_id: this.id, id:content.id }
                }).done(function( msg ) {
                    //refresh_last_modified(side);
              });


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
