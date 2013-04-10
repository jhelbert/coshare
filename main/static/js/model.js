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
    this.selected_content = [];

    // TODO: get from server

    // TODO: create checkrep?

    this.add_album = function(album) {
        this.albums.push(album);
        this.fireEvent("add_album", {album: album});
    }

    this.remove_album = function(album) {
        // TODO
    }

    /**
     * If the content was not already selected, select it
     * If the content was already selected, deselect it
     * @return true if content is now selected, false if unselected
     */
    this.toggle_content = function(content) {
        var is_selected = false;
        var index;
        for (var i in this.selected_content) {
            if (selected_content[i].equals(content)) {
                is_selected = true;
                index = i;
            }
        }

        if (is_selected) {
            // remove from selection
            this.selected_content.splice(index, 1);
            this.fireEvent("deselect_content", {content: content});
            return false;
        } else {
            this.selected_content.push(content);
            this.fireEvent("content_selected", {content: content});
            return true;
        }
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
    }

    // Event Management

    this.allHandlers = new Array();

    this.addEventListener = function(eventType, handler){
        if (!this.allHandlers[eventType])
            this.allHandlers[eventType] = [];
        this.allHandlers[eventType].push(handler);
    }

    this.fireEvent = function(type, details){
        if (this.allHandlers[type]){
            for (var i in this.allHandlers[type]){
                this.allHandlers[type][i](details);
            }
        }
    }
}