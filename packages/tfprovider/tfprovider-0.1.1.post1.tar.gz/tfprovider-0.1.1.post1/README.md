# tfprovider(-python)

This is a library to allow you to write Terraform providers in Python.

To actually deploy providers that use this library, you'll probably want to use
a packaging system like
[terradep-python](https://pypi.org/project/terradep-python/).

## Project status

**NOT USABLE YET** for anyone but myself, trust me.

**If this would be useful for you once completed, just let me know in an
issue** and I'll see what I can do to finish it. There is just no point working
on this if nobody needs it, and my own use case isn't as important to me
anymore, so I've put it on hold for now.

## Implemented/missing features

If you need any of these, please either open an issue (on GitLab or GitHub,
doesn't matter to me) or comment on an existing one and I'll see what I can do.
In contrast to larger projects, I actually prefer +1 comments over thumbs ups
*for now* (!) because they are easier for me to get notified of.

Most of them aren't difficult or time-consuming for me to implement, there is
just no point doing it if nobody needs it.

- General:
  - [ ] Not being completely horrible to use and full of bugs
- Kinds of Terraform objects:
  - [x] Resources
  - [ ] Data sources
- Terraform data types:
  - [x] Strings
  - [x] Sets of strings
  - [x] Unrefined unknowns
  - [ ] Refined unknowns
  - [ ] Anything else, including more complex types
- Miscellaneous features:
  - [ ] Private state
  - [ ] Upgrading state from earlier versions
    - Currently has an API for this that can't possibly work => needs overhaul
- Utilities:
  - [ ] Automatic comparison for `requires_replace`
- Infrastructure:
  - [ ] Possibly tighter integration with
    [terradep-python](https://pypi.org/project/terradep-python/)

## Development

### Sync/Async variants

The sync variant of the API is automatically generated from the async one
using [unasync](https://pypi.org/project/unasync/). With dev dependencies
installed, you can regenerate them by running `run_unasync.py` as a Python
script (e.g. via `poetry run run_unasync.py`).
