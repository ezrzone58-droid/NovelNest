import streamlit as st
import json
import os
import uuid
import hashlib
from datetime import datetime

# ==============================================================================
# 1. ENTERPRISE SYSTEM CONFIGURATION & SECURITY ARCHITECTURE
# ==============================================================================
st.set_page_config(
    page_title="NovelNest Enterprise Suite",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

FILE_DATABASE = "novelnest_data.json"
SYSTEM_VERSION = "5.0.0-CorporateElite"

def hash_secure(password: str) -> str:
    """Implementasi SHA-256 Hashing lapis korporat untuk proteksi kredensial."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def load_enterprise_database() -> dict:
    """Memuat database JSON dengan skema fail-safe dan auto-recovery."""
    default_schema = {
        "tema": "modern_corporate",
        "daftar_novel": [],
        "antrian_registrasi": [],
        "users_terdaftar": {
            "admin": hash_secure("admin")
        },
        "active_sessions": {},
        "audit_logs": []
    }
    
    if os.path.exists(FILE_DATABASE):
        try:
            with open(FILE_DATABASE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for key in default_schema:
                    if key not in data:
                        data[key] = default_schema[key]
                return data
        except Exception as e:
            st.error(f"[FATAL ERROR] Gagal mendekripsi struktur database: {e}")
    
    save_enterprise_database(default_schema)
    return default_schema

def save_enterprise_database(data: dict) -> bool:
    """Metode Atomic Write untuk menjamin integritas transaksi data JSON."""
    temp_target = f"{FILE_DATABASE}.tmp"
    try:
        with open(temp_target, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        if os.path.exists(FILE_DATABASE):
            os.replace(temp_target, FILE_DATABASE)
        else:
            os.rename(temp_target, FILE_DATABASE)
        return True
    except Exception as e:
        st.error(f"[TRANSACTION FAILED] Gagal menulis sinkronisasi data: {e}")
        if os.path.exists(temp_target):
            os.remove(temp_target)
        return False

def record_audit_trail(action: str, actor: str = "System"):
    """Pencatatan log aktivitas sistem (Audit Trail) terpusat."""
    if "db" in st.session_state:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_string = f"[{timestamp}] [{actor.upper()}] {action}"
        st.session_state.db.setdefault("audit_logs", []).append(log_string)
        if len(st.session_state.db["audit_logs"]) > 150:
            st.session_state.db["audit_logs"] = st.session_state.db["audit_logs"][-150:]
        save_enterprise_database(st.session_state.db)

# ==============================================================================
# 2. SESSION STATE & TOKEN MANAGEMENT
# ==============================================================================
if "db" not in st.session_state:
    st.session_state.db = load_enterprise_database()

db = st.session_state.db

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

state_defaults = {
    "menu": "Utama",
    "selected_novel": None,
    "selected_bab": None,
    "is_admin": False,
    "admin_step": 0,
    "show_settings_panel": False,
    "aktivasi_step": "input_id",
    "temp_validated_id": ""
}

for k, v in state_defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ==============================================================================
# 3. ADVANCED UI THEME ENGINE & DESIGN SYSTEM (CSS3 / HTML5)
# ==============================================================================
tema = db.get("tema", "modern_corporate")

theme_palettes = {
    "modern_corporate": {
        "bg_main": "#0f172a", "bg_surface": "#1e293b", "text_primary": "#f8fafc", 
        "text_secondary": "#94a3b8", "accent": "#3b82f6", "accent_hover": "#2563eb",
        "border": "#334155", "card_bg": "#1e293b", "shadow": "0 10px 25px -5px rgba(0, 0, 0, 0.3)"
    },
    "clean_light": {
        "bg_main": "#f8fafc", "bg_surface": "#ffffff", "text_primary": "#0f172a", 
        "text_secondary": "#64748b", "accent": "#2563eb", "accent_hover": "#1d4ed8",
        "border": "#e2e8f0", "card_bg": "#ffffff", "shadow": "0 10px 25px -5px rgba(0, 0, 0, 0.05)"
    },
    "emerald_executive": {
        "bg_main": "#022c22", "bg_surface": "#064e3b", "text_primary": "#ecfdf5", 
        "text_secondary": "#a7f3d0", "accent": "#059669", "accent_hover": "#047857",
        "border": "#065f46", "card_bg": "#064e3b", "shadow": "0 10px 25px -5px rgba(2, 44, 34, 0.5)"
    },
    "royal_purple": {
        "bg_main": "#2e1065", "bg_surface": "#3b0764", "text_primary": "#faf5ff", 
        "text_secondary": "#e9d5ff", "accent": "#7c3aed", "accent_hover": "#6d28d9",
        "border": "#581c87", "card_bg": "#3b0764", "shadow": "0 10px 25px -5px rgba(46, 16, 101, 0.5)"
    }
}

p = theme_palettes.get(tema, theme_palettes["modern_corporate"])

st.markdown(
    f"""
    <style>
    /* Global Reset & Typography */
    .stApp {{
        background-color: {p['bg_main']};
        color: {p['text_primary']};
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }}
    
    /* Tombol Interaktif Profesional */
    div.stButton > button {{
        background-color: {p['accent']} !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 0.65rem 1.25rem !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
    }}
    div.stButton > button:hover {{
        background-color: {p['accent_hover']} !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
    }}

    /* Input & Textarea Korporat Berstandar Tinggi */
    input, textarea, div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea {{
        background-color: {p['bg_surface']} !important;
        color: {p['text_primary']} !important;
        -webkit-text-fill-color: {p['text_primary']} !important;
        border-radius: 8px !important;
        border: 1px solid {p['border']} !important;
        padding: 0.75rem 1rem !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }}
    input:focus, textarea:focus, div[data-baseweb="input"]:focus-within {{
        border-color: {p['accent']} !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
    }}
    input::placeholder, textarea::placeholder {{
        color: {p['text_secondary']} !important;
        opacity: 0.7 !important;
    }}

    /* Dropdown / Selectbox Styling */
    div[data-baseweb="select"] > div {{
        background-color: {p['bg_surface']} !important;
        color: {p['text_primary']} !important;
        border-radius: 8px !important;
        border: 1px solid {p['border']} !important;
    }}
    div[data-baseweb="select"] span {{
        color: {p['text_primary']} !important;
    }}

    /* Komponen Kartu dan Kontainer Profesional */
    .corporate-card {{
        background-color: {p['card_bg']};
        border: 1px solid {p['border']};
        border-radius: 12px;
        padding: 24px;
        box-shadow: {p['shadow']};
        margin-bottom: 20px;
    }}

    .hero-container {{
        text-align: center;
        padding: 60px 20px 30px 20px;
    }}

    .hero-title {{
        font-weight: 800;
        font-size: 52px;
        letter-spacing: -1.5px;
        color: {p['text_primary']};
        margin-bottom: 15px;
    }}

    .hero-subtitle {{
        font-size: 17px;
        color: {p['text_secondary']};
        max-width: 650px;
        margin: 0 auto 40px auto;
        line-height: 1.6;
    }}

    /* Footer Korporat */
    .enterprise-footer {{
        margin-top: 60px;
        text-align: center;
        font-size: 12px;
        color: {p['text_secondary']};
        border-top: 1px solid {p['border']};
        padding-top: 20px;
        opacity: 0.8;
    }}

    p, span, label, h1, h2, h3, h4 {{
        color: {p['text_primary']} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================================================================
# 4. KONTROL ROUTING APLIKASI UTAMA
# ==============================================================================

if st.session_state.is_admin:
    # --------------------------------------------------------------------------
    # ADMIN ENTERPRISE CONTROL CENTER
    # --------------------------------------------------------------------------
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, {p['bg_surface']}, {p['bg_main']}); padding: 30px; border-radius: 14px; border: 1px solid {p['border']}; margin-bottom: 30px; box-shadow: {p['shadow']};">
            <h1 style="margin: 0; font-size: 28px; font-weight: 700;">🔐 Enterprise Admin Control Center</h1>
            <p style="margin: 6px 0 0 0; color: {p['text_secondary']};">Manajemen Terpusat Infrastruktur NovelNest & Keamanan Sesi</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_adm_ctrl1, col_adm_ctrl2 = st.columns(2)
    with col_adm_ctrl1:
        if st.button("🚪 Keluar dari Mode Admin"):
            record_audit_trail("Administrator keluar dari Control Center", "Admin")
            st.session_state.is_admin = False
            st.success("Sesi admin berhasil diakhiri.")
            st.rerun()
    with col_adm_ctrl2:
        if st.button("🔄 Sinkronisasi Database Pusat"):
            st.session_state.db = load_enterprise_database()
            st.success("Database berhasil disegarkan dari memori.")
            st.rerun()

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    tab_a, tab_b, tab_c, tab_d = st.tabs([
        "📚 Inventaris Novel", 
        "📖 Manajemen Bab", 
        "👥 Otorisasi Pengguna",
        "📊 Sistem Audit Logs"
    ])

    with tab_a:
        st.markdown("### Publikasi Novel Baru")
        with st.form("tambah_novel_form"):
            jdl = st.text_input("Judul Novel Resmi")
            gnr = st.text_input("Genre & Deskripsi Profesional")
            if st.form_submit_button("Publikasikan ke Sistem"):
                if jdl.strip() and gnr.strip():
                    db["daftar_novel"].append({"judul": jdl.strip(), "genre": gnr.strip(), "babad": []})
                    save_enterprise_database(db)
                    record_audit_trail(f"Publikasi novel baru: {jdl}", "Admin")
                    st.success("Novel berhasil ditambahkan ke direktori.")
                    st.rerun()
                else:
                    st.warning("Seluruh kolom wajib diisi.")

        st.markdown("<hr style='border-color: " + p['border'] + ";'>", unsafe_allow_html=True)
        st.markdown("### Daftar Novel Terdaftar")
        if not db["daftar_novel"]:
            st.info("Belum ada inventaris novel tersimpan.")
        else:
            for idx, nov in enumerate(db["daftar_novel"]):
                c1, c2 = st.columns([4, 1])
                c1.markdown(f"**{nov['judul']}** <span style='color:{p['text_secondary']};'>[{nov['genre']}]</span>", unsafe_allow_html=True)
                if c2.button("Hapus", key=f"hapus_nov_{idx}"):
                    record_audit_trail(f"Menghapus novel: {nov['judul']}", "Admin")
                    db["daftar_novel"].remove(nov)
                    save_enterprise_database(db)
                    st.rerun()

    with tab_b:
        st.markdown("### Manajemen Bab Cerita Korporat")
        if not db["daftar_novel"]:
            st.info("Tidak ada novel aktif untuk penambahan bab.")
        else:
            pilih_nov_nama = st.selectbox("Pilih Novel Target", [n["judul"] for n in db["daftar_novel"]])
            target_n = next(n for n in db["daftar_novel"] if n["judul"] == pilih_nov_nama)
            
            if target_n["babad"]:
                st.markdown("#### Bab Terdaftar:")
                for b_idx, b_item in enumerate(target_n["babad"]):
                    with st.expander(f"Kelola: {b_item['nama_bab']}"):
                        with st.form(f"form_edit_bab_{b_idx}"):
                            edit_nama_b = st.text_input("Judul Bab", value=b_item['nama_bab'])
                            edit_isi_b = st.text_area("Konten Narasi", value=b_item['isi'], height=140)
                            
                            col_b1, col_b2 = st.columns(2)
                            if col_b1.form_submit_button("Simpan Perubahan"):
                                if edit_nama_b and edit_isi_b:
                                    b_item['nama_bab'] = edit_nama_b
                                    b_item['isi'] = edit_isi_b
                                    save_enterprise_database(db)
                                    record_audit_trail(f"Memperbarui {edit_nama_b} pada {target_n['judul']}", "Admin")
                                    st.success("Bab diperbarui.")
                                    st.rerun()
                            if col_b2.form_submit_button("Hapus Bab"):
                                target_n['babad'].remove(b_item)
                                save_enterprise_database(db)
                                record_audit_trail(f"Menghapus bab dari {target_n['judul']}", "Admin")
                                st.success("Bab dihapus.")
                                st.rerun()

            st.markdown("<hr style='border-color: " + p['border'] + ";'>", unsafe_allow_html=True)
            with st.form("tambah_bab_form"):
                st.markdown("#### Tambah Bab Baru")
                nama_b = st.text_input("Nama Bab (Contoh: Bab I — Resolusi)")
                isi_b = st.text_area("Teks Konten Lengkap", height=150)
                if st.form_submit_button("Unggah Bab Baru"):
                    if nama_b.strip() and isi_b.strip():
                        target_n["babad"].append({"nama_bab": nama_b.strip(), "isi": isi_b.strip(), "komentar": [], "balasan": []})
                        save_enterprise_database(db)
                        record_audit_trail(f"Menambahkan {nama_b} ke {target_n['judul']}", "Admin")
                        st.success("Bab berhasil diunggah.")
                        st.rerun()
                    else:
                        st.warning("Nama bab dan konten narasi wajib diisi.")

    with tab_c:
        st.markdown("### Antrean Pengajuan ID Pengguna")
        col_head_a, col_head_b = st.columns([3, 1])
        if col_head_b.button("🔄 Refresh Antrean"):
            st.session_state.db = load_enterprise_database()
            st.rerun()

        if not db["antrian_registrasi"]:
            st.info("Tidak ada antrean registrasi pending.")
        else:
            if st.button("🗑️ Bersihkan Seluruh Antrean"):
                db["antrian_registrasi"] = []
                save_enterprise_database(db)
                record_audit_trail("Membersihkan antrean registrasi", "Admin")
                st.success("Antrean dibersihkan.")
                st.rerun()
            st.markdown("<br>", unsafe_allow_html=True)

            for q_idx, req in enumerate(db["antrian_registrasi"]):
                col_1, col_2, col_3 = st.columns([2, 1, 1])
                col_1.markdown(f"ID: **{req['id']}**")
                kode_inputan = col_2.text_input("Kode Verifikasi", value=req.get("kode", ""), key=f"q_kode_{q_idx}")
                if col_3.button("Kirim Kode", key=f"btn_q_{q_idx}"):
                    req["kode"] = kode_inputan
                    save_enterprise_database(db)
                    record_audit_trail(f"Mengirim kode verifikasi ke ID: {req['id']}", "Admin")
                    st.success("Kode terkirim.")
                    st.rerun()
                st.markdown("<hr style='border-color: " + p['border'] + ";'>", unsafe_allow_html=True)

        st.markdown("### Database Pengguna Aktif")
        active_users = {k: v for k, v in db["users_terdaftar"].items() if k != "admin"}
        if not active_users:
            st.info("Belum ada pengguna terdaftar.")
        else:
            for usr in active_users:
                col_u1, col_u2, col_u3 = st.columns([2, 1, 1])
                col_u1.markdown(f"User: **{usr}**")
                new_pwd_input = col_u2.text_input("Sandi Baru", type="password", key=f"reset_pwd_{usr}")
                if col_u2.button("Reset Sandi", key=f"btn_reset_{usr}"):
                    if new_pwd_input.strip():
                        db["users_terdaftar"][usr] = hash_secure(new_pwd_input.strip())
                        save_enterprise_database(db)
                        record_audit_trail(f"Reset password user: {usr}", "Admin")
                        st.success("Sandi direset.")
                        st.rerun()
                if col_u3.button("Hapus Akun", key=f"btn_del_usr_{usr}"):
                    del db["users_terdaftar"][usr]
                    save_enterprise_database(db)
                    record_audit_trail(f"Mencabut akses user: {usr}", "Admin")
                    st.success("Akun dicabut.")
                    st.rerun()

    with tab_d:
        st.markdown("### Audit Logs & Keamanan Sistem")
        logs = db.get("audit_logs", [])
        if not logs:
            st.info("Belum ada aktivitas tercatat.")
        else:
            for log in reversed(logs):
                st.code(log, language="text")

else:
    # --------------------------------------------------------------------------
    # PENGGUNA / USER PORTAL
    # --------------------------------------------------------------------------
    
    # Tombol Setting di Kiri Atas (Simbol Gerigi)
    col_top_l, col_top_r = st.columns([1, 12])
    with col_top_l:
        if st.button("⚙️", help="Pengaturan Tampilan"):
            st.session_state.show_settings_panel = not st.session_state.show_settings_panel
            st.rerun()

    if st.session_state.show_settings_panel:
        st.markdown(
            f"""
            <div class="corporate-card">
                <h3 style="margin-top:0;">🎨 Pengaturan Tema Korporat</h3>
            """,
            unsafe_allow_html=True
        )
        pilihan_tema = st.selectbox(
            "Pilih Skema Warna Sistem",
            ["modern_corporate", "clean_light", "emerald_executive", "royal_purple"],
            index=["modern_corporate", "clean_light", "emerald_executive", "royal_purple"].index(tema)
        )
        if pilihan_tema != tema:
            db["tema"] = pilihan_tema
            save_enterprise_database(db)
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # A. HALAMAN UTAMA (LANDING PAGE)
    if st.session_state.menu == "Utama":
        st.markdown(
            f"""
            <div class="hero-container">
                <h1 class="hero-title">NovelNest</h1>
                <p class="hero-subtitle">
                    Platform publikasi literatur digital tingkat perusahaan. Menghadirkan pengalaman membaca cerita naratif yang mendalam dengan arsitektur keamanan data yang mutakhir.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Dua Tombol: Masuk & Registrasi (Tengah, Sejajar, Ukuran Sama)
        col_sp1, col_b1, col_b2, col_sp2 = st.columns([1.5, 2, 2, 1.5])
        with col_b1:
            if st.button("🔑 Masuk Akun", use_container_width=True):
                st.session_state.menu = "Login"
                st.rerun()
        with col_b2:
            if st.button("📝 Registrasi Akun", use_container_width=True):
                st.session_state.menu = "Registrasi"
                st.rerun()

    # B. HALAMAN LOGIN
    elif st.session_state.menu == "Login":
        if st.button("← Kembali ke Beranda Utama"):
            st.session_state.menu = "Utama"
            st.session_state.admin_step = 0
            st.rerun()

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        st.markdown("<h2>Portal Autentikasi Pengguna</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:{p['text_secondary']};'>Masukkan kredensial akun korporat Anda untuk mengakses pustaka.</p>", unsafe_allow_html=True)

        if st.session_state.logged_in_user:
            st.info(f"Sesi terdeteksi aktif sebagai **{st.session_state.logged_in_user}**.")
            col_lg1, col_lg2 = st.columns(2)
            if col_lg1.button("🚀 Buka Pustaka Novel", use_container_width=True):
                st.session_state.menu = "Koleksi Novel"
                st.rerun()
            if col_lg2.button("🚪 Keluar (Logout)", use_container_width=True):
                record_audit_trail(f"User {st.session_state.logged_in_user} logout", "User")
                if current_device_token in db.get("active_sessions", {}):
                    del db["active_sessions"][current_device_token]
                    save_enterprise_database(db)
                st.session_state.logged_in_user = None
                st.rerun()
        else:
            if st.session_state.admin_step == 1:
                st.info("Verifikasi Kunci Administratif Lapis 1.")
                with st.form("form_verif_1"):
                    v1 = st.text_input("Kunci Enkripsi Lapis 1:", type="password")
                    if st.form_submit_button("Lanjutkan Verifikasi"):
                        if v1 == "123":
                            st.session_state.admin_step = 2
                            st.rerun()
                        else:
                            st.error("Kunci tidak valid.")
                            st.session_state.admin_step = 0

            elif st.session_state.admin_step == 2:
                st.info("Verifikasi Kunci Administratif Lapis 2.")
                with st.form("form_verif_2"):
                    v2 = st.text_input("Kunci Enkripsi Lapis 2:", type="password")
                    if st.form_submit_button("Otorisasi Masuk"):
                        if v2 == "321":
                            st.session_state.is_admin = True
                            st.session_state.admin_step = 0
                            record_audit_trail("Akses Admin berhasil dibuka", "Security")
                            st.success("Otorisasi sukses. Memuat Admin Center...")
                            st.rerun()
                        else:
                            st.error("Kunci tidak valid.")
                            st.session_state.admin_step = 0

            else:
                with st.form("form_user_login"):
                    u_name = st.text_input("Username Korporat")
                    u_pass = st.text_input("Kata Sandi", type="password")
                    
                    if st.form_submit_button("Masuk ke Sistem"):
                        if u_name == "admin" and u_pass == "admin":
                            st.session_state.admin_step = 1
                            st.rerun()
                        else:
                            registered = db["users_terdaftar"]
                            hashed_input = hash_secure(u_pass)
                            if u_name in registered and registered[u_name] == hashed_input:
                                st.session_state.logged_in_user = u_name
                                db.setdefault("active_sessions", {})[current_device_token] = u_name
                                save_enterprise_database(db)
                                record_audit_trail(f"User {u_name} login", "User")
                                st.success(f"Autentikasi berhasil, selamat datang {u_name}.")
                                st.rerun()
                            else:
                                st.error("Kredensial akses tidak dikenali.")

    # C. HALAMAN REGISTRASI & AKTIVASI
    elif st.session_state.menu == "Registrasi":
        if st.button("← Kembali ke Beranda Utama"):
            st.session_state.menu = "Utama"
            st.rerun()

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        st.markdown("<h2>Pusat Registrasi & Aktivasi Akun</h2>", unsafe_allow_html=True)

        t_reg1, t_reg2 = st.tabs(["1. Ajukan ID Pengguna", "2. Aktivasi & Ubah Profil"])

        with t_reg1:
            st.markdown("### Pengajuan ID Pengguna Unik")
            st.markdown(f"<p style='color:{p['text_secondary']};'>Masukkan ID Pengguna samaran Anda untuk antrean verifikasi.</p>", unsafe_allow_html=True)

            col_r_left, col_r_right = st.columns([2, 1])
            with col_r_left:
                with st.form("form_ajukan_id"):
                    id_temp = st.text_input("Masukkan ID Pengguna:")
                    
                    col_btn_sub, col_btn_res = st.columns(2)
                    sub_pengajuan = col_btn_sub.form_submit_button("Kirim Pengajuan")
                    btn_restart_code = col_btn_res.form_submit_button("🔄 Muat Ulang Kode")

                    if sub_pengajuan:
                        if not id_temp.strip():
                            st.warning("ID Pengguna tidak boleh kosong.")
                        else:
                            found_req = next((x for x in db["antrian_registrasi"] if x["id"] == id_temp.strip()), None)
                            if found_req:
                                st.info("ID sudah terdaftar dalam antrean pending.")
                            else:
                                db["antrian_registrasi"].append({"id": id_temp.strip(), "kode": "", "username": "", "password": ""})
                                save_enterprise_database(db)
                                record_audit_trail(f"Pengajuan ID baru: {id_temp.strip()}", "Registration")
                                st.success("Pengajuan berhasil dikirim.")
                                st.rerun()

                    if btn_restart_code:
                        st.session_state.db = load_enterprise_database()
                        st.success("Status antrean diperbarui.")
                        st.rerun()

            with col_r_right:
                st.markdown(
                    f"""
                    <div class="corporate-card" style="margin-bottom:0; padding:16px;">
                        <span style="font-size: 13px; font-weight: 700;">Panel Status Antrean</span><br>
                        <span style="font-size: 24px; font-weight: 800;">{len(db['antrian_registrasi'])}</span><br>
                        <span style="font-size: 12px; color:{p['text_secondary']};">Menunggu persetujuan admin.</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with t_reg2:
            st.markdown("### Aktivasi Akun & Ubah Profil")

            if st.session_state.aktivasi_step == "input_id":
                st.markdown(f"<p style='color:{p['text_secondary']};'>Kolom ini wajib diisi dengan ID Pengguna yang telah dikirimi kode oleh admin.</p>", unsafe_allow_html=True)
                with st.form("form_cek_id_aktivasi"):
                    check_id = st.text_input("ID Pengguna Anda:")
                    if st.form_submit_button("Lanjutkan Verifikasi"):
                        target_q = next((x for x in db["antrian_registrasi"] if x["id"] == check_id.strip()), None)
                        if target_q and target_q.get("kode"):
                            st.session_state.temp_validated_id = check_id.strip()
                            st.session_state.aktivasi_step = "konfirmasi_id"
                            st.rerun()
                        else:
                            st.error("ID tidak ditemukan atau kode verifikasi belum dikirim admin.")

            elif st.session_state.aktivasi_step == "konfirmasi_id":
                st.warning(f"Apakah Anda yakin ID Pengguna **'{st.session_state.temp_validated_id}'** sudah benar?")
                col_konf1, col_konf2 = st.columns(2)
                if col_konf1.button("Ya, Benar", use_container_width=True):
                    st.session_state.aktivasi_step = "form_profil"
                    st.rerun()
                if col_konf2.button("Tidak, Ulangi", use_container_width=True):
                    st.session_state.temp_validated_id = ""
                    st.session_state.aktivasi_step = "input_id"
                    st.rerun()

            elif st.session_state.aktivasi_step == "form_profil":
                st.info("Silakan buat Username dan Password permanen untuk akun Anda.")
                target_q = next((x for x in db["antrian_registrasi"] if x["id"] == st.session_state.temp_validated_id), None)
                
                with st.form("form_aktivasi_profil_final"):
                    inp_kode = st.text_input("Kode Verifikasi dari Admin:")
                    inp_new_u = st.text_input("Username Baru:")
                    inp_new_p = st.text_input("Password Baru:", type="password")

                    if st.form_submit_button("Simpan & Aktifkan Akun"):
                        if not target_q or target_q.get("kode") != inp_kode.strip():
                            st.error("Kode verifikasi salah.")
                        elif inp_new_u.strip() in db["users_terdaftar"]:
                            st.error("Username sudah digunakan.")
                        else:
                            db["users_terdaftar"][inp_new_u.strip()] = hash_secure(inp_new_p.strip())
                            db["antrian_registrasi"].remove(target_q)
                            save_enterprise_database(db)
                            
                            record_audit_trail(f"Akun baru aktif: {inp_new_u.strip()}", "Registration")
                            st.session_state.aktivasi_step = "input_id"
                            st.session_state.temp_validated_id = ""
                            st.session_state.menu = "Login"
                            st.success("Akun berhasil diaktifkan! Dialihkan ke halaman Login...")
                            st.rerun()

    # D. KOLEKSI NOVEL
    elif st.session_state.menu == "Koleksi Novel":
        if st.button("← Keluar ke Beranda Utama"):
            st.session_state.menu = "Utama"
            st.rerun()

        if not st.session_state.logged_in_user:
            st.warning("Anda harus masuk terlebih dahulu melalui menu 'Masuk Akun'.")
            if st.button("Pindah ke Halaman Login"):
                st.session_state.menu = "Login"
                st.rerun()
        else:
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            st.markdown(f"<h2>NovelNest Pustaka Utama</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:{p['text_secondary']};'>Sesi Aktif: <strong>{st.session_state.logged_in_user}</strong></p>", unsafe_allow_html=True)
            st.markdown("<hr style='border-color: " + p['border'] + ";'>", unsafe_allow_html=True)

            if st.session_state.selected_novel is None:
                st.markdown("### Pilih Novel Favorit Anda:")
                if not db["daftar_novel"]:
                    st.info("Belum ada novel tersedia dalam sistem.")
                else:
                    for idx_n, n_item in enumerate(db["daftar_novel"]):
                        if st.button(f"📖 {n_item['judul']} — [{n_item['genre']}]", key=f"pilih_n_{idx_n}", use_container_width=True):
                            st.session_state.selected_novel = n_item
                            st.rerun()
            else:
                current_novel = st.session_state.selected_novel
                if st.button("Kembali ke Daftar Novel"):
                    st.session_state.selected_novel = None
                    st.session_state.selected_bab = None
                    st.rerun()

                if st.session_state.selected_bab is None:
                    st.markdown(f"<h2>{current_novel['judul']}</h2>", unsafe_allow_html=True)
                    st.markdown(f"<p style='color:{p['text_secondary']};'><strong>Genre / Sinopsis:</strong> {current_novel['genre']}</p>", unsafe_allow_html=True)
                    st.markdown("<hr style='border-color: " + p['border'] + ";'>", unsafe_allow_html=True)
                    st.markdown("### Daftar Bab Tersedia")
                    if not current_novel["babad"]:
                        st.info("Belum ada bab yang dirilis.")
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

                    st.markdown(f"<h3>{current_novel['judul']} — {current_bab['nama_bab']}</h3>", unsafe_allow_html=True)
                    st.markdown("<hr style='border-color: " + p['border'] + ";'>", unsafe_allow_html=True)
                    
                    # Kotak Bacaan Naratif Elegan
                    st.markdown(
                        f"""
                        <div class="corporate-card" style="line-height: 1.8; font-size: 16px; white-space: pre-wrap; font-weight: 400;">
{current_bab['isi']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    st.markdown("<hr style='border-color: " + p['border'] + ";'>", unsafe_allow_html=True)
                    st.markdown("### Kolom Komentar & Diskusi")

                    if "komentar" not in current_bab:
                        current_bab["komentar"] = []

                    with st.form("form_tambah_komentar"):
                        isi_komentar = st.text_area("Tulis ulasan Anda...")
                        if st.form_submit_button("Kirim Komentar"):
                            if isi_komentar.strip():
                                current_bab["komentar"].append({
                                    "user": st.session_state.logged_in_user,
                                    "pesan": isi_komentar.strip(),
                                    "balasan": []
                                })
                                save_enterprise_database(db)
                                st.success("Komentar terkirim.")
                                st.rerun()
                            else:
                                st.warning("Komentar kosong.")

                    if not current_bab["komentar"]:
                        st.info("Belum ada ulasan pada bab ini.")
                    else:
                        for idx_k, kom in enumerate(current_bab["komentar"]):
                            if "balasan" not in kom:
                                kom["balasan"] = []
                            st.markdown(
                                f"""
                                <div style="background-color: {p['bg_surface']}; padding: 14px; border-radius: 8px; border: 1px solid {p['border']}; margin-bottom: 10px;">
                                    <strong>{kom['user']}</strong><br>{kom['pesan']}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            for bal in kom["balasan"]:
                                st.markdown(
                                    f"""
                                    <div style="background-color: rgba(0,0,0,0.05); padding: 8px 10px; border-radius: 6px; margin-left: 30px; margin-bottom: 6px; border-left: 3px solid {p['accent']};">
                                        <span style="font-size: 13px;">↳ <strong>{bal['user']}</strong>: {bal['pesan']}</span>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                            with st.form(f"form_balas_{idx_k}"):
                                pesan_balasan = st.text_input("Balas ulasan...", key=f"input_balas_{idx_k}")
                                if st.form_submit_button("Kirim Balasan"):
                                    if pesan_balasan.strip():
                                        kom["balasan"].append({
                                            "user": st.session_state.logged_in_user,
                                            "pesan": pesan_balasan.strip()
                                        })
                                        save_enterprise_database(db)
                                        st.success("Balasan terkirim.")
                                        st.rerun()
                                    else:
                                        st.warning("Balasan kosong.")
                            st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 5. FOOTER KORPORAT PROFESIONAL
# ==============================================================================
st.markdown(
    f"""
    <div class="enterprise-footer">
        NovelNest Corporate Suite &bull; Version {SYSTEM_VERSION} &bull; Secured with Advanced UI/UX Architecture &bull; All Rights Reserved
    </div>
    """,
    unsafe_allow_html=True
)
