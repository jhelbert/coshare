/**
 * Central model in MVC framework.
 * 
 * Use this to register CoShare specific actions.
 */
var Model = function() {
    
    
    this.albums = []
    // populate albums when model is created
    // TODO: get from server
    

    this.add_album = function(album) {
        this.albums.push(album);
        this.fireEvent("add_album", {album: album});
    }

    /**
     * If the content was not already selected, select it
     * If the content was already selected, deselect it
     * @return true if content is now selected, false if unselected
     */
    this.toggle_content = function(content) {
        // TODO
    }


    this.select_album = function(album) {
        // TODO
        this.fireEvent("select_album", {album: album});
    }

    this.save_content = function(wasup) {

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