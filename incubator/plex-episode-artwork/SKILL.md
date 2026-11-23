---
name: plex-episode-artwork
description: Update Plex episode artwork from a supplied local image folder using the season-card editor and Finder drag and drop. Use for authorized episode thumbnail changes across shows or seasons, not media-file renaming or metadata rematching.
---

# Plex episode artwork

Status: incubating. The user demonstrated this workflow successfully; automated cross-window drag replay has not been qualified. Do not claim that recording the workflow proves replay works.

## Inputs and scope

Use the requested Plex server/library, show, season, episode range, and local artwork folder. Resolve each image against the displayed episode number AND title. Ask only about unresolved mappings. TVDB/TMDB numbering differences can affect the media underneath an episode; artwork changes do not authorize moving video files or editing metadata.

## Computer Use workflow

Use available authenticated Plex connectors if they support the requested operation reliably. Otherwise use Computer Use through cua_repl and the current browser and Finder windows.

1. Keep the Plex season grid and Finder image folder visible, preserving the user's window arrangement. The demonstrated arrangement has Finder beneath the browser.
2. Identify the target episode card. Reveal its controls and click the pencil at the lower left of that card. Verify the editor heading names the intended show, season, episode and title.
3. Select Poster. Verify the image drop area is visible.
4. In Finder identify the matching image by filename and visible artwork. Drag the image thumbnail into the Plex Poster drop area.
5. Confirm the upload success message and correct selected artwork. Click Save Changes. Verify the editor closes and the episode card shows the intended image.
6. Continue from the season grid, maintaining an exact list of confirmed saves and unresolved episodes.

Use fresh screenshots and accessibility state to ground actions. Derive drag endpoints from current supported screen coordinates; separate cropped app screenshots do not establish a shared coordinate origin. Never invent negative/off-window coordinates from estimated window offsets.

If cross-window dragging is unsupported or fails, say so. A supported browser file-upload API or verified file chooser is an acceptable fallback for completing authorized artwork updates. In a native chooser, confirm GoToWindow and PathTextField before setting a path; never type a path into a selected filename. Verify the selected file before opening it. Do not rename source files as part of uploading.

After a failed action, inspect state before retrying. Repeated noWindowsAvailable, stale-target errors, or disconnected browser errors are execution blockers; do not loop through the same failed actions. Stop with precise completion status after a bounded recovery attempt.

## Provenance and qualification

Source demonstration: Record & Replay session 573BEA8F-D220-4D56-B00A-29955FAA45CB, 2026-09-16 00:43:38–00:44:11 UTC. Events 5–8 show the episode 22 editor, Poster selection, Finder image drag to Arc, and Save Changes. The season grid subsequently displayed the American Classics card.

The reusable inputs are server, show, season, episode mapping, and artwork folder; the demonstrated year and episode are examples only. Requires Computer Use, a signed-in Plex session with artwork-edit rights, and readable local images. No Plex-specific connector was available in the originating session.

Positive scope check: updating supplied episode cards for another season follows this workflow with fresh mappings. Negative scope check: requests to rename video files, fix TVDB/TMDB matching, or create artwork must not activate this as an execution recipe for those operations.

Validation boundary: the user demonstrated the drag workflow, and native picker fallback saved one further episode. Automated drag replay did not upload. Subsequent native clicks repeatedly failed with noWindowsAvailable despite readable accessibility state. Keep this skill in the incubator until a live cross-window replay succeeds and the resulting card is visually verified; structural validation alone is insufficient for promotion.
