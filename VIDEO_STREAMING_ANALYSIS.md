# Qiara Video Streaming Analysis

This document outlines the video streaming process used by the Qiara mobile application, based on the analysis of the decompiled Android application and the provided system files.

## Overview

The Qiara security system uses two primary protocols for video streaming:

*   **SRT (Secure Reliable Transport)**: This appears to be the preferred method for live video streaming. The app uses the `srtdroid-core` library to handle SRT connections.
*   **HLS (HTTP Live Streaming)**: This is likely used as a fallback or for viewing recorded video clips. The streams are encrypted using AES.

The overall process for initiating a video stream involves these steps:

1.  **Fetching Node Information**: The application retrieves a list of all connected devices (nodes) from the `/home/nodes` API endpoint. For cameras, this information includes a `stream_url_path`.

2.  **Opening the Stream**: To start a video stream, the app sends a request to the `/home/open_stream` endpoint.

3.  **Receiving Stream Credentials**: The response from `/home/open_stream` contains the necessary credentials to access the stream, including a `passphrase` for SRT streams.

4.  **Constructing the Stream URL**: The application constructs the final stream URL.
    *   For **SRT**, the URL is in the format: `srt://<host>:<port>?streamid=<stream_url_path>&passphrase=<passphrase>`.
    *   For **HLS**, the app would fetch a `.m3u8` playlist file from a URL likely provided in the node information.

5.  **Playing the Video**: The app uses the ExoPlayer library to play the video stream.
    *   For SRT, a custom `SrtDataSource` is used to feed the data from the `SrtSocket` to ExoPlayer.
    *   For HLS, the standard `HlsMediaSource` is used, with the `HlsAesInterceptor` handling decryption.

## Detailed Analysis

### SRT (Secure Reliable Transport)

The decompiled code shows extensive use of the `io.github.thibaultbee.srtdroid.core` library. Key classes involved are:

*   `co.qiara.app.components.videoPlayer.live.LivePlayerViewModel`: Contains the `listenSrtLiveStream` method, which is responsible for setting up and listening to the SRT stream.
*   `io.github.thibaultbee.srtdroid.core.models.SrtSocket`: Used to establish and manage the SRT connection.
*   `io.github.thibaultbee.srtdroid.core.models.SrtUrl`: A helper class to construct the SRT URL with all the necessary parameters, such as `passphrase`, `streamid`, and `latency`.
*   `co.qiara.app.core.domain.controllers.SrtController`: Manages the entire lifecycle of the SRT stream, from opening the connection to handling errors and managing credentials.
*   `i6/C5905a.java`: Defines a custom `SrtDataSource` that integrates the `SrtSocket` with ExoPlayer, allowing it to play SRT streams.

The string resources in `resources/res/values/strings.xml` also indicate that SRT is a user-configurable feature, with strings like `camera_settings_srt` and `camera_settings_srt_unsupported`.

### HLS (HTTP Live Streaming)

The presence of `androidx.media3.exoplayer.hls.HlsMediaSource` in the code confirms that the app is capable of playing HLS streams. The `co.qiara.app.data.api.bridge.HlsAesInterceptor` class strongly suggests that the HLS streams are encrypted with AES. The app would need to fetch the decryption key to play the stream.

The logging statements in `co.qiara.app.core.app.initializers.DatadogInitializer` and `co.qiara.app.core.app.initializers.TimberInitializer` look for `.ts` files and the "stream" keyword, which are characteristic of HLS.

### API Endpoints

The `qiara-api-openapi.yaml` file defines the following key endpoints for video streaming:

*   **/home/open_stream**: This endpoint is called to initiate a video stream. It takes a `force` parameter and returns a `ApiVideoStreamResponse`, which contains the `passphrase` for the SRT stream.
*   **/home/nodes**: This endpoint returns a list of all devices. The response for a camera node contains the `stream_url_path`, which is used to construct the SRT URL.
*   **/home/stream/live.jpeg**: This endpoint provides a JPEG snapshot of the live video stream.

## Conclusion

The Qiara mobile application employs a robust video streaming solution that uses both SRT and HLS. SRT appears to be the primary method for live streaming, offering low latency and reliability. HLS is likely used as a fallback or for accessing recorded clips, with AES encryption to secure the content. The entire process is orchestrated through a set of well-defined API endpoints that provide the necessary information to establish and authenticate the video stream.
