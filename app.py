import streamlit as st
import assemblyai as aai
import os

# Konfigurasi Tampilan
st.set_page_config(page_title="AI Subtitle Generator", page_icon="🎬")
st.title("🎬 AI Subtitle Generator")
st.write("Upload videomu, dan AI akan buatkan file subtitle (.srt) otomatis.")

# KONEKSI OTOMATIS KE API KEY (Tanpa Input di Web)
try:
    aai.settings.api_key = st.secrets["AAI_KEY"]
except:
    st.error("Konfigurasi API Key belum lengkap di Secrets Streamlit.")

# Langsung ke tempat Upload
uploaded_file = st.file_uploader("Pilih file video (mp4, mov)", type=["mp4", "mov"])

if st.button("Mulai Proses Subtitle") and uploaded_file:
    st.info("Sedang memproses... Tunggu sebentar ya.")
    
    # Simpan file sementara
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    try:
        # Setting AI Bahasa Indonesia
        config = aai.TranscriptionConfig(
            speech_models=["universal-3-pro"], 
            language_code="id"
        )
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe("temp_video.mp4", config=config)
        
        if transcript.status == aai.TranscriptStatus.error:
            st.error(f"AI Error: {transcript.error}")
        else:
            # Export ke SRT
            srt_data = transcript.export_subtitles_srt(chars_per_caption=30)
            st.success("✅ Selesai! File subtitle siap didownload.")
            st.download_button(
                label="⬇️ DOWNLOAD SUBTITLE (.SRT)",
                data=srt_data,
                file_name="subtitle_otomatis.srt",
                mime="text/plain"
            )
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
    finally:
        # Hapus file sementara
        if os.path.exists("temp_video.mp4"):
            os.remove("temp_video.mp4")
