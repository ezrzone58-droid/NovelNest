import streamlit as st
import json
import os
import uuid
import hashlib
from datetime import datetime

# ==========================================
# 1. KONFIGURASI ENTERPRISE & KEMANAN APLIKASI
# ==========================================
st.set_page_config(
    page_title="NovelNest Enterprise - Core Web Edition",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

FILE_DATABASE = "novelnest_data.json"
SYSTEM_VERSION = "4.2.0-Enterprise"

# ==========================================
# 2. SISTEM DATABASE CORE & ATOMIC WRITE (JSON)
# ==========================================
def hash_password(password: str) -> str:
    """Menghasilkan enkripsi SHA-256 untuk password agar aman."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def muat_data() -> dict:
    """Memuat database dengan penanganan struktur fail-safe enterprise."""
    default_db = {
        "tema": "biru",
        "daftar_novel": [],
        "antrian_registrasi": [],
        "users_terdaftar": {
            "admin": hash_password("admin")
        },
        "active_sessions": {},
        "system_logs": []
    }
    
    if os.path.exists(FILE_DATABASE):
        try:
            with open(FILE_DATABASE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Validasi integritas skema data minimum
                for key in default_db:
                    if key not in data:
                        data[key] = default_db[key]
                return data
        except Exception as e:
            st.error(f"[CRITICAL ERROR] Gagal mengurai Database JSON: {e}")
    
    # Inisialisasi file baru jika belum ada
    simpan_data(default_db)
    return default_db

def simpan_data(data: dict) -> bool:
    """Menyimpan data dengan metode Atomic Write untuk mencegah korupsi file."""
    temp_file = f"{FILE_DATABASE}.tmp"
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        if os.path.exists(FILE_DATABASE):
            os.replace(temp_file, FILE_DATABASE)
        else:
            os.rename(temp_file, FILE_DATABASE)
        return True
    except Exception as e:
        st.error(f"[TRANSACTION ERROR] Gagal menulis database: {e}")
        if os.path.exists(temp_file):
            os.remove(temp_file)
        return False

def catat_log(aktivitas: str, aktor: str = "System"):
    """Mencatat aktivitas sistem (Audit Trail)."""
    if "db" in st.session_state:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{aktor.upper()}] {aktivitas}"
        st.session_state.db.setdefault("system_logs", []).append(log_entry)
        # Batasi log maksimal 100 catatan terakhir
        if len(st.session_state.db["system_logs"]) > 100:
            st.session_state.db["system_logs"] = st.session_state.db["system_logs"][-100:]
        simpan_data(st.session_state.db)

# ==========================================
# 3. INISIALISASI SESSION STATE & KEAMANAN SESI
# ==========================================
if "db" not in st.session_state:
    st.session_state.db = muat_data()

db = st.session_state.db

# Device Token Tracking untuk Sesi Mandiri Tanpa Login Ulang
if "device_token" not in st.session_state:
    params = st.query_params
    if "token" in params:
        st.session_state.device_token = params["token"]
    else:
        new_token = str(uuid.uuid4())
        st.session_state.device_token = new_token
        st.query_params["token"] = new_token

active_sessions = db.get("active_sessions", {})
current_device_token = st.session_state.device_token

if current_device_token in active_sessions:
    st.session_state.logged_in_user = active_sessions[current_device_token]
else:
    st.session_state.logged_in_user = None

# Default State Variables
state_defaults = {
    "menu": "Utama",
    "selected_novel": None,
    "selected_bab": None,
    "is_admin": False,
    "admin_step": 0,
    "show_theme_modal": False,
    "aktivasi_step": "input_id",
    "temp_validated_id": ""
}

for key, val in state_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ==========================================
# 4. MANAJEMEN TEMA & ENTERPRISE UI STYLING
# ==========================================
tema = db.get("tema", "biru")

theme_configs = {
    "merah": {"bg": "#121212", "text": "#f3f4f6", "btn": "#dc2626", "box": "#27272a"},
    "hijau": {"bg": "#f0fdf4", "text": "#022c22", "btn": "#059669", "box": "#d1fae5"},
    "ungu": {"bg": "#faf5ff", "text": "#2e1065", "btn": "#7c3aed", "box": "#f3e8ff"},
    "biru": {"bg": "#f4f6f8", "text": "#0f172a", "btn": "#2563eb", "box": "#e2e8f0"}
}

cfg = theme_configs.get(tema, theme_configs["biru"])

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {cfg['bg']};
        color: {cfg['text']};
        font-family: 'Inter', 'Segoe UI', -apple-system, sans-serif;
    }}
    div.stButton > button {{
        background-color: {cfg['btn']};
        color: white;
        border-radius: 6px;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        width: 100%;
        transition: opacity 0.2s ease;
    }}
    div.stButton > button:hover {{
        opacity: 0.85;
    }}
    /* Kolom Input & Textarea Kontras Tinggi */
    input, textarea, div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea {{
        background-color: #ffffff !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        border-radius: 6px !important;
        border: 2px solid {cfg['btn']} !important;
        font-weight: 600 !important;
    }}
    input::placeholder, textarea::placeholder {{
        color: #4b5563 !important;
        opacity: 1 !important;
    }}
    div[data-baseweb="select"] > div {{
        background-color: #ffffff !important;
        color: #000000 !important;
        border-radius: 6px !important;
        border: 2px solid {cfg['btn']} !important;
        font-weight: 600 !important;
    }}
    div[data-baseweb="select"] span {{
        color: #000000 !important;
    }}
    p, span, label, h1, h2, h3, h4 {{
        color: {cfg['text']} !important;
    }}
    .enterprise-footer {{
        margin-top: 50px;
        text-align: center;
        font-size: 11px;
        opacity: 0.6;
        border-top: 1px solid rgba(0,0,0,0.1);
        padding-top: 15px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# 5. ROUTING APLIKASI BERDASARKAN OTORISASI
# ==========================================

if st.session_state.is_admin:
    # ----------------------------------------------------
    # DASHBOARD ADMIN ENTERPRISE
    # ----------------------------------------------------
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #1e293b, #0f172a); padding: 25px; border-radius: 10px; color: white; margin-bottom: 25px; border-left: 6px solid #3b82f6;">
            <h1 style="color: #ffffff !important; margin: 0; font-size: 28px;">🔐 Enterprise Control Center — Administrator</h1>
            <p style="color: #94a3b8 !important; margin: 5px 0 0 0;">Sistem Manajemen Terpusat NovelNest — Keamanan Tingkat Tinggi</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_adm_ctrl1, col_adm_ctrl2 = st.columns(2)
    with col_adm_ctrl1:
        if st.button("🚪 Keluar Sepenuhnya dari Admin"):
            catat_log("Administrator keluar dari panel kontrol.", "Admin")
            st.session_state.is_admin = False
            st.success("Berhasil keluar dari mode admin.")
            st.rerun()
    with col_adm_ctrl2:
        if st.button("🔄 Sinkronisasi Database (Refresh)"):
            st.session_state.db = muat_data()
            st.success("Database berhasil disinkronkan!")
            st.rerun()

    st.markdown("---")

    tab_a, tab_b, tab_c, tab_d = st.tabs([
        "📚 Manajemen Novel", 
        "📖 Manajemen Bab", 
        "👥 Otorisasi & Antrean",
        "📊 System Audit Logs"
    ])

    with tab_a:
        st.subheader("Tambah Publikasi Novel Baru")
        with st.form("tambah_novel_form"):
            jdl = st.text_input("Judul Novel Resmi")
            gnr = st.text_input("Genre & Sinopsis Singkat")
            if st.form_submit_button("Publikasikan Novel"):
                if jdl.strip() and gnr.strip():
                    db["daftar_novel"].append({"judul": jdl.strip(), "genre": gnr.strip(), "babad": []})
                    simpan_data(db)
                    catat_log(f"Menambahkan novel baru: {jdl}", "Admin")
                    st.success("Novel baru berhasil dipublikasikan.")
                    st.rerun()
                else:
                    st.warning("Judul dan genre wajib diisi secara valid.")

        fn_col1, fn_col2 = st.columns([3, 1])
        fn_col1.subheader("Daftar Inventaris Novel")
        if not db["daftar_novel"]:
            st.info("Belum ada inventaris novel di database.")
        else:
            for idx, nov in enumerate(db["daftar_novel"]):
                c1, c2 = st.columns([3, 1])
                c1.write(f"**{nov['judul']}** [{nov['genre']}]")
                if c2.button("Hapus Novel", key=f"hapus_nov_{idx}"):
                    catat_log(f"Menghapus novel: {nov['judul']}", "Admin")
                    db["daftar_novel"].remove(nov)
                    simpan_data(db)
                    st.rerun()

    with tab_b:
        st.subheader("Manajemen Bab & Konten Cerita")
        if not db["daftar_novel"]:
            st.info("Belum ada novel tersedia untuk diberi bab.")
        else:
            pilih_nov_nama = st.selectbox("Pilih Novel Target", [n["judul"] for n in db["daftar_novel"]])
            target_n = next(n for n in db["daftar_novel"] if n["judul"] == pilih_nov_nama)
            
            if not target_n["babad"]:
                st.caption("Novel ini belum memiliki bab cerita.")
            else:
                for b_idx, b_item in enumerate(target_n["babad"]):
                    with st.expander(f"Edit: {b_item['nama_bab']}"):
                        with st.form(f"form_edit_bab_{b_idx}"):
                            edit_nama_b = st.text_input("Judul Bab", value=b_item['nama_bab'])
                            edit_isi_b = st.text_area("Isi Konten Bab", value=b_item['isi'], height=150)
                            
                            col_b1, col_b2 = st.columns(2)
                            if col_b1.form_submit_button("Simpan Perubahan"):
                                if edit_nama_b and edit_isi_b:
                                    b_item['nama_bab'] = edit_nama_b
                                    b_item['isi'] = edit_isi_b
                                    simpan_data(db)
                                    catat_log(f"Mengubah bab {edit_nama_b} pada {target_n['judul']}", "Admin")
                                    st.success("Bab berhasil diperbarui.")
                                    st.rerun()
                                else:
                                    st.warning("Data tidak boleh kosong.")
                            if col_b2.form_submit_button("Hapus Bab"):
                                target_n['babad'].remove(b_item)
                                simpan_data(db)
                                catat_log(f"Menghapus bab dari {target_n['judul']}", "Admin")
                                st.success("Bab berhasil dihapus.")
                                st.rerun()

            st.markdown("---")
            with st.form("tambah_bab_form"):
                st.subheader("Tambah Bab Baru")
                nama_b = st.text_input("Nama Bab (Contoh: Bab 1 — Permulaan)")
                isi_b = st.text_area("Teks Narasi / Isi Bab", height=150)
                if st.form_submit_button("Unggah Bab"):
                    if nama_b.strip() and isi_b.strip():
                        target_n["babad"].append({"nama_bab": nama_b.strip(), "isi": isi_b.strip(), "komentar": [], "balasan": []})
                        simpan_data(db)
                        catat_log(f"Menambahkan {nama_b} ke {target_n['judul']}", "Admin")
                        st.success("Bab berhasil diunggah.")
                        st.rerun()
                    else:
                        st.warning("Nama bab dan konten wajib diisi.")

    with tab_c:
        col_head_a, col_head_b = st.columns([3, 1])
        col_head_a.subheader("Antrean Pendaftaran Akun")
        if col_head_b.button("🔄 Refresh Antrean"):
            st.session_state.db = muat_data()
            st.rerun()

        if not db["antrian_registrasi"]:
            st.info("Tidak ada antrean registrasi pending.")
        else:
            if st.button("🗑️ Bersihkan Semua Antrean"):
                db["antrian_registrasi"] = []
                simpan_data(db)
                catat_log("Membersihkan seluruh antrean registrasi", "Admin")
                st.success("Antrean dibersihkan.")
                st.rerun()
            st.markdown("---")

            for q_idx, req in enumerate(db["antrian_registrasi"]):
                col_1, col_2, col_3 = st.columns([2, 1, 1])
                col_1.write(f"ID Pengguna: **{req['id']}**")
                kode_inputan = col_2.text_input("Kode Verifikasi", value=req.get("kode", ""), key=f"q_kode_{q_idx}")
                if col_3.button("Kirim Kode", key=f"btn_q_{q_idx}"):
                    req["kode"] = kode_inputan
                    simpan_data(db)
                    catat_log(f"Mengirim kode verifikasi ke ID: {req['id']}", "Admin")
                    st.success("Kode dikirim.")
                    st.rerun()
                st.markdown("---")

        st.subheader("Database Pengguna Terdaftar")
        active_users = {k: v for k, v in db["users_terdaftar"].items() if k != "admin"}
        if not active_users:
            st.info("Belum ada pengguna terdaftar.")
        else:
            for usr in active_users:
                col_u1, col_u2, col_u3 = st.columns([2, 1, 1])
                col_u1.write(f"- Username: **{usr}**")
                new_pwd_input = col_u2.text_input("Reset Sandi", type="password", key=f"reset_pwd_{usr}")
                if col_u2.button("Reset", key=f"btn_reset_{usr}"):
                    if new_pwd_input.strip():
                        db["users_terdaftar"][usr] = hash_password(new_pwd_input.strip())
                        simpan_data(db)
                        catat_log(f"Reset password untuk user: {usr}", "Admin")
                        st.success(f"Sandi {usr} direset.")
                        st.rerun()
                    else:
                        st.warning("Masukkan sandi baru.")
                if col_u3.button("Cabut Akses", key=f"btn_del_usr_{usr}"):
                    del db["users_terdaftar"][usr]
                    simpan_data(db)
                    catat_log(f"Mencabut akses user: {usr}", "Admin")
                    st.success(f"Akun {usr} dihapus.")
                    st.rerun()

    with tab_d:
        st.subheader("Log Keamanan & Aktivitas Sistem")
        logs = db.get("system_logs", [])
        if not logs:
            st.info("Belum ada catatan log sistem.")
        else:
            for log in reversed(logs):
                st.code(log, language="text")

else:
    # ----------------------------------------------------
    # APLIKASI UTAMA PENGGUNA (LANDING & FITUR)
    # ----------------------------------------------------
    
    # 1. TOMBOL SETTING (KIRI ATAS) & MENU POPUP
    col_top_left, col_top_right = st.columns([1, 10])
    with col_top_left:
        if st.button("⚙️", help="Pengaturan Tema Sistem"):
            st.session_state.show_theme_modal = not st.session_state.show_theme_modal
            st.rerun()

    if st.session_state.show_theme_modal:
        st.markdown("### 🎨 Pengaturan Tampilan Enterprise")
        pilihan_tema = st.selectbox(
            "Pilih Tema Warna Korporat",
            ["biru", "merah", "hijau", "ungu"],
            index=["biru", "merah", "hijau", "ungu"].index(tema)
        )
        if pilihan_tema != tema:
            db["tema"] = pilihan_tema
            simpan_data(db)
            catat_log(f"Mengubah tema visual sistem ke {pilihan_tema}", "User")
            st.rerun()
        st.markdown("---")

    # A. HALAMAN UTAMA (LANDING PAGE)
    if st.session_state.menu == "Utama":
        st.markdown(
            f"""
            <div style="text-align: center; padding: 40px 20px 20px 20px;">
                <h1 style="font-weight: 800; font-size: 52px; margin-bottom: 10px; letter-spacing: -1px;">NovelNest</h1>
                <p style="font-size: 18px; font-style: italic; opacity: 0.8; max-width: 650px; margin: 0 auto 40px auto; line-height: 1.6;">
                    Enterprise-grade digital publishing platform. Rumah digital bagi para pembaca untuk menikmati literatur berkualitas tinggi dengan sistem verifikasi berlapis.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Tombol Masuk & Registrasi: Sejajar, Tengah, Ukuran Sama
        col_space_l, col_btn1, col_btn2, col_space_r = st.columns([1.5, 2, 2, 1.5])
        with col_btn1:
            if st.button("🔑 Masuk", use_container_width=True):
                st.session_state.menu = "Login"
                st.rerun()
        with col_btn2:
            if st.button("📝 Registrasi", use_container_width=True):
                st.session_state.menu = "Registrasi"
                st.rerun()

    # B. HALAMAN LOGIN KORPORAT
    elif st.session_state.menu == "Login":
        if st.button("← Kembali ke Beranda Utama"):
            st.session_state.menu = "Utama"
            st.session_state.admin_step = 0
            st.rerun()

        st.title("Autentikasi Akun Pengguna")

        if st.session_state.logged_in_user:
            st.info(f"Sesi aktif terdeteksi sebagai **{st.session_state.logged_in_user}**.")
            if st.button("🚀 Masuk ke Pustaka Novel", use_container_width=True):
                st.session_state.menu = "Koleksi Novel"
                st.rerun()
            if st.button("🚪 Keluar Akun (Logout)", use_container_width=True):
                catat_log(f"User {st.session_state.logged_in_user} logout", "User")
                if current_device_token in db.get("active_sessions", {}):
                    del db["active_sessions"][current_device_token]
                    simpan_data(db)
                st.session_state.logged_in_user = None
                st.rerun()
        else:
            if st.session_state.admin_step == 1:
                st.info("Otorisasi Administratif Lapis 1 Diperlukan.")
                with st.form("form_verif_1"):
                    v1 = st.text_input("Kunci Enskripsi Lapis 1:", type="password")
                    if st.form_submit_button("Otorisasi Lanjut"):
                        if v1 == "123":
                            st.session_state.admin_step = 2
                            st.rerun()
                        else:
                            st.error("Kunci lapis 1 tidak valid.")
                            st.session_state.admin_step = 0

            elif st.session_state.admin_step == 2:
                st.info("Otorisasi Administratif Lapis 2 Diperlukan.")
                with st.form("form_verif_2"):
                    v2 = st.text_input("Kunci Enskripsi Lapis 2:", type="password")
                    if st.form_submit_button("Akses Sistem Admin"):
                        if v2 == "321":
                            st.session_state.is_admin = True
                            st.session_state.admin_step = 0
                            catat_log("Akses Administrator berhasil dibuka", "Security")
                            st.success("Otorisasi sukses! Memuat Enterprise Dashboard...")
                            st.rerun()
                        else:
                            st.error("Kunci lapis 2 tidak valid.")
                            st.session_state.admin_step = 0

            else:
                with st.form("form_user_login"):
                    u_name = st.text_input("Username Korporat / Pengguna")
                    u_pass = st.text_input("Kata Sandi", type="password")
                    
                    if st.form_submit_button("Autentikasi Masuk"):
                        if u_name == "admin" and u_pass == "admin":
                            st.session_state.admin_step = 1
                            st.rerun()
                        else:
                            registered = db["users_terdaftar"]
                            hashed_input = hash_password(u_pass)
                            if u_name in registered and registered[u_name] == hashed_input:
                                st.session_state.logged_in_user = u_name
                                db.setdefault("active_sessions", {})[current_device_token] = u_name
                                simpan_data(db)
                                catat_log(f"User {u_name} berhasil login", "User")
                                st.success(f"Autentikasi berhasil. Selamat datang, {u_name}.")
                                st.rerun()
                            else:
                                st.error("Kredensial akses tidak dikenali.")

    # C. HALAMAN REGISTRASI & AKTIVASI BERTAHAP
    elif st.session_state.menu == "Registrasi":
        if st.button("← Kembali ke Beranda Utama"):
            st.session_state.menu = "Utama"
            st.rerun()

        st.title("Portal Pendaftaran & Aktivasi Pengguna")
        st.markdown("Proses pendaftaran terintegrasi dengan verifikasi ID Pengguna unik.")

        t_reg1, t_reg2 = st.tabs(["1. Pengajuan ID Pengguna", "2. Aktivasi & Profiling"])

        with t_reg1:
            st.subheader("Pengajuan ID Pengguna Korporat")
            st.write("Masukkan ID Pengguna unik Anda (Gunakan nama samaran/ID operasional, hindari informasi sensitif).")

            col_r_left, col_r_right = st.columns([2, 1])
            with col_r_left:
                with st.form("form_ajukan_id"):
                    id_temp = st.text_input("ID Pengguna Unik:")
                    
                    col_btn_sub, col_btn_res = st.columns(2)
                    sub_pengajuan = col_btn_sub.form_submit_button("Ajukan ID")
                    btn_restart_code = col_btn_res.form_submit_button("🔄 Muat Ulang Kode")

                    if sub_pengajuan:
                        if not id_temp.strip():
                            st.warning("ID Pengguna tidak boleh kosong.")
                        else:
                            found_req = next((x for x in db["antrian_registrasi"] if x["id"] == id_temp.strip()), None)
                            if found_req:
                                st.info("ID Pengguna ini sudah tercatat dalam antrean pending.")
                            else:
                                db["antrian_registrasi"].append({"id": id_temp.strip(), "kode": "", "username": "", "password": ""})
                                simpan_data(db)
                                catat_log(f"Pengajuan ID baru: {id_temp.strip()}", "Registration")
                                st.success("Pengajuan berhasil dimasukkan ke antrean verifikasi.")
                                st.rerun()

                    if btn_restart_code:
                        st.session_state.db = muat_data()
                        st.success("Status antrean berhasil disinkronkan!")
                        st.rerun()

            with col_r_right:
                st.markdown("#### Status Sistem")
                st.markdown(
                    f"""
                    <div style="background-color: {cfg['box']}; padding: 12px; border-radius: 6px; margin-bottom: 10px;">
                        <span style="font-size: 12px; font-weight: bold;">Total Antrean Menunggu:</span><br>
                        <span style="font-size: 20px; font-weight: bold;">{len(db['antrian_registrasi'])}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"""
                    <div style="background-color: {cfg['box']}; padding: 12px; border-radius: 6px;">
                        <span style="font-size: 12px; font-weight: bold;">Catatan Keamanan:</span><br>
                        <span style="font-size: 13px;">Gunakan tombol muat ulang untuk memeriksa ketersediaan kode verifikasi dari administrator.</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with t_reg2:
            st.subheader("Aktivasi Akun & Konfigurasi Profil")

            if st.session_state.aktivasi_step == "input_id":
                st.write("Masukkan ID Pengguna yang telah divalidasi dan dikirimi kode verifikasi oleh administrator.")
                with st.form("form_cek_id_aktivasi"):
                    check_id = st.text_input("ID Pengguna Terdaftar:")
                    if st.form_submit_button("Verifikasi ID"):
                        target_q = next((x for x in db["antrian_registrasi"] if x["id"] == check_id.strip()), None)
                        if target_q and target_q.get("kode"):
                            st.session_state.temp_validated_id = check_id.strip()
                            st.session_state.aktivasi_step = "konfirmasi_id"
                            st.rerun()
                        else:
                            st.error("ID tidak ditemukan atau kode verifikasi belum diotorisasi oleh admin.")

            elif st.session_state.aktivasi_step == "konfirmasi_id":
                st.warning(f"Konfirmasi integritas: Apakah Anda yakin ID Pengguna **'{st.session_state.temp_validated_id}'** sudah benar?")
                col_konf1, col_konf2 = st.columns(2)
                if col_konf1.button("Ya, Benar", use_container_width=True):
                    st.session_state.aktivasi_step = "form_profil"
                    st.rerun()
                if col_konf2.button("Tidak, Ulangi", use_container_width=True):
                    st.session_state.temp_validated_id = ""
                    st.session_state.aktivasi_step = "input_id"
                    st.rerun()

            elif st.session_state.aktivasi_step == "form_profil":
                st.info("Buat kredensial Username dan Password permanen untuk akses penuh sistem.")
                target_q = next((x for x in db["antrian_registrasi"] if x["id"] == st.session_state.temp_validated_id), None)
                
                with st.form("form_aktivasi_profil_final"):
                    inp_kode = st.text_input("Kode Verifikasi Admin:")
                    inp_new_u = st.text_input("Username Permanen:")
                    inp_new_p = st.text_input("Kata Sandi Aman:", type="password")

                    if st.form_submit_button("Aktifkan Akun"):
                        if not target_q or target_q.get("kode") != inp_kode.strip():
                            st.error("Kode verifikasi salah.")
                        elif inp_new_u.strip() in db["users_terdaftar"]:
                            st.error("Username tersebut sudah digunakan dalam sistem.")
                        else:
                            db["users_terdaftar"][inp_new_u.strip()] = hash_password(inp_new_p.strip())
                            db["antrian_registrasi"].remove(target_q)
                            simpan_data(db)
                            
                            catat_log(f"Akun baru berhasil diaktifkan: {inp_new_u.strip()}", "Registration")
                            st.session_state.aktivasi_step = "input_id"
                            st.session_state.temp_validated_id = ""
                            st.session_state.menu = "Login"
                            st.success("Akun berhasil diaktifkan! Mengalihkan ke portal login...")
                            st.rerun()

    # D. KOLEKSI NOVEL & PUSTAKA BACAAN
    elif st.session_state.menu == "Koleksi Novel":
        if st.button("← Keluar ke Beranda Utama"):
            st.session_state.menu = "Utama"
            st.rerun()

        if not st.session_state.logged_in_user:
            st.warning("Autentikasi diperlukan. Silakan masuk melalui portal login.")
            if st.button("Pindah ke Halaman Login"):
                st.session_state.menu = "Login"
                st.rerun()
        else:
            st.title("NovelNest Enterprise Library")
            st.markdown(f"Status Sesi Aktif: **{st.session_state.logged_in_user}**")
            st.markdown("---")

            if st.session_state.selected_novel is None:
                st.subheader("Pilih Karya Literatur Tersedia:")
                if not db["daftar_novel"]:
                    st.info("Belum ada publikasi novel di perpustakaan.")
                else:
                    for idx_n, n_item in enumerate(db["daftar_novel"]):
                        if st.button(f"📖 {n_item['judul']} — [{n_item['genre']}]", key=f"pilih_n_{idx_n}", use_container_width=True):
                            st.session_state.selected_novel = n_item
                            st.rerun()
            else:
                current_novel = st.session_state.selected_novel
                if st.button("Kembali ke Daftar Pustaka"):
                    st.session_state.selected_novel = None
                    st.session_state.selected_bab = None
                    st.rerun()

                if st.session_state.selected_bab is None:
                    st.title(f"📚 {current_novel['judul']}")
                    st.markdown(f"**Sinopsis / Genre:** {current_novel['genre']}")
                    st.markdown("---")
                    st.subheader("Daftar Bab Publikasi")
                    if not current_novel["babad"]:
                        st.info("Bab cerita belum dirilis untuk novel ini.")
                    else:
                        for idx_b, b_item in enumerate(current_novel["babad"]):
                            if st.button(f"📄 {b_item['nama_bab']}", key=f"buka_b_{idx_b}"):
                                st.session_state.selected_bab = b_item
                                st.rerun()
                else:
                    current_bab = st.session_state.selected_bab
                    if st.button("Kembali ke Daftar Bab"):
                        st.session_state.selected_bab = None
                        st.rerun()

                    st.markdown(f"### {current_novel['judul']} — {current_bab['nama_bab']}")
                    st.markdown("---")
                    st.markdown(
                        f"""
                        <div style="background-color: {cfg['box']}; color: {cfg['text']}; padding: 30px; border-radius: 8px; line-height: 1.8; white-space: pre-wrap; font-weight: 500; font-size: 16px;">
{current_bab['isi']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown("---")
                    st.subheader("Diskusi & Ulasan Pembaca")

                    if "komentar" not in current_bab:
                        current_bab["komentar"] = []

                    with st.form("form_tambah_komentar"):
                        isi_komentar = st.text_area("Tulis ulasan atau tanggapan Anda...")
                        if st.form_submit_button("Kirim Komentar"):
                            if isi_komentar.strip():
                                current_bab["komentar"].append({
                                    "user": st.session_state.logged_in_user,
                                    "pesan": isi_komentar.strip(),
                                    "balasan": []
                                })
                                simpan_data(db)
                                st.success("Komentar terkirim.")
                                st.rerun()
                            else:
                                st.warning("Komentar tidak boleh kosong.")

                    if not current_bab["komentar"]:
                        st.info("Belum ada ulasan pada bab ini.")
                    else:
                        for idx_k, kom in enumerate(current_bab["komentar"]):
                            if "balasan" not in kom:
                                kom["balasan"] = []
                            st.markdown(
                                f"""
                                <div style="background-color: {cfg['box']}; padding: 12px; border-radius: 6px; margin-bottom: 10px;">
                                    <strong>{kom['user']}</strong><br>{kom['pesan']}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            for bal in kom["balasan"]:
                                st.markdown(
                                    f"""
                                    <div style="background-color: rgba(0,0,0,0.05); padding: 8px 10px; border-radius: 6px; margin-left: 30px; margin-bottom: 6px; border-left: 3px solid {cfg['btn']};">
                                        <span style="font-size: 13px;">↳ <strong>{bal['user']}</strong>: {bal['pesan']}</span>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                            with st.form(f"form_balas_{idx_k}"):
                                pesan_balasan = st.text_input("Balas ulasan ini...", key=f"input_balas_{idx_k}")
                                if st.form_submit_button("Kirim Balasan"):
                                    if pesan_balasan.strip():
                                        kom["balasan"].append({
                                            "user": st.session_state.logged_in_user,
                                            "pesan": pesan_balasan.strip()
                                        })
                                        simpan_data(db)
                                        st.success("Balasan terkirim.")
                                        st.rerun()
                                    else:
                                        st.warning("Balasan kosong.")
                            st.markdown("---")

# ==========================================
# 6. FOOTER KORPORAT
# ==========================================
st.markdown(
    f"""
    <div class="enterprise-footer">
        NovelNest Core System &bull; Version {SYSTEM_VERSION} &bull; Secured Enterprise Architecture &bull; All Transactions Synchronized
    </div>
    """,
    unsafe_allow_html=True
)
