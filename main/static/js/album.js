/**
 * ADT representing an Album
 *
 * @name - string of function name
 * @id - integer that is database id
 */
var Album = function(id) {
    this.id  = id;
    this.name = "STUBBED ALBUM NAME " + (this.id + 1);

    // TODO: create checkrep?

    /** returns name of album */
    this.get_name = function() {
        return this.name;

        // TODO: interface with server
        // caching?
    }

    this.get_contents = function() {

        var output = [];
        for (var i = 0; i < id + 1; ++i) {
            output.push(new Content(i));
        }
        return output;

        // TODO: interface with server
        // caching?
    }

    /** sets new name for this album */
    this.set_name = function(name) {
        this.name = name;

        // TODO: interface with server

    }

    /** adds @new_content to the album, if not already present */
    this.add_content = function(new_content) {
        // currently does nothing

        // TODO: interface with server
    }

    /** removes @content from this album, if present */
    this.remove_content = function(content) {
        // current does nothing

        // TODO: interface with server
    }

    /** 
     * @return true iff @other has same id as album, 
     *         false otherwise
     */
    this.equals = function(other) {
        return this.id === other.id;
    }
}