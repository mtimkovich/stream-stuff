# TextApp

Twitch Studio Beta doesn't support displaying text from a file like OBS, so this is my hack around it.

TextApp creates a simple window that displays text from a text file, updating every couple seconds.
The window can then be screen shared with Twitch Studio and the background color can be chroma keyed away.

## Usage

Modify `config.ini` with your desired settings.

## Issues

* Twitch Studio can't always tell which window it should be grabbing. I'm not sure how to improve this atm.
