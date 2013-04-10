/**
 * ADT representing an Album
 *
 * @name - string of function name
 * @id - integer that is database id
 */
var Album = function(id) {
    this.id  = id;

    // TODO: create checkrep?

    /** returns name of album */
    this.get_name = function() {
        return "STUBBED ALBUM NAME " + this.id;

        // TODO: interface with server
        // caching?
    }

    this.get_contents = function() {

        var output = [];
        for (var i = 0; i < id + 1; ++i) {
            output.push(new Content());
        }
        return output;

        // TODO: interface with server
        // caching?
    }

    /** sets new name for this album */
    this.set_name = function() {
        // currently does nothing

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
}