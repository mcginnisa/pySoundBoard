1. font, various sizes, resolution, and number of squares can be configured through variables at the top of the script.
  * the resolution is set with the default raspi touch screen resolution in mind

2. config file needs at least the title at the top, and one file with at least 3 comma seperated fields.
  * quotations dont matter.
  * all comma seperated fields after the first three will be interpeted as sound filenames.



3. So far only .ogg and .wav seem to work, .mp3 seems to break it



4. sound files can be missing and the sound board wont crash
  the square will turn yellow if it cant find a sound file



5. Every line corresponds to a square, and there can be any number of lines between 1 and infinity
  the lines which exceed rows^2-2 will just be forgotten about by the soundboard
  * by default, there are 6 rows so there is room for 34 squares and 34 lines



6. pressing any empty square will silence the soundboard



7. the reset button will reset all the multiple-sound-file-per-square states
