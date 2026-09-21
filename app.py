import streamlit as st
import json
import os

st.set_page_config(page_title="NovelNest", page_icon="📚", layout="wide")

FILE_DATABASE = "novelnest_data.json"

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
        except:
            pass
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

# --- STYLING CSS KUSTOM (MENYERUPAI APLIKASI DESKTOP) ---
tema = db["tema"]
if tema == "merah":
    bg_sidebar = "#18181b"
    bg_utama = "#121212"
    fg_teks = "#f3f4f6"
    accent_btn = "#dc2626"
    box_bg = "#27272a"
elif tema == "hijau":
    bg_sidebar = "#064e3b"
    bg_utama = "#f0fdf4"
    fg_teks = "#064e3b"
    accent_btn = "#059669"
    box_bg = "#d1fae5"
elif tema == "ungu":
    bg_sidebar = "#3b0764"
    bg_utama = "#faf5ff"
    fg_teks = "#3b0764"
    accent_btn = "#7c3aed"
    box_bg = "#f3e8ff"
else: # biru
    bg_sidebar = "#0f172a"
    bg_utama = "#f4f6f8"
    fg_teks = "#1e293b"
    accent_btn = "#2563eb"
    box_bg = "#e2e8f0"

st.markdown(f"""
    <style>
    /* Mengatur Latar Belakang Utama & Warna Teks */
    .stApp {{
        background-color: {bg_utama};
        color: {fg_teks};
        font-family: 'Century Gothic', sans-serif;
    }}
    
    /* Mengatur Sidebar agar Bold & Elegan */
    [data-testid="stSidebar"] {{
        background-color: {bg_sidebar};
        padding-top: 20px;
    }}
    [data-testid="stSidebar"] * {{
        color: #ffffff !important;
        font-family: 'Century Gothic', sans-serif;
    }}

    /* Mempercantik Tombol (Button) */
    div.stButton > button {{
        background-color: {accent_btn};
        color: white;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }}
    div.stButton > button:hover {{
        opacity: 0.85;
        border-color: transparent;
    }}

    /* Mempercantik Input Teks & Text Area */
    input, textarea {{
        background-color: {box_bg} !important;
        color: {fg_teks} !important;
        border-radius: 6px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR MENU (ELEGAN & SIMPLE) ---
st.sidebar.markdown("<h1 style='text-align: center; font-size: 24px; font-weight: bold;'>NovelNest</h1>", unsafe_allow_html=True)
st.sidebar.markdown("---")

menu_pilihan = st.sidebar.radio("NAVIGASI MENU", ["Beranda", "Masuk (Login)", "Registrasi Akun", "Koleksi Novel"])

st.sidebar.markdown("---")

# Tombol Gerigi Setting di Sidebar
if st.sidebar.button("⚙️ Setting"):
    st.session_state.show_theme_selector = not st.session_state.show_theme_selector

# Panel Pengaturan Tema yang Muncul Saat Gerigi Ditekan
if st.session_state.show_theme_selector:
    st.sidebar.markdown("### Pengaturan Tema")
    tema_pilihan = st.sidebar.selectbox("Pilih Tema Warna", ["biru", "merah", "hijau", "ungu"], index=["biru", "merah", "hijau", "ungu"].index(tema))
    if tema_pilihan != tema:
        db["tema"] = tema_pilihan
        simpan_data(db)
        st.rerun()

# --- HALAMAN BERANDA (MINIMALIS & RAHASIA ADMIN) ---
if st.session_state.menu == "AdminLogin":
    st.title("ADMIN ACCESS")
    with st.form("form_admin_login"):
        pass1 = st.text_input("Verifikasi Atas (Pass: 123):", type="password")
        pass2 = st.text_input("Verifikasi Bawah (Pass: abc):", type="password")
        submit_adm = st.form_submit_button("Masuk Admin")
        
        if submit_adm:
            if pass1 == "123" and pass2 == "abc":
                st.session_state.is_admin = True
                st.session_state.menu = "AdminDashboard"
                st.success("Verifikasi berhasil!")
                st.rerun()
            else:
                st.error("Verifikasi salah!")
    if st.button("Kembali ke Beranda"):
        st.session_state.menu = "Beranda"
        st.rerun()

elif st.session_state.menu == "AdminDashboard" or st.session_state.is_admin:
    st.title("ADMIN DASHBOARD")
    if st.button("🚪 Logout Admin"):
        st.session_state.is_admin = False
        st.session_state.menu = "Beranda"
        st.rerun()
        
    tab_adm1, tab_adm2, tab_adm3 = st.tabs(["📚 Tambah & Hapus Novel", "✏️ Edit Novel & Kelola Bab", "👥 Data User & Antrean"])
    
    with tab_adm1:
        st.subheader("Tambah Novel Baru")
        with st.form("form_tambah_nov"):
            j_nov = st.text_input("Judul Novel")
            g_nov = st.text_input("Deskripsi / Genre")
            s_nov = st.form_submit_button("Selesai")
            if s_nov:
                if j_nov and g_nov:
                    db["daftar_novel"].append({"judul": j_nov, "genre": g_nov, "babad": []})
                    simpan_data(db)
                    st.success("Novel berhasil disimpan!")
                    st.rerun()
                else:
                    st.warning("Semua kolom harus diisi!")
                    
        st.markdown("---")
        st.subheader("Hapus Novel")
        if not db["daftar_novel"]:
            st.info("Belum ada novel.")
        else:
            for n_idx, novel in enumerate(db["daftar_novel"]):
                col1, col2 = st.columns([3, 1])
                col1.write(f"**{novel['judul']}** ({novel['genre']})")
                if col2.button("Hapus", key=f"del_n_{n_idx}"):
                    db["daftar_novel"].remove(novel)
                    simpan_data(db)
                    st.rerun()
                    
    with tab_adm2:
        st.subheader("Kelola Bab Novel")
        if not db["daftar_novel"]:
            st.info("Belum ada novel.")
        else:
            selected_novel_name = st.selectbox("Pilih Novel", [n['judul'] for n in db["daftar_novel"]])
            target_novel = next(n for n in db["daftar_novel"] if n['judul'] == selected_novel_name)
            
            st.markdown(f"**Daftar Bab Saat Ini:**")
            if not target_novel['babad']:
                st.caption("Belum ada bab.")
            else:
                for b in target_novel['babad']:
                    st.write(f"- {b['nama_bab']}")
                    
            st.markdown("---")
            st.subheader("Tambah Bab Baru")
            with st.form(f"form_tambah_bab_{selected_novel_name}"):
                nama_bab = st.text_input("Nama Bab (Cth: Bab 1)")
                isi_cerita = st.text_area("Isi Cerita")
                s_bab = st.form_submit_button("Simpan Bab")
                if s_bab:
                    if nama_bab and isi_cerita:
                        target_novel['babad'].append({"nama_bab": nama_bab, "isi": isi_cerita})
                        simpan_data(db)
                        st.success("Bab berhasil ditambahkan!")
                        st.rerun()
                    else:
                        st.warning("Semua kolom harus diisi!")
                        
    with tab_adm3:
        st.subheader("Antrean Registrasi Pengajuan")
        if not db["antrian_registrasi"]:
            st.info("Tidak ada pengajuan antrean.")
        else:
            for a_idx, req in enumerate(db["antrian_registrasi"]):
                col1, col2, col3 = st.columns([2, 1, 1])
                col1.write(f"ID: **{req['id']}**")
                k_val = col2.text_input("Kode", value=req.get('kode', ''), key=f"kode_req_{a_idx}")
                if col3.button("Kirim Kode", key=f"btn_req_{a_idx}"):
                    req['kode'] = k_val
                    simpan_data(db)
                    st.success("Kode dikirim!")
                    st.rerun()
                st.markdown("---")
                
        st.subheader("Database User Terdaftar")
        for u_key, u_val in db["users_terdaftar"].items():
            if u_key != "admin":
                st.write(f"- Username: **{u_key}** | Password: **{u_val}**")

elif menu_pilihan == "Beranda":
    # Tombol Tersembunyi di Judul Beranda untuk Mengakses Halaman Admin
    if st.button("✨ NovelNest (Akses Admin Rahasia)", use_container_width=True):
        st.session_state.menu = "AdminLogin"
        st.rerun()
        
    st.markdown("<p style='text-align: center; font-style: italic; color: gray; margin-top: 20px;'>Rumah digital bagi para reader yang suka membaca hal-hal seru</p>", unsafe_allow_html=True)

# --- HALAMAN KOLEKSI NOVEL (PERLU LOGIN) ---
elif menu_pilihan == "Koleksi Novel":
    if not st.session_state.logged_in_user:
        st.warning("⚠️ Anda harus masuk (login) terlebih dahulu untuk mengakses dan membaca koleksi novel!")
    else:
        st.title("📚 NovelNest Library")
        st.write(f"Selamat datang kembali, **{st.session_state.logged_in_user}**!")
        st.markdown("---")
        
        if st.session_state.selected_novel is None:
            st.subheader("Pilih Novel:")
            if not db["daftar_novel"]:
                st.info("Belum ada novel tersedia.")
            else:
                for idx, novel in enumerate(db["daftar_novel"]):
                    if st.button(f"📖 {novel['judul']} — ({novel['genre']})", key=f"nov_list_{idx}"):
                        st.session_state.selected_novel = novel
                        st.rerun()
        else:
            novel = st.session_state.selected_novel
            if st.button("⬅️ Kembali ke Daftar Novel"):
                st.session_state.selected_novel = None
                st.session_state.selected_bab = None
                st.rerun()
                
            if st.session_state.selected_bab is None:
                st.title(f"📖 {novel['judul']}")
                st.markdown(f"**Deskripsi / Genre:** {novel['genre']}")
                st.markdown("---")
                st.subheader("Daftar Bab")
                if not novel['babad']:
                    st.info("Belum ada bab tersedia.")
                else:
                    for b_idx, bab in enumerate(novel['babad']):
                        if st.button(f"• {bab['nama_bab']}", key=f"bab_pilih_{b_idx}"):
                            st.session_state.selected_bab = bab
                            st.rerun()
            else:
                bab = st.session_state.selected_bab
                if st.button("⬅️ Kembali ke Daftar Bab"):
                    st.session_state.selected_bab = None
                    st.rerun()
                    
                st.title(f"{novel['judul']} — {bab['nama_bab']}")
                st.markdown("---")
                st.write(bab['isi'])

# --- HALAMAN LOGIN ---
elif menu_pilihan == "Masuk (Login)":
    st.title("USER LOGIN")
    with st.form("form_login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_login = st.form_submit_button("Login")
        
        if submit_login:
            users = db["users_terdaftar"]
            if username in users and users[username] == password:
                st.session_state.logged_in_user = username
                st.success(f"Berhasil login sebagai {username}! Silakan buka menu 'Koleksi Novel'.")
            else:
                st.error("Username atau Password salah!")

# --- HALAMAN REGISTRASI ---
elif menu_pilihan == "Registrasi Akun":
    st.title("USER REGISTRATION")
    
    tab1, tab2 = st.tabs(["1. Ajukan ID Sementara", "2. Edit Username & Password"])
    
    with tab1:
        with st.form("form_reg"):
            id_sementara = st.text_input("Masukkan ID Sementara:")
            submit_reg = st.form_submit_button("Kirim Pengajuan ID")
            
            if submit_reg:
                if not id_sementara:
                    st.warning("ID tidak boleh kosong!")
                else:
                    existing = next((item for item in db["antrian_registrasi"] if item['id'] == id_sementara), None)
                    if existing:
                        idx_antri = db["antrian_registrasi"].index(existing) + 1
                        st.info(f"ID sudah terdaftar.\nNomor Antrean Anda: #{idx_antri}\nKode Dari Admin: {existing.get('kode', 'Menunggu pengiriman...')}")
                    else:
                        db["antrian_registrasi"].append({"id": id_sementara, "kode": "", "username": "", "password": ""})
                        simpan_data(db)
                        st.success(f"Pengajuan berhasil dikirim!\nNomor Antrean Anda: #{len(db['antrian_registrasi'])}")
                        
    with tab2:
        with st.form("form_edit_akun"):
            id_input = st.text_input("Masukkan ID Anda:")
            kode_input = st.text_input("Masukkan Kode dari Admin:")
            new_user = st.text_input("Username Baru:")
            new_pass = st.text_input("Password Baru:", type="password")
            submit_aktivasi = st.form_submit_button("Simpan Perubahan Akun")
            
            if submit_aktivasi:
                target = next((item for item in db["antrian_registrasi"] if item['id'] == id_input), None)
                if not target:
                    st.error("ID tidak ditemukan dalam pengajuan antrean!")
                elif target.get('kode') != kode_input:
                    st.error("Kode dari admin salah atau belum dikirimkan!")
                elif new_user in db["users_terdaftar"]:
                    st.error("Username sudah digunakan oleh akun lain!")
                else:
                    db["users_terdaftar"][new_user] = new_pass
                    db["antrian_registrasi"].remove(target)
                    simpan_data(db)
                    st.success("Akun berhasil diaktifkan! Silakan pindah ke menu Login.")
