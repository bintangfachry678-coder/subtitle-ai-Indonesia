import streamlit as st
import assemblyai as aai
import os

# 1. SETTING TAMPILAN WEB
st.set_page_config(page_title="AI Subtitle Generator", page_icon="🎬")
st.title("🎬 AI Subtitle Generator")
st.write("Upload videomu, dan AI akan buatkan file subtitle (.srt) otomatis.")

# 2. KONEKSI KE API KEY (Diambil dari Secrets Streamlit)
try:
    aai.settings.api_key = st.secrets["AAI_KEY"]
except:
    st.error("Waduh! API Key belum dipasang di Secrets Streamlit, Bro.")

# 3. TEMPAT UPLOAD VIDEO
uploaded_file = st.file_uploader("Pilih file video (mp4, mov)", type=["mp4", "mov"])

if st.button("Mulai Proses Subtitle") and uploaded_file:
    st.info("Sedang memproses... AI lagi dengerin video kamu. Sabar ya!")
    
    # Simpan file sementara di server
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    try:
        # 4. SETTING AI (Dukungan penuh Bahasa Indonesia)
        config = aai.TranscriptionConfig(
            speech_models=["universal-3-pro", "universal-2"], 
            language_code="id"
        )
        
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe("temp_video.mp4", config=config)
        
        if transcript.status == aai.TranscriptStatus.error:
            st.error(f"AI Error: {transcript.error}")
        else:
            # 5. EXPORT HASIL KE FORMAT SRT
            srt_data = transcript.export_subtitles_srt(chars_per_caption=30)
            
            st.success("✅ Selesai! Subtitle kamu sudah jadi.")
            
            # Tombol Download
            st.download_button(
                label="⬇️ DOWNLOAD SUBTITLE (.SRT)",
                data=srt_data,
                file_name="subtitle_otomatis.srt",
                mime="text/plain"
            )
            
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
    finally:
        # Hapus file sampah agar server tidak penuh
        if os.path.exists("temp_video.mp4"):
            os.remove("temp_video.mp4")

elif not uploaded_file:
    st.info("Silakan upload video dulu untuk memulai.")