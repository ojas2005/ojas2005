# Profile art

The ASCII portrait was sampled from the owner-supplied `Subject.png`, then rendered as actual monospace characters. The source photograph is intentionally not committed. No new facial details were generated.

- `ojas-terminal.gif`: animated portrait, terminal messages and gentle scan; plays twice, then rests.
- `ojas-terminal-static.png`: still alternative linked from the profile.
- `ojas-portrait-static.svg`: scalable character-based portrait.
- `ojas-portrait.txt`: the actual ASCII grid.
- `works-on-my-machine.gif`: original deployment joke animation.
- `duck-debugger.gif`: original ASCII rubber-duck consultant animation.
- `ojas-ascii.svg`: previous portrait retained for history/reference.

The two joke GIFs are original repo-owned artwork. Existing external badges, contribution graphics, typing banners and contextual GIFs retain their existing URLs in the README.

## Rebuild

Install Pillow in a local virtual environment, then run:

```sh
python scripts/generate_profile_art.py /path/to/Subject.png
```

The script uses the Menlo monospace font on macOS. Supply `--font /path/to/a-monospace.ttf` on another system. Output is deterministic; no model credentials, remote generation, source-photo upload, or animation runtime is needed by GitHub visitors.
