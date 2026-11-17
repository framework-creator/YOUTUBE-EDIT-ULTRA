# YouTube rights and availability preflight

This is a **risk-reduction workflow, not a Content ID prediction system**. A source
that plays on YouTube can still be claimed, monetized by the rightsholder, muted,
blocked in some countries, or blocked everywhere after you re-upload any part of it.

## 1. Select footage before editing

The one-shot discovery pipeline first requires the existing documented reuse
permission and a trusted Creative Commons publisher. It now also calls the
official YouTube Data API v3 for **automatically discovered YouTube candidates**.
Any of these conditions exclude a candidate from automatic acquisition:

- API shows regional restrictions (either an allowlist or a blocklist), even if
  the current viewer can play the source.
- `licensedContent=true` indicates content claimed by a YouTube partner.
- Source lacks `creativeCommon` licence metadata, is not public or fully
  processed, or disallows embedded playback.
- API request fails, response is incomplete or the API key is unavailable.
  Such candidates are `UNKNOWN`, never silently classified as safe.

This policy is deliberately conservative and may exclude reusable footage.
Passing metadata means only that these specific warning signs were absent at
the time of checking. Creative Commons labels, successful extraction, official
accounts, fair-use arguments and video view counts do **not** establish ownership
or permission to redistribute footage.

Get a YouTube Data API v3 key with permission to call `videos.list` and set
it in your shell without adding it to this repository:

```bash
export YEU_YOUTUBE_API_KEY='YOUR_API_KEY'
ultra inspect-youtube 'https://www.youtube.com/watch?v=jNQXAC9IVRw'
ueu create 'Terence Crawford — R&B 2000s — 10 minutes'
```

The inspect result is `AVAILABLE_METADATA_ONLY`, `REJECT`, or `UNKNOWN`.
The first **does not mean** Content ID clean, rights-cleared, or publishable.
The decision and its reasons are stored on candidates in
`discovery_report.json`. Missing keys or quota failures block newly discovered
YouTube candidates instead of approving them by default.

Existing locally authorised media and explicit authorised URLs retain their
existing permission flow; this metadata check is **not** a substitute for a
complete audit of locally imported footage. Use `ueu create --mode commercial`
only with explicit rights documentation for each audio and video asset when
production is intended for distribution, and review the
`rights_report.json`. User `--attest-local-media` declarations are personal
attestations, not validated upload rights.

## 2. Check the final edited file, not just the source URLs

All new `ultra publish` and legacy `ultra create --publish` uploads are
**forced to private** even when `--privacy public`, `--privacy unlisted`,
or `--publish public` was requested. The requested and actual privacy states,
and the video URL, are saved in the local `*.youtube.json` upload receipt.

1. Open `https://studio.youtube.com/` for the uploaded file.
2. Wait until YouTube finishes copyright checks/processing, then inspect
   **Restrictions** and any specific countries affected. Check both the music
   and sports video claims. Do not interpret an unfinished check as a pass.
3. If there is a claim or block, do not publish the file. Rebuild from
   footage and music with documented rights, or pursue an authorized dispute
   where appropriate. Do not try to disguise Content ID matches by pitch,
   speed, cropping, mirroring, layering or fragmenting copyrighted material.
4. Publish manually from Studio **only after** clearing rights and reviewing
   all current restrictions. Future claims or territorial policy changes
   remain possible.

YouTube's public creator Data API does **not** provide a reliable general-purpose
pre-upload query for Content ID decisions. Studio's copyright check applies to
the **final MP4** and is not a guarantee against later claims. There is no
general GitHub solution that makes unlicensed Champions League broadcast
footage safe to re-upload.

## 3. Regression scope

The pipeline leaves action rankings, whole-event boundaries, original files,
audio mastering, existing job checkpoints, and editorial style unchanged.
Unit tests mock API responses (geo allowlist/blocklist, claim warning flags,
missing/invalid metadata, no key and network errors) and the upload API
(privacy status and duplicate-upload receipt). They do not upload any real
YouTube video or test live Content ID on a user's account.

References:
- [YouTube Data API video resource](https://developers.google.com/youtube/v3/docs/videos)
- [YouTube Studio copyright checks](https://support.google.com/youtube/answer/17011221)
- [How Content ID works](https://support.google.com/youtube/answer/2797370)
