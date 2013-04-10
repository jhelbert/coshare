/**
 * ADT representing an individual piece of content
 * 
 * TODO  - implement more than just pictures
 * 
 * @image - an Image object of the actual media
 * @id - integer that is database ID
 */
var Content = function(id) {
    this.id = id;

    /** @return javascript object of the image */
    this.get_content = function() {

        // use stubbed image for now
        var output = new Image();
        output.src = "static/rsc/pic.jpg";
        output.height = 50;
        return output;

        // TODO: interface with backend
        // request image object each time it's needed?
        // cache it?
    }

    /** sets the description of the image */
    this.set_description = function(new_description) {
        // currently does nothing

        // TODO: interface with backend
    }

    /** @return string description of content */
    this.get_description = function() {

        // use stubbed description for now
        return "Isn't this picture awesome!?";

        // TODO: interface with backend
        // request description each time it's needed
        // cache it?
    }

    /** 
     * @return true iff @other has same id as this piece of content, 
     *         false otherwise
     */
    this.equals = function(other) {
        return other.id && (this.id === other.id);
    }
    
}