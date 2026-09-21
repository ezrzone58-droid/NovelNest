import streamlit as st
import json
import os

# ==================== KONFIGURASI HALAMAN ====================
st.set_page_config(
    page_title="NovelNest - Web Edition",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

FILE_DATABASE = "novelnest_data.json"

# ==================== MANAJEMEN DATABASE ====================
def muat_data():
    if os.path.exists(FILE_DATABASE):
        try:
            with open(FILE_DATABASE, "r") as f:
                data = json.load(f)
                return {
                    "tema": data.get("tema", "biru"),
                    "daftar_novel": data.get("daftar_novel", []),
                    "antrian_registrasi": data.get("antrian_registrasi", []),
                    "users_terdaftar": data.get("users_terdaftar", {"admin": "admin"})
                }
        except Exception as e:
            st.error(f"Gagal memuat data: {e}")
    return {
        "tema": "biru",
        "daftar_novel": [],
        "antrian_registrasi": [],
        "users_terdaftar": {"admin": "admin"}
    }

def simpan_data(data):
    try:
        with open(FILE_DATABASE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        st.error(f"Gagal menyimpan data: {e}")

# ==================== INISIALISASI STATE ====================
if "db" not in st.session_state:
    st.session_state.db = muat_data()

if "menu" not in st.session_state:
    st.session_state.menu = "Beranda"

if "selected_novel" not in st.session_state:
    st.session_state.selected_novel = None

if "selected_bab" not in st.session_state:
    st.session_state.selected_bab = None

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

if "show_theme_selector" not in st.session_state:
    st.session_state.show_theme_selector = False

db = st.session_state.db

# ==================== Kustomisasi Tema & CSS ====================
tema = db.get("tema", "biru")
if tema == "merah":
    bg_sidebar = "#18181b"
    bg_utama = "#121212"
    fg_teks = "#f3f4f6"
    accent_btn = "#dc2626"
    box_bg = "#27272a"
    muted_color = "#9ca3af"
elif tema == "hijau":
    bg_sidebar = "#064e3b"
    bg_utama = "#f0fdf4"
    fg_teks = "#064e3b"
    accent_btn = "#059669"
    box_bg = "#d1fae5"
    muted_color = "#047857"
elif tema == "ungu":
    bg_sidebar = "#3b0764"
    bg_utama = "#faf5ff"
    fg_teks = "#3b0764"
    accent_btn = "#7c3aed"
    box_bg = "#f3e8ff"
    muted_color = "#6b21a8"
else:  # biru
    bg_sidebar = "#0f172a"
    bg_utama = "#f4f6f8"
    fg_teks = "#1e293b"
    accent_btn = "#2563eb"
    box_bg = "#e2e8f0"
    muted_color = "#64748b"

st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_utama};
        color: {fg_teks};
        font-family: 'Century Gothic', sans-serif;
    }}
    [data-testid="stSidebar"] {{
        background-color: {bg_sidebar};
        padding-top: 15px;
    }}
    [data-testid="stSidebar"] * {{
        color: #ffffff !important;
        font-family: 'Century Gothic', sans-serif;
    }}
    div.stButton > button {{
        background-color: {accent_btn};
        color: white;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.2s ease-in-out;
    }}
    div.stButton > button:hover {{
        opacity: 0.85;
        transform: translateY(-1px);
    }}
    input, textarea {{
        background-color: {box_bg} !important;
        color: {fg_teks} !important;
        border-radius: 6px !important;
        border: 1px solid rgba(0,0,0,0.1) !important;
    }}
    .custom-card {{
        background-color: {box_bg};
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 15px;
    }}
    </style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR UTAMA ====================
