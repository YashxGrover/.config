# Media source

Spotify is the only enabled source. No media utility or browser extension is required.
If Spotify is closed, stopped, or unavailable, the song item hides. Paused songs keep their title.
Click the item to play or pause. macOS may require permission to control Spotify.

To connect another app or browser later, edit `media.json`:

- Set `source` to `external`.
- Set `external.metadata_argv` to an array containing the provider executable and its arguments.
- The provider must print JSON: `{"title":"Media title","state":"playing","app":"Browser"}`.
- Use `paused` to retain a paused title, or print `null` when nothing is playing.
- Optionally set `external.play_pause_argv` to the provider's play/pause command.

Commands run as argument arrays without a shell, with a five-second timeout.
The provider is queried at the bar's normal media interval; it should return cached or inexpensive metadata.
A future browser integration can implement this contract without changing the bar layout.
ByTune and browser monitoring are not enabled.
