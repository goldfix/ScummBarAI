# Gemini 3.1 Flash Lite Image

- On this page
- [Documentation](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-lite-image#documentation)
- [gemini-3.1-flash-lite-image](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-lite-image#gemini-31-flash-lite-image)

**Nano Banana 2 Lite** is designed as the efficiency specialist of the image
generation family, offering ultra-low latency and cost-effective image
generation and editing. By targeting a sub-2 second latency and significantly
reduced TPU compute costs, this model enables high-volume interactive developer
use cases and real-time consumer applications.

**Key capabilities:**

- **Sub-2 second end-to-end latency**
- **Interleaved generation and editing** with native support for Text -> Text + Image(s) and Image + Text -> Text + Image(s).
- **Optimized for lower resolutions** of 1K (1024x1024px).
- Supports a discrete set of **14 aspect ratios** including standard formats.
- **Fast multi-turn local edits** (swapping colors, sticker creation, background adjustments).
- Maintains high character alignment matching original Nano Banana standards.
- New `1:1`, `3:2`, `2:3`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9` aspect ratios.
- Supported `image_size` values: `1024px` (1K). _(Note: 2K and 4K are unsupported)._
- **SynthID (Always On) + C2PA** watermarking.

[Try in Google AI Studio](https://aistudio.google.com/?model=gemini-3.1-flash-lite-image)

## Documentation

Visit the [Image generation](https://ai.google.dev/gemini-api/docs/image-generation) page for full
coverage of features and capabilities.

## gemini-3.1-flash-lite-image

| Property | Description |
| --- | --- |
| id\_cardModel code | `gemini-3.1-flash-lite-image` |
| saveSupported data types | **Inputs**<br>Text and Image<br>**Output**<br>Image and Text |
| token\_autoToken limits[\[\*\]](https://ai.google.dev/gemini-api/docs/tokens) | **Input token limit**<br>65,536<br>**Output token limit**<br>4,096 |
| handymanCapabilities | **Audio generation**<br>Not supported<br>**Batch API**<br>Supported<br>**Caching**<br>Not supported<br>**Code execution**<br>Not supported<br>**File search**<br>Not supported<br>**Function calling**<br>Supported<br>**Grounding with Google Maps**<br>Not supported<br>**Grounding with Google Search**<br>Not supported<br>**Image editing**<br>Supported<br>**Image generation**<br>Supported<br>**Live API**<br>Not supported<br>**Search grounding**<br>Not supported<br>**Structured outputs**<br>Not supported<br>**Thinking**<br>Supported (minimal and high)<br>**URL context**<br>Not supported |
| 123Versions | Read the [model version patterns](https://ai.google.dev/gemini-api/docs/models/gemini#model-versions) for more details.<br>- Stable: `gemini-3.1-flash-lite-image` |
| calendar\_monthLatest update | June 2026 |
| cognition\_2Knowledge cutoff | January 2025 |



 Send feedback



Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-07-09 UTC.


Need to tell us more?






\[\[\["Easy to understand","easyToUnderstand","thumb-up"\],\["Solved my problem","solvedMyProblem","thumb-up"\],\["Other","otherUp","thumb-up"\]\],\[\["Missing the information I need","missingTheInformationINeed","thumb-down"\],\["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"\],\["Out of date","outOfDate","thumb-down"\],\["Samples / code issue","samplesCodeIssue","thumb-down"\],\["Other","otherDown","thumb-down"\]\],\["Last updated 2026-07-09 UTC."\],\[\],\[\]\]
