# Gemini 3.1 Flash Image

- On this page
- [Documentation](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-image#documentation)
- [gemini-3.1-flash-image](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-image#gemini-31-flash-image)

**Nano Banana 2** provides high-quality image generation and conversational
editing at a mainstream price point and low latency. It serves as the
high-efficiency counterpart to [Gemini 3 Pro Image](https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image), optimized for speed and
high-volume developer use cases.

**Key updates:**

- New output resolution options:
  - New support for 0.5K, 2K and 4K, default 1K
- New Image Search Grounding:
  - Integration of both text and image search results to inform generation with
    real-time web data
  - Supported with Thinking on or off
- New 1:4, 4:1, 1:8 and 8:1 aspect ratios
- Improved aspect ratio adherence
- Improved image quality and consistency
- Improved i18n text rendering

[Try in Google AI Studio](https://aistudio.google.com/?model=gemini-3.1-flash-image)

## Documentation

Visit the [Image generation](https://ai.google.dev/gemini-api/docs/image-generation) page for full
coverage of features and capabilities.

## gemini-3.1-flash-image

| Property | Description |
| --- | --- |
| id\_cardModel code | `gemini-3.1-flash-image` |
| saveSupported data types | **Inputs**<br>Text and Image / PDF<br>**Output**<br>Image and Text |
| token\_autoToken limits[\[\*\]](https://ai.google.dev/gemini-api/docs/tokens) | **Input token limit**<br>131,072<br>**Output token limit**<br>32,768 |
| handymanCapabilities | **[Audio generation](https://ai.google.dev/gemini-api/docs/speech-generation)**<br>Not supported<br>**[Caching](https://ai.google.dev/gemini-api/docs/caching)**<br>Not supported<br>**[Code execution](https://ai.google.dev/gemini-api/docs/code-execution)**<br>Not supported<br>**[File search](https://ai.google.dev/gemini-api/docs/file-search)**<br>Not supported<br>**[Function calling](https://ai.google.dev/gemini-api/docs/function-calling)**<br>Not supported<br>**[Grounding with Google Maps](https://ai.google.dev/gemini-api/docs/maps-grounding)**<br>Not supported<br>**[Image generation](https://ai.google.dev/gemini-api/docs/image-generation)**<br>Supported<br>**[Live API](https://ai.google.dev/gemini-api/docs/live-api)**<br>Not supported<br>**[Search grounding](https://ai.google.dev/gemini-api/docs/google-search)**<br>Supported<br>**[Structured outputs](https://ai.google.dev/gemini-api/docs/structured-output)**<br>Not supported<br>**[Thinking](https://ai.google.dev/gemini-api/docs/thinking)**<br>Supported<br>**[URL context](https://ai.google.dev/gemini-api/docs/url-context)**<br>Not supported |
| speedConsumption options | **[Batch API](https://ai.google.dev/gemini-api/docs/batch-api)**<br>Supported<br>**[Flex inference](https://ai.google.dev/gemini-api/docs/flex-inference)**<br>Not supported<br>**[Priority inference](https://ai.google.dev/gemini-api/docs/priority-inference)**<br>Not supported |
| 123Versions | Read the [model version patterns](https://ai.google.dev/gemini-api/docs/models/gemini#model-versions) for more details.<br>- Stable: `gemini-3.1-flash-image` |
| calendar\_monthLatest update | February 2026 |
| cognition\_2Knowledge cutoff | January 2025 |



 Send feedback



Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-06-23 UTC.


Need to tell us more?






\[\[\["Easy to understand","easyToUnderstand","thumb-up"\],\["Solved my problem","solvedMyProblem","thumb-up"\],\["Other","otherUp","thumb-up"\]\],\[\["Missing the information I need","missingTheInformationINeed","thumb-down"\],\["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"\],\["Out of date","outOfDate","thumb-down"\],\["Samples / code issue","samplesCodeIssue","thumb-down"\],\["Other","otherDown","thumb-down"\]\],\["Last updated 2026-06-23 UTC."\],\[\],\[\]\]