st.sidebar.markdown("<h2 style='text-align: center; letter-spacing: 1px;'>NovelNest</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

st.sidebar.markdown(f"<p style='font-size: 11px; color: {muted_color}; text-transform: uppercase;'>Navigasi Menu</p>", unsafe_allow_html=True)

# Logika Navigasi Sidebar
menu_opsi = ["Beranda", "Masuk (Login)", "Registrasi Akun", "Koleksi Novel"]
if st.session_state.is_admin:
    menu_opsi.append("Admin Dashboard")

navigasi = st.sidebar.radio("Pilih Menu", menu_opsi, label_visibility="collapsed")

st.sidebar.markdown("---")

# Tombol Pengaturan Setting (Gerigi)
if st.sidebar.button("⚙️ Setting Aplikasi", use_container_width=True):
    st.session_state.show_theme_selector = not st.session_state.show_theme_selector

if st.session_state.show_theme_selector:
    st.sidebar.markdown("### Pengaturan Tema")
    pilihan_tema = st.sidebar.selectbox(
        "Pilih Tema Warna", 
        ["biru", "merah", "hijau", "ungu"], 
        index=["biru", "merah", "hijau", "ungu"].index(tema)
    )
    if pilihan_tema != tema:
        db["tema"] = pilihan_tema
        simpan_data(db)
        st.rerun()

# ==================== KONTROL HALAMAN ====================

# 1. HALAMAN BERANDA
if navigasi == "Beranda":
    # Tombol rahasia di judul beranda untuk akses login admin
    if st.button("✨ Selamat Datang di NovelNest", use_container_width=True):
        st.session_state.menu = "AdminLogin"
        st.rerun()
        
    st.markdown(f"""
        <div style='text-align: center; padding: 40px 0;'>
            <p style='font-size: 16px; font-style: italic; color: {muted_color};'>
                Rumah digital bagi para reader yang suka membaca hal-hal seru dan mendalam.
            </p>
        </div>
    """, unsafe_allow_html=True)

# 2. HALAMAN LOGIN ADMIN TERSEMBUNYI
elif st.session_state.menu == "AdminLogin":
    st.title("🔐 ADMIN ACCESS")
    with st.form("form_login_admin"):
        p1 = st.text_input("Verifikasi Atas (Pass: 123):", type="password")
        p2 = st.text_input("Verifikasi Bawah (Pass: abc):", type="password")
        submit_adm = st.form_submit_button("Masuk Sistem Admin")
        
        if submit_adm:
            if p1 == "123" and p2 == "abc":
                st.session_state.is_admin = True
                st.session_state.menu = "AdminDashboard"
                st.success("Verifikasi berhasil! Mengalihkan ke Dashboard...")
                st.rerun()
            else:
                st.error("Verifikasi kredensial salah!")
                
    if st.button("Kembali ke Beranda Utama"):
        st.session_state.menu = "Beranda"
        st.rerun()

# 3. ADMIN DASHBOARD
elif navigasi == "AdminDashboard" or st.session_state.menu == "AdminDashboard":
    st.title("📊 ADMIN DASHBOARD")
    
    if st.button("🚪 Logout dari Mode Admin"):
        st.session_state.is_admin = False
        st.session_state.menu = "Beranda"
        st.rerun()
        
    tab_a, tab_b, tab_c = st.tabs(["📚 Kelola Novel", "✏️ Kelola Bab", "👥 Data User & Antrean"])
    
    with tab_a:
        st.subheader("Tambah Novel Baru")
        with st.form("tambah_novel_form"):
            jdl = st.text_input("Judul Novel")
            gnr = st.text_input("Deskripsi / Genre")
            if st.form_submit_button("Simpan Novel"):
                if jdl and gnr:
                    db["daftar_novel"].append({"judul": jdl, "genre": gnr, "babad": []})
                    simpan_data(db)
                    st.success("Novel baru berhasil ditambahkan!")
                    st.rerun()
                else:
                    st.warning("Judul dan genre tidak boleh kosong.")
                    
        st.markdown("---")
        st.subheader("Daftar Hapus Novel")
        if not db["daftar_novel"]:
            st.info("Belum ada novel di database.")
        else:
            for idx, nov in enumerate(db["daftar_novel"]):
                c1, c2 = st.columns([3, 1])
                c1.write(f"**{nov['judul']}** ({nov['genre']})")
                if c2.button("Hapus", key=f"hapus_nov_{idx}"):
                    db["daftar_novel"].remove(nov)
                    simpan_data(db)
                    st.rerun()

    with tab_b:
        st.subheader("Manajemen Bab Cerita")
        if not db["daftar_novel"]:
            st.info("Belum ada novel tersedia untuk diberi bab.")
        else:
            pilih_nov_nama = st.selectbox("Pilih Novel", [n['judul'] for n in db["daftar_novel"]])
            target_n = next(n for n in db["daftar_novel"] if n['judul'] == pilih_nov_nama)
            
            st.markdown("**Bab Terdaftar:**")
            if not target_n['babad']:
                st.caption("Belum ada bab.")
            else:
                for b_item in target_n['babad']:
                    st.write(f"- {b_item['nama_bab']}")
                    
            st.markdown("---")
            with st.form("tambah_bab_form"):
                nama_b = st.text_input("Nama Bab (Contoh: Bab 1 - Awal Mula)")
                isi_b = st.text_area("Isi Cerita Lengkap", height=150)
                if st.form_submit_button("Simpan Bab Baru"):
                    if nama_b and isi_b:
                        target_n['babad'].append({"nama_bab": nama_b, "isi": isi_b})
                        simpan_data(db)
                        st.success("Bab berhasil disimpan!")
                        st.rerun()
                    else:
                        st.warning("Nama bab dan isi cerita wajib diisi.")

    with tab_c:
        st.subheader("Antrean Registrasi Pengajuan User")
        if not db["antrian_registrasi"]:
            st.info("Tidak ada antrean registrasi.")
        else:
            for q_idx, req in enumerate(db["antrian_registrasi"]):
                col_1, col_2, col_3 = st.columns([2, 1, 1])
                col_1.write(f"ID Sementara: **{req['id']}**")
                kode_inputan = col_2.text_input("Kode Verifikasi", value=req.get('kode', ''), key=f"q_kode_{q_idx}")
                if col_3.button("Kirim Kode", key=f"btn_q_{q_idx}"):
                    req['kode'] = kode_inputan
                    simpan_data(db)
                    st.success(f"Kode untuk ID {req['id']} berhasil dikirim!")
                    st.rerun()
                st.markdown("---")
                
        st.subheader("Database User Aktif")
        active_users = {k: v for k, v in db["users_terdaftar"].items() if k != "admin"}
        if not active_users:
            st.info("Belum ada user terdaftar selain admin.")
        else:
            for usr, pwd in active_users.items():
                st.write(f"- Username: **{usr}** | Password: **{pwd}**")

# 4. HALAMAN KOLEKSI NOVEL (PERLU LOGIN)
elif navigasi == "Koleksi Novel":
    if not st.session_state.logged_in_user:
        st.warning("⚠️ Anda harus masuk (login) terlebih dahulu melalui menu 'Masuk (Login)' untuk membaca koleksi novel!")
    else:
        st.title("📚 NovelNest Library")
        st.markdown(f"Status Login: **{st.session_state.logged_in_user}**")
        st.markdown("---")
        
        if st.session_state.selected_novel is None:
            st.subheader("Pilih Novel Favorit Anda:")
            if not db["daftar_novel"]:
                st.info("Belum ada novel tersedia.")
            else:
                for idx_n, n_item in enumerate(db["daftar_novel"]):
                    if st.button(f"📖 {n_item['judul']} [{n_item['genre']}]", key=f"pilih_n_{idx_n}", use_container_width=True):
                        st.session_state.selected_novel = n_item
                        st.rerun()
        else:
            current_novel = st.session_state.selected_novel
            if st.button("⬅️ Kembali ke Daftar Novel"):
                st.session_state.selected_novel = None
                st.session_state.selected_bab = None
                st.rerun()
                
            if st.session_state.selected_bab is None:
                st.title(f"📖 {current_novel['judul']}")
                st.markdown(f"**Genre/Deskripsi:** {current_novel['genre']}")
                st.markdown("---")
                st.subheader("Daftar Bab Tersedia")
                if not current_novel['babad']:
                    st.info("Belum ada bab yang ditulis untuk novel ini.")
                else:
                    for idx_b, b_item in enumerate(current_novel['babad']):
                        if st.button(f"• {b_item['nama_bab']}", key=f"buka_b_{idx_b}"):
                            st.session_state.selected_bab = b_item
                            st.rerun()
            else:
                current_bab = st.session_state.selected_bab
                if st.button("⬅️ Kembali ke Daftar Bab"):
                    st.session_state.selected_bab = None
                    st.rerun()
                    
                st.markdown(f"### {current_novel['judul']} — {current_bab['nama_bab']}")
                st.markdown("---")
                
                # Area Teks Bacaan yang Lebar dan Nyaman
                st.markdown(f"""
                    <div style='background-color: {box_bg}; padding: 25px; border-radius: 8px; line-height: 1.6; white-space: pre-wrap;'>
{current_bab['isi']}
                    </div>
                """, unsafe_allow_html=True)

# 5. HALAMAN LOGIN USER
elif navigasi == "Masuk (Login)":
    st.title("🔑 USER LOGIN")
    with st.form("form_user_login"):
        u_name = st.text_input("Username")
        u_pass = st.text_input("Password", type="password")
        if st.form_submit_button("Masuk"):
            registered = db["users_terdaftar"]
            if u_name in registered and registered[u_name] == u_pass:
                st.session_state.logged_in_user = u_name
                st.success(f"Berhasil masuk sebagai {u_name}! Silakan buka menu 'Koleksi Novel'.")
            else:
                st.error("Username atau Password salah!")

# 6. HALAMAN REGISTRASI
elif navigasi == "Registrasi Akun":
    st.title("📝 USER REGISTRATION")
    
    t_reg1, t_reg2 = st.tabs(["1. Ajukan ID Sementara", "2. Aktivasi Akun & Ubah Profil"])
    
    with t_reg1:
        with st.form("form_ajukan_id"):
            id_temp = st.text_input("Masukkan ID Sementara Anda:")
            if st.form_submit_button("Kirim Pengajuan"):
                if not id_temp:
                    st.warning("ID tidak boleh kosong.")
                else:
                    found_req = next((x for x in db["antrian_registrasi"] if x['id'] == id_temp), None)
                    if found_req:
                        pos = db["antrian_registrasi"].index(found_req) + 1
                        st.info(f"ID sudah terdaftar dalam antrean ke-#{pos}.\nKode Admin: {found_req.get('kode', 'Menunggu pengiriman...')}")
                    else:
                        db["antrian_registrasi"].append({"id": id_temp, "kode": "", "username": "", "password": ""})
                        simpan_data(db)
                        st.success(f"Pengajuan berhasil dikirim! Nomor antrean Anda: #{len(db['antrian_registrasi'])}")
                        
    with t_reg2:
        with st.form("form_aktivasi_akun"):
            inp_id = st.text_input("ID Sementara Anda:")
            inp_kode = st.text_input("Kode Verifikasi dari Admin:")
            inp_new_u = st.text_input("Username Baru:")
            inp_new_p = st.text_input("Password Baru:", type="password")
            if st.form_submit_button("Simpan Perubahan Akun"):
                target_q = next((x for x in db["antrian_registrasi"] if x['id'] == inp_id), None)
                if not target_q:
                    st.error("ID tidak ditemukan dalam antrean registrasi.")
                elif target_q.get('kode') != inp_kode:
                    st.error("Kode verifikasi salah atau belum dikirimkan oleh admin.")
                elif inp_new_u in db["users_terdaftar"]:
                    st.error("Username tersebut sudah digunakan orang lain.")
                else:
                    db["users_terdaftar"][inp_new_u] = inp_new_p
                    db["antrian_registrasi"].remove(target_q)
                    simpan_data(db)
                    st.success("Akun berhasil diaktifkan! Silakan lakukan login melalui menu 'Masuk (Login)'.")
