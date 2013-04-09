/**
  ADT representing a Playlist
  @name - string of function name
  @id - integer that is database id
*/
var Playlist = function(name, id) {
    self.name = name;
    self.id  = id;

    /** returns name of playlist */
    self.get_name() {
        return self.name;
    }

    /**
       sets the name of this playlist
       @new_name - string, new name of playlist
    */
    self.set_name(new_name) {
        self.name = new_name;
        // TODO - sync with server
    }
}