
/**
  ADT representing an individual piece of content
  TODO  - implement more than just pictures
  @image - an Image object of the actual media
  @id - integer that is database ID
*/
var Content = function(image, id) {
    self.image = image;
    self.id = id;
}