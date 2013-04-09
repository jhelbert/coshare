/**
  ADT representing current selection
  This includes the playlist that is currently active.
  This includes which pieces of Content in the current playlist selected
*/
var Selection(playlist) {
    self.selected_playlist = playlist;
    self.selected_content = [];

    /** returns currently selected playlist */
    self.get_playlist() {
        return self.selected_playlist;
    }

    /** sets currently active playlist */
    self.set_playlist(new_playlist) {
        self.selected_playlist = new_playlist;
    }

    /** adds content to selection */
    self.add_selected_content(content) {
        // TODO
    }

    self.remove_from_selected_content(content) {
        // TODO
    }

    self.clear_selected_content() {
        self.selected_content = [];
    }

    self.select_all_content() {
        // TODO
    }
}