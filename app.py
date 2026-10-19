import io
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from audio_recorder_streamlit import audio_recorder
import soundfile as sf
import streamlit as st

# إعدادات الصفحة
st.set_page_config(
    page_title="SADA | نظام الكشف المبكر",
    page_icon="🔊",
    layout="wide"
)
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, #172D40 0%, transparent 38%),
        radial-gradient(ellipse at 95% 15%, #251B3B 0%, transparent 32%),
        #080D16;
    color: #EAF2FA;
}

[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer {
    visibility: hidden;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111C2B, #0B111B);
    border-right: 1px solid #26394D;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #43D9D0;
}

h1, h2, h3 {
    color: #F3F7FF !important;
    letter-spacing: -0.4px;
}

p, label {
    color: #B9C9D9;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #172638, #101925);
    border: 1px solid #2B455B;
    border-radius: 16px;
    padding: 20px 18px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.20);
    transition: border-color 0.2s ease,
                transform 0.2s ease;
}

[data-testid="stMetric"]:hover {
    border-color: #43D9D0;
    transform: translateY(-3px);
}

[data-testid="stMetricLabel"] {
    color: #AFC4D7 !important;
}

[data-testid="stMetricValue"] {
    color: #43D9D0 !important;
    font-weight: 800;
}

.stButton > button {
    background: linear-gradient(110deg, #43D9D0, #64BFD7);
    color: #08131D;
    border: none;
    border-radius: 11px;
    font-weight: 800;
    padding: 0.65rem 1.2rem;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(110deg, #72F0E7, #91D9F0);
    color: #08131D;
    box-shadow: 0 0 20px rgba(67,217,208,0.20);
    transform: translateY(-1px);
}

[data-testid="stSlider"] [role="slider"] {
    border-color: #43D9D0;
}

[data-testid="stDataFrame"],
[data-testid="stTable"] {
    border: 1px solid #293D52;
    border-radius: 13px;
    overflow: hidden;
}

[data-testid="stAlert"] {
    border-radius: 12px;
    border: 1px solid #30485E;
}

hr {
    border-color: #26394D;
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
}

@media (max-width: 768px) {
    .block-container {
        padding: 1rem 0.8rem 2rem;
    }

    [data-testid="stMetric"] {
        padding: 13px 10px;
    }
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<div style="
    padding: 22px;
    border: 1px solid #254657;
    border-right: 5px solid #43D9D0;
    border-radius: 14px;
    background: linear-gradient(135deg, #152433, #0B111A);
    margin-bottom: 12px;
">
    <div style="
        color: #43D9D0;
        font-size: 13px;
        letter-spacing: 4px;
        font-weight: bold;
    ">SMART SAFETY SYSTEM</div>
    <div style="
        color: #FFFFFF;
        font-size: 36px;
        font-weight: 800;
        margin-top: 8px;
    ">SADA <span style="color:#43D9D0;">| صَدَى</span></div>
    <div style="
        color: #B7C8D8;
        font-size: 15px;
        margin-top: 8px;
    ">نظام ذكي لمراقبة سلامة الحواجز وتحليل الإشارات الصوتية</div>
</div>
""", unsafe_allow_html=True)
st.caption(
    "نظام ذكي للكشف المبكر عن مخاطر الحواجز "
    "وتحليل الإشارات الصوتية."
)
st.markdown("""
<div style="
    display:flex;
    flex-wrap:wrap;
    align-items:center;
    justify-content:space-between;
    gap:16px;
    background:linear-gradient(110deg,#111E2D,#17152A);
    border:1px solid #293C52;
    border-radius:15px;
    padding:16px 20px;
    margin:22px 0;
    box-shadow:0 8px 28px rgba(0,0,0,0.20);
">
    <div style="display:flex;align-items:center;gap:12px;">
        <div style="
            width:11px;height:11px;border-radius:50%;
            background:#43D9D0;
            box-shadow:0 0 12px #43D9D0;
        "></div>
        <div>
            <div style="color:#F3F7FF;font-weight:800;font-size:15px;">
                SADA SYSTEM
            </div>
            <div style="color:#8FA7BD;font-size:12px;margin-top:4px;">
                منصة مراقبة وتحليل الإشارات
            </div>
        </div>
    </div>
    <div style="
        padding:9px 13px;
        border-radius:9px;
        background:#202B36;
        border:1px solid #3A4A5A;
        color:#F2C879;
        font-size:12px;
        font-weight:700;
    ">
        ◈ وضع المحاكاة التجريبي
    </div>
    <div style="color:#43D9D0;font-size:12px;letter-spacing:1px;">
        STRUCTURAL + AUDIO
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("""
<div style="
    display:flex;
    align-items:center;
    gap:14px;
    margin:30px 0;
">
    <div style="height:1px;flex:1;background:linear-gradient(to right,transparent,#43D9D0);"></div>
    <div style="color:#43D9D0;font-size:12px;letter-spacing:3px;font-weight:bold;">
        SADA • SYSTEM ANALYSIS
    </div>
    <div style="height:1px;flex:1;background:linear-gradient(to left,transparent,#A78BFA);"></div>
</div>
""", unsafe_allow_html=True)
# أدوات التحكم التفاعلية في القائمة الجانبية للتجربة
st.sidebar.title("🎛️ لوحة التحكم")
st.sidebar.caption("إعدادات المحاكاة التجريبية")
st.sidebar.info(
    "🧪 وضع المحاكاة التجريبي\n\n"
    "تعرض المنصة قراءات افتراضية لاختبار استجابة النظام "
    "والتنبيهات. لم تُربط الحساسات الحقيقية بعد."
)

simulated_pressure = st.sidebar.slider(
    "قراءة الضغط (Bar)", min_value=1.0, max_value=6.0, value=4.0
)


simulated_vibration = st.sidebar.slider(
    "قراءة الاهتزاز (G)",
    min_value=0.0,
    max_value=1.0,
    value=0.2,
    step=0.05
)

# --- العمود الأول: لوحة الحساسات ---
# تقسيم الصفحة إلى عمودين (الحساسات + تحليل الصوت)
col1, col2 = st.columns([1, 1.2], gap="large")

# --- لوحة الحساسات الذكية ---
with col1:
    st.header("📡 لوحة مراقبة الحواجز")
    st.caption("STRUCTURAL SENSOR MONITORING")

    pressure_alert = simulated_pressure > 3.5
    vibration_alert = simulated_vibration > 0.4

    sub_col1, sub_col2 = st.columns(2)

    pressure_color = "#FF6B7A" if pressure_alert else "#43D9D0"
    vibration_color = "#FF6B7A" if vibration_alert else "#A78BFA"

    with sub_col1:
        st.markdown(f"""
        <div style="
            background:linear-gradient(145deg,#172638,#101925);
            border:1px solid {pressure_color}55;
            border-top:3px solid {pressure_color};
            border-radius:16px;
            padding:20px 14px;
            min-height:145px;
            box-shadow:0 8px 24px rgba(0,0,0,0.18);
        ">
            <div style="color:#AFC4D7;font-size:13px;">
                ◈ ضغط الحاجز
            </div>
            <div style="
                color:{pressure_color};
                font-size:27px;
                font-weight:800;
                margin:15px 0;
            ">
                {simulated_pressure:.2f}
                <span style="font-size:13px;">Bar</span>
            </div>
            <div style="
                color:{pressure_color};
                font-size:11px;
                font-weight:700;
            ">
                {"● تجاوز الحد التجريبي" if pressure_alert else "● ضمن النطاق التجريبي"}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with sub_col2:
        st.markdown(f"""
        <div style="
            background:linear-gradient(145deg,#172638,#101925);
            border:1px solid {vibration_color}55;
            border-top:3px solid {vibration_color};
            border-radius:16px;
            padding:20px 14px;
            min-height:145px;
            box-shadow:0 8px 24px rgba(0,0,0,0.18);
        ">
            <div style="color:#AFC4D7;font-size:13px;">
                ◈ اهتزاز الحاجز
            </div>
            <div style="
                color:{vibration_color};
                font-size:27px;
                font-weight:800;
                margin:15px 0;
            ">
                {simulated_vibration:.2f}
                <span style="font-size:13px;">G</span>
            </div>
            <div style="
                color:{vibration_color};
                font-size:11px;
                font-weight:700;
            ">
                {"● تجاوز الحد التجريبي" if vibration_alert else "● ضمن النطاق التجريبي"}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    if pressure_alert or vibration_alert:
        st.error("🚨 تم رصد تجاوز للحد التجريبي")

        if pressure_alert and vibration_alert:
            st.write("تم تجاوز الحد التجريبي للضغط والاهتزاز.")
        elif pressure_alert:
            st.write("تم تجاوز الحد التجريبي للضغط.")
        else:
            st.write("تم تجاوز الحد التجريبي للاهتزاز.")

    else:
        st.success("✅ جميع القراءات ضمن الحدود التجريبية المحددة.")

# --- العمود الثاني: سجل القراءات ---
with col2:
    st.subheader("📋 سجل قراءات الحاجز")
    st.caption("LIVE SENSOR READINGS")
    st.caption("تتحدث القراءات تلقائيًا عند تغيير قيم المحاكاة.")

    data = {
        "المؤشر": ["الضغط", "الاهتزاز"],
        "القراءة الحالية": [
            f"{simulated_pressure:.2f} Bar",
            f"{simulated_vibration:.2f} G",
        ],
        "الحالة": [
            "🔴 تجاوز تجريبي" if pressure_alert else "🟢 ضمن النطاق",
            "🔴 تجاوز تجريبي" if vibration_alert else "🟢 ضمن النطاق",
        ],
    }

    df = pd.DataFrame(data)

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True,
        height=160,
    )

# وحدة الفحص الجنائي الرقمي للتحقق من سلامة الصوت

st.markdown("""
<div style="background:linear-gradient(135deg,#19152F,#101B2B);border:1px solid #514477;border-right:5px solid #A78BFA;border-radius:18px;padding:25px;margin:18px 0 12px 0;">
    <div style="color:#A78BFA;font-size:11px;letter-spacing:3px;font-weight:800;">DIGITAL AUDIO FORENSICS</div>
    <h2 style="color:#FFFFFF;margin:12px 0 8px 0;">🎙️ مختبر صَدَى للتحليل الصوتي</h2>
    <p style="color:#C5C5DA;font-size:14px;line-height:1.8;">فحص الخصائص الطيفية للإشارات الصوتية واستكشاف الأنماط والترددات غير المعتادة.</p>
    <div style="color:#C4B5FD;font-size:12px;">STFT ANALYSIS　 |　 AUDIO SIGNAL　 |　 SPECTRAL REVIEW</div>
</div>
""", unsafe_allow_html=True)

st.caption(
    "تحليل الخصائص الطيفية للصوت للمساعدة في فحص الإشارة "
    "ورصد الأنماط غير المعتادة."
)

st.markdown("""
<div style="background:#151D2C;border:1px solid #35445C;border-radius:15px;padding:20px;margin:16px 0 10px 0;">
    <h3 style="color:#F3F7FF;margin:0;">🎤 تسجيل عينة صوتية</h3>
    <p style="color:#9CAFC4;font-size:13px;line-height:1.8;margin-bottom:0;">اضغط على زر الميكروفون لبدء التسجيل، ثم اضغط مرة أخرى لإيقافه.</p>
</div>
""", unsafe_allow_html=True)
audio_bytes = audio_recorder(
    text="اضغطي للبدء / الإيقاف",
    recording_color="#FF6B7A",
    neutral_color="#514477",
    icon_name="microphone",
    icon_size="2x",
)

st.markdown("""
<div style="
    background:#111C2B;
    border:1px solid #293C52;
    border-radius:12px;
    padding:14px 16px;
    margin-top:12px;
    color:#B9C9D9;
    font-size:13px;
    line-height:1.9;
">
    <span style="color:#A78BFA;font-weight:800;">
        💡 طريقة الاستخدام
    </span>
    <br>
    1. ابدء التسجيل وتحدث بوضوح.
    <br>
    2. أوقف التسجيل عند الانتهاء.
    <br>
    3. انتظر ظهور الرسم الطيفي ونتائج التحليل.
</div>
""", unsafe_allow_html=True)
# 2. معالجة الصوت وعرض الموجة والترددات الحقيقية
if audio_bytes is not None and len(audio_bytes) > 0:
    st.audio(audio_bytes, format="audio/wav")

    audio_io = io.BytesIO(audio_bytes)
    y, sr = sf.read(audio_io)

    # تحويل الصوت إلى قناة واحدة عند الحاجة
    if y.ndim > 1:
        y = y.mean(axis=1)

    # التأكد من وجود بيانات صوتية
    if len(y) > 0:
        duration = len(y) / sr

        st.markdown("## 🎙️ الموجة الصوتية — Waveform")

        # عرض الموجة الصوتية مع الزمن
        step = max(1, len(y) // 12000)
        y_plot = y[::step]
        time_axis = np.arange(len(y_plot)) * step / sr

        fig1, ax1 = plt.subplots(
            figsize=(12, 3),
            facecolor="#101827",
            constrained_layout=True
        )
        ax1.set_facecolor("#101827")
        ax1.plot(time_axis, y_plot, color="#43D9D0", linewidth=0.8)
        ax1.set_title("Audio Waveform", color="white")
        ax1.set_xlabel("Time (seconds)", color="#B7C8D8")
        ax1.set_ylabel("Amplitude", color="#B7C8D8")
        ax1.tick_params(colors="#B7C8D8")
        ax1.grid(alpha=0.2)

        for spine in ax1.spines.values():
            spine.set_color("#35445C")

        st.pyplot(fig1, use_container_width=True)
        plt.close(fig1)

        # حساب طيف الترددات
        st.markdown("## 📊 طيف الترددات — Frequency Spectrum")

        spectrum = np.abs(np.fft.rfft(y))
        frequencies = np.fft.rfftfreq(len(y), d=1 / sr)

        # تجاهل التردد صفر عند تحديد أقوى تردد
        if len(spectrum) > 1:
            peak_index = np.argmax(spectrum[1:]) + 1
            peak_frequency = frequencies[peak_index]

            fig2, ax2 = plt.subplots(
                figsize=(12, 4),
                facecolor="#101827",
                constrained_layout=True
            )
            ax2.set_facecolor("#101827")
            ax2.plot(
                frequencies,
                spectrum,
                color="#A78BFA",
                linewidth=0.8
            )
            ax2.set_xlim(0, sr / 2)
            ax2.set_title("Frequency Spectrum", color="white")
            ax2.set_xlabel("Frequency (Hz)", color="#B7C8D8")
            ax2.set_ylabel("Magnitude", color="#B7C8D8")
            ax2.tick_params(colors="#B7C8D8")
            ax2.grid(alpha=0.2)

            for spine in ax2.spines.values():
                spine.set_color("#35445C")

            st.pyplot(fig2, use_container_width=True)
            plt.close(fig2)

            st.metric(
                "أقوى تردد مكتشف",
                f"{peak_frequency:.1f} Hz"
            )

        # الرسم الطيفي الذي كان موجودًا في مشروعك
        st.markdown("##  التحليل الطيفي مع الزمن")

        D = librosa.amplitude_to_db(
            np.abs(librosa.stft(y)),
            ref=np.max
        )

        fig3, ax3 = plt.subplots(
            figsize=(12, 5),
            facecolor="#101827",
            constrained_layout=True
        )
        ax3.set_facecolor("#101827")

        img = librosa.display.specshow(
            D,
            sr=sr,
            x_axis="time",
            y_axis="log",
            cmap="magma",
            ax=ax3
        )

        fig3.colorbar(img, ax=ax3, format="%+2.0f dB")
        ax3.set_title("Frequency vs Time", color="white")
        ax3.set_xlabel("Time (seconds)", color="#B7C8D8")
        ax3.set_ylabel("Frequency (Hz)", color="#B7C8D8")
        ax3.tick_params(colors="#B7C8D8")

        st.pyplot(fig3, use_container_width=True)
        plt.close(fig3)

        st.caption(f"⏱️ مدة التسجيل: {duration:.2f} ثانية")
        st.caption(f"🎚️ معدل أخذ العينات: {sr:,} Hz")

        mean_level_db = np.mean(D)

        st.metric(
            "متوسط المستوى الطيفي",
            f"{mean_level_db:.2f} dB"
        )

        st.info(
            "ℹ️ تعرض الرسوم خصائص الإشارة الصوتية المسجلة. "
            "أقوى تردد ليس بالضرورة تردد الصوت الأساسي، "
            "ولا تثبت هذه الرسوم وحدها وجود تلاعب رقمي."
        )