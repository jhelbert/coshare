/**
 * Central model in MVC framework.
 * 
 * Use this to register CoShare specific events.
 * 
 * Supported events: argument passed to event handler
 *    add_album: {album: album}
 *    remove_album: TODO
 *    select_content: {content: content}
 *    deselect_content: {content: content}
 *    select_album: {album: album}
 *    deselect_album: {album: album}
 */
var Model = function() {
    
    this.albums = []
    this.selected_album = null;
    this.selected_contents = [];

    // TODO: get from server

    // TODO: create checkrep?

    this.add_album = function(album,name) {
        this.albums.push(album);
        this.fireEvent("add_album", {album: album, name:name});
        
    }

    this.remove_selected_album = function() {

        // should not be able to remove auto album
        if (!this.selected_album.can_remove()) {
            return false;
        }

        var index = this.albums.indexOf(this.selected_album);
        this.albums.splice(index, 1);
        this.fireEvent("deselect_album", {album: this.selected_album});
        this.fireEvent("remove_album", {album: this.selected_album});
        this.select_album(this.albums[0]); // TODO: improve 
        this.select_album(this.albums[0]);
    }

    this.rename_selected_album = function() {

        // should not be able to rename auto album
        if (!this.selected_album.can_rename()) {
            return false;
        }

        // note, this is and MUST REMAIN a reference 
        // to the album in the `albums` liset
        this.selected_album.set_name("RENAMED");
        this.fireEvent("rename_album", {album: this.selected_album});
    }

    /**
     * If the content was not already selected, select it
     * If the content was already selected, deselect it
     * @return true if content is now selected, false if unselected
     */
    this.toggle_content = function(content) {

        if (content.id in this.selected_contents) {
            delete this.selected_contents[content.id]
            this.fireEvent("deselect_content", {content: content});
        } else {
            this.selected_contents[content.id] = content;
            this.fireEvent("select_content", {content: content});
        }
    }

    this.select_all = function() {

        var contents = this.selected_album.get_contents();
        this.selected_contents = []
        for (var i in contents) {
            var content = contents[i]
            this.selected_contents[content.id] = content;
            // WARNING: requires event listeners to be idempotent
            this.fireEvent("select_content", {content: contents[i]});
        }
    }

    this.deselect_all = function() {
        var contents = this.selected_contents;
        this.selected_contents = []
        for (var i in contents) {
            var content = contents[i]
            // WARNING: requires event listeners to be idempotent
            this.fireEvent("deselect_content", {content: content});
            console.log("DESELECTING " + i);
        }
        this.selected_contents = []
    }

    /**
     * changes selected album to given album
     * fires deselection of old album
     * fires selection of new album
     */
    this.select_album = function(album) {
        if (this.selected_album != null) {
            this.fireEvent("deselect_album", {album: this.selected_album})
        }
        this.selected_album = album;
        this.fireEvent("select_album", {album: album});

        // TODO: manage content selection
        // what if we are selecting the current album again?
        this.selected_contents = [];
    }


    // i'm really sorry about this name
    this.remove_selected_contents_from_selected_album = function() {
        for (var i in this.selected_contents) {
            var content = this.selected_contents[i];
            this.selected_album.remove_content(content);
            this.fireEvent("remove_content", {album: this.selected_album, content: content});
        }
    }

    this.get_num_selected_contents = function() {
        var output = 0;
        for (i in this.selected_contents) {
            if (this.selected_contents[i]) {
                output += 1
            }
        }
        return output;
    }

    // Event Management

    this.allHandlers = new Array();

    this.addEventListener = function(eventType, handler) {
        if (!this.allHandlers[eventType]) {
            this.allHandlers[eventType] = [];
        }
        this.allHandlers[eventType].push(handler);
    }

    this.fireEvent = function(type, details) {
        if (this.allHandlers[type]) {
            for (var i in this.allHandlers[type]) {
                this.allHandlers[type][i](details);
            }
        }
    }
}
