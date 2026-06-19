# Task Plot Review

## Evidence Match

- Pass: title and construct match the SST README and task logic.
- Pass: Go trial and Stop trial rows correctly collapse left/right arrow variants.
- Pass: Go flow shows fixation, go arrow, and timeout feedback only if no response.
- Pass: Stop flow shows fixation, pre-stop go window, adaptive SSD, and red stop-signal window.
- Pass: timings match config and controller bounds: 800-1000 ms fixation, 1000 ms go window, SSD 50-500 ms adaptive, 800 ms timeout feedback.
- Pass: response mapping is correct: F/J for left/right arrows; stop trials require withholding response.

## Visual Quality

- Pass: text is readable and rows are separated clearly.
- Pass: generated content stays below the reserved header band.
- Pass: fixed title and Construct subtitle are centered.
- Pass: top-right TaskBeacon logo lockup is borderless and non-overlapping.
- Pass: no generated title, logo, watermark, people, devices, or decorative scene is present.
- Note: first generation made timeout feedback look unconditional; second generation fixed this by adding `only if no response`.

## README Embed

- Pass: `README.md` contains `## 2. Task Flow`.
- Pass: the section embeds `![Task Flow](task_flow.png)`.
- Pass: final image is saved as `task_flow.png`; raw timeline is saved as `references/task_plot_timeline_raw.png`.
