import streamlit as st
import json
import os

# Konfigurasi Halaman Web
st.set_page_config(page_title="NovelNest", page_icon="📚", layout="centered")

# File Database Lokal
FILE_DATABASE = "novelnest_data.json"

# Fungsi untuk memuat data
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

# Fungsi untuk menyimpan data
def simpan_data(data):
    try:
        with open(FILE_DATABASE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        st.error(f"Gagal menyimpan data: {e}")

# Inisialisasi Session State
if "db" not in st.session_state:
    st.session_state.db = muat_data()

if "menu" not in st.session_state:
    st.session_state.menu = "Beranda"

if "selected_novel" not in st.session_state:
    st.session_state.selected_novel = None

if "selected_bab" not in st.session_state:
    st.session_state.selected_bab = None

db = st.session_state.db

# --- SIDEBAR MENU ---
st.sidebar.title("📖 NovelNest")
st.sidebar.markdown("---")

menu_pilihan = st.sidebar.radio("Navigasi Menu", ["Beranda", "Login", "Registrasi Akun", "Admin Dashboard"])

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Setting Tema")
tema_pilihan = st.sidebar.selectbox("Pilih Tema Warna", ["biru", "merah", "hijau", "ungu"], index=["biru", "merah", "hijau", "ungu"].index(db["tema"]))
if tema_pilihan != db["tema"]:
    db["tema"] = tema_pilihan
    simpan_data(db)
    st.rerun()

# --- HALAMAN BERANDA ---
if menu_pilihan == "Beranda":
    st.title("✨ Selamat Datang di NovelNest")
    st.markdown("*Rumah digital bagi para reader yang suka membaca hal-hal seru*")
    st.markdown("---")
    
    st.subheader("📚 Koleksi Novel Tersedia")
    if not db["daftar_novel"]:
        st.info("Belum ada novel yang ditambahkan oleh admin.")
    else:
        for idx, novel in enumerate(db["daftar_novel"]):
            with st.container():
                st.markdown(f"### 📖 {novel['judul']}")
                st.caption(f"Genre: {novel['genre']}")
                if st.button(f"Baca Novel Ini", key=f"baca_home_{idx}"):
                    st.session_state.selected_novel = novel
                    st.session_state.menu = "DetailNovel"
                    st.rerun()
                st.markdown("---")

# --- HALAMAN DETAIL & BACA NOVEL ---
elif menu_pilihan == "DetailNovel" or st.session_state.selected_novel:
    novel = st.session_state.selected_novel
    if st.button("⬅️ Kembali ke Beranda"):
        st.session_state.selected_novel = None
        st.session_state.selected_bab = None
        st.rerun()
        
    if st.session_state.selected_bab is None:
        st.title(f"📖 {novel['judul']}")
        st.markdown(f"**Genre/Deskripsi:** {novel['genre']}")
        st.markdown("---")
        
        st.subheader("Daftar Bab")
        if not novel['babad']:
            st.info("Belum ada bab yang tersedia untuk novel ini.")
        else:
            for b_idx, bab in enumerate(novel['babad']):
                if st.button(f"Bab: {bab['nama_bab']}", key=f"bab_{b_idx}"):
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
elif menu_pilihan == "Login":
    st.title("🔑 User Login")
    with st.form("form_login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_login = st.form_submit_button("Login")
        
        if submit_login:
            users = db["users_terdaftar"]
            if username in users and users[username] == password:
                st.success(f"Berhasil login sebagai {username}!")
            else:
                st.error("Username atau Password salah!")

# --- HALAMAN REGISTRASI ---
elif menu_pilihan == "Registrasi Akun":
    st.title("📝 Registrasi Akun Baru")
    
    tab1, tab2 = st.tabs(["1. Ajukan ID Sementara", "2. Edit Akun (Aktivasi)"])
    
    with tab1:
        st.markdown("Masukkan ID sementara Anda untuk mendapatkan nomor antrean dan menunggu kode dari admin.")
        with st.form("form_reg"):
            id_sementara = st.text_input("ID Sementara / Nama Lengkap")
            submit_reg = st.form_submit_button("Kirim Pengajuan ID")
            
            if submit_reg:
                if not id_sementara:
                    st.warning("ID tidak boleh kosong!")
                else:
                    existing = next((item for item in db["antrian_registrasi"] if item['id'] == id_sementara), None)
                    if existing:
                        idx_antri = db["antrian_registrasi"].index(existing) + 1
                        st.info(f"ID sudah terdaftar dalam antrean.\nNomor Antrean Anda: #{idx_antri}\nKode Admin: {existing.get('kode', 'Belum dikirim')}")
                    else:
                        db["antrian_registrasi"].append({"id": id_sementara, "kode": "", "username": "", "password": ""})
                        simpan_data(db)
                        st.success(f"Pengajuan berhasil dikirim! Nomor Antrean Anda: #{len(db['antrian_registrasi'])}")
                        
    with tab2:
        st.markdown("Jika Anda sudah mendapatkan **Kode dari Admin**, masukkan data di bawah untuk mengatur Username & Password Anda.")
        with st.form("form_edit_akun"):
            id_input = st.text_input("ID Anda yang terdaftar")
            kode_input = st.text_input("Kode dari Admin")
            new_user = st.text_input("Username Baru")
            new_pass = st.text_input("Password Baru", type="password")
            submit_aktivasi = st.form_submit_button("Simpan & Aktifkan Akun")
            
            if submit_aktivasi:
                target = next((item for item in db["antrian_registrasi"] if item['id'] == id_input), None)
                if not target:
                    st.error("ID tidak ditemukan dalam antrean pengajuan!")
                elif target.get('kode') != kode_input:
                    st.error("Kode dari admin salah atau belum dikirimkan!")
                elif new_user in db["users_terdaftar"]:
                    st.error("Username sudah digunakan oleh akun lain!")
                else:
                    db["users_terdaftar"][new_user] = new_pass
                    db["antrian_registrasi"].remove(target)
                    simpan_data(db)
                    st.success("Akun berhasil diaktifkan! Silakan pindah ke menu Login.")

# --- HALAMAN ADMIN DASHBOARD ---
elif menu_pilihan == "Admin Dashboard":
    st.title("📊 Admin Dashboard")
    pass_admin = st.text_input("Masukkan Password Admin (Pass: admin)", type="password")
    
    if pass_admin == "admin":
        st.success("Akses Admin Diberikan!")
        
        tab_adm1, tab_adm2, tab_adm3 = st.tabs(["📚 Kelola Novel & Bab", "👥 Data User & Antrean", "➕ Tambah Novel Baru"])
        
        with tab_adm1:
            st.subheader("Daftar Novel & Tambah Bab")
            if not db["daftar_novel"]:
                st.info("Belum ada novel.")
            else:
                for n_idx, novel in enumerate(db["daftar_novel"]):
                    with st.expander(f"{novel['judul']} ({novel['genre']})"):
                        if st.button(f"Hapus Novel Ini", key=f"del_nov_{n_idx}"):
                            db["daftar_novel"].remove(novel)
                            simpan_data(db)
                            st.rerun()
                            
                        st.markdown("--- **Tambah Bab Baru** ---")
                        with st.form(f"form_bab_{n_idx}"):
                            nama_bab = st.text_input("Nama Bab (Cth: Bab 1)", key=f"nb_{n_idx}")
                            isi_cerita = st.text_area("Isi Cerita Lengkap", key=f"ic_{n_idx}")
                            submit_bab = st.form_submit_button("Simpan Bab")
                            if submit_bab:
                                if nama_bab and isi_cerita:
                                    novel['babad'].append({"nama_bab": nama_bab, "isi": isi_cerita})
                                    simpan_data(db)
                                    st.success("Bab berhasil ditambahkan!")
                                    st.rerun()
                                else:
                                    st.warning("Semua kolom harus diisi!")
                                    
        with tab_adm2:
            st.subheader("Antrean Pengajuan User")
            if not db["antrian_registrasi"]:
                st.info("Tidak ada pengajuan antrean.")
            else:
                for a_idx, req in enumerate(db["antrian_registrasi"]):
                    col1, col2 = st.columns([2, 1])
                    col1.write(f"ID: **{req['id']}**")
                    k_val = col2.text_input("Kode", value=req.get('kode', ''), key=f"k_val_{a_idx}")
                    if st.button(f"Kirim Kode untuk {req['id']}", key=f"btn_k_{a_idx}"):
                        req['kode'] = k_val
                        simpan_data(db)
                        st.success("Kode berhasil disimpan!")
                        st.rerun()
                    st.markdown("---")
                    
            st.subheader("Database User Terdaftar")
            for u_key, u_val in db["users_terdaftar"].items():
                if u_key != "admin":
                    st.write(f"- Username: **{u_key}** | Password: **{u_val}**")

        with tab_adm3:
            st.subheader("Tambah Novel Baru")
            with st.form("form_add_novel"):
                j_nov = st.text_input("Judul Novel")
                g_nov = st.text_input("Deskripsi / Genre")
                submit_nov = st.form_submit_button("Simpan Novel")
                
                if submit_nov:
                    if j_nov and g_nov:
                        db["daftar_novel"].append({"judul": j_nov, "genre": g_nov, "babad": []})
                        simpan_data(db)
                        st.success("Novel berhasil ditambahkan!")
                        st.rerun()
                    else:
                        st.warning("Judul dan genre harus diisi!")
    elif pass_admin != "":
        st.error("Password Admin Salah!")