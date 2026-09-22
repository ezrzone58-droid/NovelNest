import streamlit as st
import json
import os
import uuid

st.set_page_config(
    page_title="NovelNest - Web Edition",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

FILE_DATABASE = "novelnest_data.json"

def muat_data():
    if os.path.exists(FILE_DATABASE):
        try:
            with open(FILE_DATABASE, "r", encoding="utf-8") as f:
                data = json.load(f)

                return {
                    "tema": data.get("tema", "biru"),
                    "daftar_novel": data.get("daftar_novel", []),
                    "antrian_registrasi": data.get("antrian_registrasi", []),
                    "users_terdaftar": data.get(
                        "users_terdaftar",
                        {"admin": "admin"}
                    ),
                    "active_sessions": data.get("active_sessions", {})
                }

        except Exception as e:
            st.error(f"Gagal memuat data: {e}")

    return {
        "tema": "biru",
        "daftar_novel": [],
        "antrian_registrasi": [],
        "users_terdaftar": {"admin": "admin"},
        "active_sessions": {}
    }

def simpan_data(data):
    try:
        with open(FILE_DATABASE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    except Exception as e:
        st.error(f"Gagal menyimpan data: {e}")

if "db" not in st.session_state:
    st.session_state.db = muat_data()

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

if "menu" not in st.session_state:
    st.session_state.menu = "Utama"

if "selected_novel" not in st.session_state:
    st.session_state.selected_novel = None

if "selected_bab" not in st.session_state:
    st.session_state.selected_bab = None

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

if "admin_step" not in st.session_state:
    st.session_state.admin_step = 0

if "show_theme_modal" not in st.session_state:
    st.session_state.show_theme_modal = False

if "aktivasi_step" not in st.session_state:
    st.session_state.aktivasi_step = "input_id"

if "temp_validated_id" not in st.session_state:
    st.session_state.temp_validated_id = ""

tema = db.get("tema", "biru")

if tema == "merah":
    bg_utama = "#121212"
    fg_teks = "#f3f4f6"
    accent_btn = "#dc2626"
    box_bg = "#27272a"
    muted_color = "#d1d5db"
elif tema == "hijau":
    bg_utama = "#f0fdf4"
    fg_teks = "#022c22"
    accent_btn = "#059669"
    box_bg = "#d1fae5"
    muted_color = "#065f46"
elif tema == "ungu":
    bg_utama = "#faf5ff"
    fg_teks = "#2e1065"
    accent_btn = "#7c3aed"
    box_bg = "#f3e8ff"
    muted_color = "#581c87"
else:
    bg_utama = "#f4f6f8"
    fg_teks = "#0f172a"
    accent_btn = "#2563eb"
    box_bg = "#e2e8f0"
    muted_color = "#334155"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {bg_utama};
        color: {fg_teks};
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }}
    div.stButton > button {{
        background-color: {accent_btn};
        color: white;
        border-radius: 6px;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        width: 100%;
    }}
    div.stButton > button:hover {{
        opacity: 0.9;
    }}
    /* Kontras Tinggi untuk Kolom Input & Textarea */
    input, textarea, div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea {{
        background-color: #ffffff !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        border-radius: 6px !important;
        border: 2px solid #2563eb !important;
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
        border: 2px solid #2563eb !important;
        font-weight: 600 !important;
    }}
    div[data-baseweb="select"] span {{
        color: #000000 !important;
    }}
    p, span, label, h1, h2, h3, h4 {{
        color: {fg_teks} !important;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ==================== KONTROL ALUR APLIKASI ====================
if st.session_state.is_admin:
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #1e293b, #0f172a); padding: 25px; border-radius: 10px; color: white; margin-bottom: 25px; border-left: 6px solid #3b82f6;">
            <h1 style="color: #ffffff; margin: 0; font-size: 28px;">🔐 Panel Kontrol Administrator</h1>
            <p style="color: #94a3b8; margin: 5px 0 0 0;">Sistem Manajemen Pusat NovelNest — Kontrol Penuh Data dan Pengguna</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_adm_ctrl1, col_adm_ctrl2 = st.columns(2)
    with col_adm_ctrl1:
        if st.button("🚪 Keluar Sepenuhnya dari Admin"):
            st.session_state.is_admin = False
            st.success("Berhasil keluar dari mode admin.")
            st.rerun()
    with col_adm_ctrl2:
        if st.button("🔄 Muat Ulang Dashboard (Pertahankan Admin)"):
            st.session_state.db = muat_data()
            st.success("Dashboard dimuat ulang, status admin dipertahankan!")
            st.rerun()

    st.markdown("---")

    tab_a, tab_b, tab_c = st.tabs(["📚 Kelola Novel", "📖 Kelola Bab", "👥 Data User dan Antrean"])

    with tab_a:
        st.subheader("Tambah Novel Baru")
        with st.form("tambah_novel_form"):
            jdl = st.text_input("Judul Novel")
            gnr = st.text_input("Deskripsi / Genre")
            if st.form_submit_button("Simpan Novel"):
                if jdl and gnr:
                    db["daftar_novel"].append({"judul": jdl, "genre": gnr, "babad": []})
                    simpan_data(db)
                    st.success("Novel baru berhasil ditambahkan.")
                    st.rerun()
                else:
                    st.warning("Judul dan genre wajib diisi.")

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
            pilih_nov_nama = st.selectbox("Pilih Novel", [n["judul"] for n in db["daftar_novel"]])
            target_n = next(n for n in db["daftar_novel"] if n["judul"] == pilih_nov_nama)
            
            st.markdown("**Bab Terdaftar & Pengaturan:**")
            if not target_n["babad"]:
                st.caption("Belum ada bab.")
            else:
                for b_idx, b_item in enumerate(target_n["babad"]):
                    with st.expander(f"{b_item['nama_bab']}"):
                        with st.form(f"form_edit_bab_{b_idx}"):
                            edit_nama_b = st.text_input("Judul Bab", value=b_item['nama_bab'])
                            edit_isi_b = st.text_area("Isi Cerita Lengkap", value=b_item['isi'], height=150)
                            
                            col_b1, col_b2 = st.columns(2)
                            simpan_edit = col_b1.form_submit_button("Simpan Perubahan")
                            hapus_bab_btn = col_b2.form_submit_button("Hapus Bab Ini")
                            
                            if simpan_edit:
                                if edit_nama_b and edit_isi_b:
                                    b_item['nama_bab'] = edit_nama_b
                                    b_item['isi'] = edit_isi_b
                                    simpan_data(db)
                                    st.success("Bab berhasil diperbarui.")
                                    st.rerun()
                                else:
                                    st.warning("Judul bab dan isi cerita wajib diisi.")
                            if hapus_bab_btn:
                                target_n['babad'].remove(b_item)
                                simpan_data(db)
                                st.success("Bab berhasil dihapus.")
                                st.rerun()

            st.markdown("---")
            with st.form("tambah_bab_form"):
                st.subheader("Tambah Bab Baru")
                nama_b = st.text_input("Nama Bab (Contoh: Bab 1)")
                isi_b = st.text_area("Isi Cerita Lengkap", height=150)
                if st.form_submit_button("Simpan Bab Baru"):
                    if nama_b and isi_b:
                        target_n["babad"].append({"nama_bab": nama_b, "isi": isi_b, "komentar": [], "balasan": []})
                        simpan_data(db)
                        st.success("Bab berhasil disimpan.")
                        st.rerun()
                    else:
                        st.warning("Nama bab dan isi cerita wajib diisi.")

    with tab_c:
        col_head_a, col_head_b = st.columns([3, 1])
        col_head_a.subheader("Antrean Registrasi Pengajuan User")
        if col_head_b.button("🔄 Muat Ulang", key="btn_restart_admin"):
            st.session_state.db = muat_data()
            st.success("Data diperbarui!")
            st.rerun()

        if not db["antrian_registrasi"]:
            st.info("Tidak ada antrean registrasi.")
        else:
            if st.button("🗑️ Hapus Semua Antrean Menumpuk", key="btn_clear_queue"):
                db["antrian_registrasi"] = []
                simpan_data(db)
                st.success("Semua antrean registrasi berhasil dibersihkan.")
                st.rerun()
            st.markdown("---")

            for q_idx, req in enumerate(db["antrian_registrasi"]):
                col_1, col_2, col_3 = st.columns([2, 1, 1])
                col_1.write(f"ID Pengguna: **{req['id']}**")
                kode_inputan = col_2.text_input("Kode Verifikasi", value=req.get("kode", ""), key=f"q_kode_{q_idx}")
                if col_3.button("Kirim Kode", key=f"btn_q_{q_idx}"):
                    req["kode"] = kode_inputan
                    simpan_data(db)
                    st.success(f"Kode untuk ID {req['id']} berhasil dikirim.")
                    st.rerun()
                st.markdown("---")

        col_sub_u1, col_sub_u2 = st.columns([3, 1])
        col_sub_u1.subheader("Database User Aktif")
        if col_sub_u2.button("🔄 Muat Ulang User", key="btn_restart_users_list"):
            st.session_state.db = muat_data()
            st.success("Daftar user diperbarui!")
            st.rerun()

        active_users = {k: v for k, v in db["users_terdaftar"].items() if k != "admin"}
        if not active_users:
            st.info("Belum ada user terdaftar selain admin.")
        else:
            for usr, pwd in active_users.items():
                col_u1, col_u2, col_u3 = st.columns([2, 1, 1])
                col_u1.write(f"- Username: **{usr}** | Password: **{pwd}**")
                new_pwd_input = col_u2.text_input("Password Baru", type="password", key=f"reset_pwd_{usr}")
                if col_u2.button("Reset Password", key=f"btn_reset_{usr}"):
                    if new_pwd_input.strip():
                        db["users_terdaftar"][usr] = new_pwd_input.strip()
                        simpan_data(db)
                        st.success(f"Password untuk user {usr} berhasil direset.")
                        st.rerun()
                    else:
                        st.warning("Masukkan password baru terlebih dahulu.")
                if col_u3.button("Hapus Akun", key=f"btn_del_usr_{usr}"):
                    del db["users_terdaftar"][usr]
                    simpan_data(db)
                    st.success(f"Akun {usr} berhasil dihapus.")
                    st.rerun()

else:
    # ==================== HALAMAN UTAMA (LANDING PAGE) ====================
    if st.session_state.menu == "Utama":
        # Tombol Setting di Kiri Atas
        col_top_left, col_top_right = st.columns([1, 5])
        with col_top_left:
            if st.button("⚙️"):
                st.session_state.show_theme_modal = not st.session_state.show_theme_modal
                st.rerun()

        if st.session_state.show_theme_modal:
            st.markdown("### Pengaturan Tema Aplikasi")
            pilihan_tema = st.selectbox(
                "Pilih Tema Warna",
                ["biru", "merah", "hijau", "ungu"],
                index=["biru", "merah", "hijau", "ungu"].index(tema)
            )
            if pilihan_tema != tema:
                db["tema"] = pilihan_tema
                simpan_data(db)
                st.rerun()
            st.markdown("---")

        st.markdown(
            """
            <div style="text-align: center; padding: 40px 20px 20px 20px;">
                <h1 style="font-weight: 800; font-size: 48px; margin-bottom: 10px;">NovelNest</h1>
                <p style="font-size: 18px; font-style: italic; color: #94a3b8; font-weight: 500; max-width: 600px; margin: 0 auto 35px auto;">
                    Rumah digital bagi para pembaca untuk menikmati berbagai cerita menarik, berdiskusi, dan menjelajahi bab-bab seru.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Dua tombol di tengah, sejajar, dan berukuran sama berdampingan
        col_space_l, col_btn1, col_btn2, col_space_r = st.columns([1, 1.5, 1.5, 1])
        with col_btn1:
            if st.button("🔑 Masuk", use_container_width=True):
                st.session_state.menu = "Login"
                st.rerun()
        with col_btn2:
            if st.button("📝 Registrasi", use_container_width=True):
                st.session_state.menu = "Registrasi"
                st.rerun()

    # ==================== HALAMAN LOGIN ====================
    elif st.session_state.menu == "Login":
        if st.button("← Kembali ke Beranda Utama"):
            st.session_state.menu = "Utama"
            st.session_state.admin_step = 0
            st.rerun()

        st.title("Masuk ke Akun NovelNest")

        if st.session_state.logged_in_user:
            st.info(f"Anda sudah masuk sebagai **{st.session_state.logged_in_user}**.")
            if st.button("🚀 Buka Koleksi Novel Sekarang", use_container_width=True):
                st.session_state.menu = "Koleksi Novel"
                st.rerun()
        else:
            if st.session_state.admin_step == 1:
                st.info("Deteksi akses administrator. Masukkan verifikasi lapis pertama.")
                with st.form("form_verif_1"):
                    v1 = st.text_input("Password Lapis 1:", type="password")
                    if st.form_submit_button("Lanjutkan"):
                        if v1 == "123":
                            st.session_state.admin_step = 2
                            st.rerun()
                        else:
                            st.error("Password lapis pertama salah.")
                            st.session_state.admin_step = 0

            elif st.session_state.admin_step == 2:
                st.info("Verifikasi lapis kedua diperlukan.")
                with st.form("form_verif_2"):
                    v2 = st.text_input("Password Lapis 2:", type="password")
                    if st.form_submit_button("Masuk Admin"):
                        if v2 == "321":
                            st.session_state.is_admin = True
                            st.session_state.admin_step = 0
                            st.success("Verifikasi sukses! Membuka Admin Dashboard...")
                            st.rerun()
                        else:
                            st.error("Password lapis kedua salah.")
                            st.session_state.admin_step = 0

            else:
                with st.form("form_user_login"):
                    u_name = st.text_input("Username")
                    u_pass = st.text_input("Password", type="password")
                    
                    submitted_login = st.form_submit_button("Masuk")
                    if submitted_login:
                        if u_name == "admin" and u_pass == "admin":
                            st.session_state.admin_step = 1
                            st.rerun()
                        else:
                            registered = db["users_terdaftar"]
                            if u_name in registered and registered[u_name] == u_pass:
                                st.session_state.logged_in_user = u_name
                                db.setdefault("active_sessions", {})[current_device_token] = u_name
                                simpan_data(db)
                                st.success(f"Berhasil masuk sebagai {u_name}.")
                                st.rerun()
                            else:
                                st.error("Username atau Password salah.")

    # ==================== HALAMAN REGISTRASI ====================
    elif st.session_state.menu == "Registrasi":
        if st.button("← Kembali ke Beranda Utama"):
            st.session_state.menu = "Utama"
            st.rerun()

        st.title("Registrasi Akun NovelNest")
        st.markdown("Pilih tahapan registrasi di bawah ini:")

        t_reg1, t_reg2 = st.tabs(["1. Ajukan ID Pengguna", "2. Aktivasi & Ubah Profil"])

        with t_reg1:
            st.subheader("Pengajuan ID Pengguna")
            st.write("Masukkan ID Pengguna unik Anda (gunakan nama samaran/ID unik, bukan nama asli).")

            col_r_left, col_r_right = st.columns([2, 1])
            with col_r_left:
                with st.form("form_ajukan_id"):
                    id_temp = st.text_input("Masukkan ID Pengguna:")
                    
                    col_btn_sub, col_btn_res = st.columns(2)
                    sub_pengajuan = col_btn_sub.form_submit_button("Kirim Pengajuan")
                    btn_restart_code = col_btn_res.form_submit_button("🔄 Muat Ulang Kode")

                    if sub_pengajuan:
                        if not id_temp:
                            st.warning("ID Pengguna tidak boleh kosong.")
                        else:
                            found_req = next((x for x in db["antrian_registrasi"] if x["id"] == id_temp), None)
                            if found_req:
                                st.info(f"ID sudah terdaftar dalam antrean.")
                            else:
                                db["antrian_registrasi"].append({"id": id_temp, "kode": "", "username": "", "password": ""})
                                simpan_data(db)
                                st.success("Pengajuan berhasil dikirim.")
                                st.rerun()

                    if btn_restart_code:
                        st.session_state.db = muat_data()
                        st.success("Status antrean & kode berhasil dimuat ulang!")
                        st.rerun()

            with col_r_right:
                st.markdown("#### Panel Status")
                st.markdown(
                    f"""
                    <div style="background-color: {box_bg}; padding: 12px; border-radius: 6px; margin-bottom: 10px;">
                        <span style="font-size: 12px; font-weight: bold;">Nomor Antrean Pengguna:</span><br>
                        <span style="font-size: 20px; font-weight: bold;">{len(db['antrian_registrasi'])}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"""
                    <div style="background-color: {box_bg}; padding: 12px; border-radius: 6px;">
                        <span style="font-size: 12px; font-weight: bold;">Kode Verifikasi Admin:</span><br>
                        <span style="font-size: 14px;">Klik Muat Ulang untuk melihat kode jika sudah dikirimkan admin.</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with t_reg2:
            st.subheader("Aktivasi Akun & Ubah Profil")

            if st.session_state.aktivasi_step == "input_id":
                st.write("Kolom di bawah ini wajib diisi dengan ID Pengguna yang sebelumnya telah diajukan dan dikirimi kode oleh admin.")
                with st.form("form_cek_id_aktivasi"):
                    check_id = st.text_input("ID Pengguna Anda:")
                    if st.form_submit_button("Lanjutkan Verifikasi"):
                        target_q = next((x for x in db["antrian_registrasi"] if x["id"] == check_id), None)
                        if target_q and target_q.get("kode"):
                            st.session_state.temp_validated_id = check_id
                            st.session_state.aktivasi_step = "konfirmasi_id"
                            st.rerun()
                        else:
                            st.error("ID tidak ditemukan atau kode verifikasi belum dikirimkan oleh admin.")

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
                    inp_kode = st.text_input("Masukkan Kode Verifikasi dari Admin:")
                    inp_new_u = st.text_input("Username Baru:")
                    inp_new_p = st.text_input("Password Baru:", type="password")

                    if st.form_submit_button("Simpan Perubahan Akun"):
                        if not target_q or target_q.get("kode") != inp_kode:
                            st.error("Kode verifikasi salah.")
                        elif inp_new_u in db["users_terdaftar"]:
                            st.error("Username tersebut sudah digunakan orang lain.")
                        else:
                            db["users_terdaftar"][inp_new_u] = inp_new_p
                            db["antrian_registrasi"].remove(target_q)
                            simpan_data(db)
                            
                            st.session_state.aktivasi_step = "input_id"
                            st.session_state.temp_validated_id = ""
                            st.session_state.menu = "Login"
                            st.success("Akun berhasil diaktifkan! Dialihkan ke halaman Login...")
                            st.rerun()

    # ==================== KOLEKSI NOVEL ====================
    elif st.session_state.menu == "Koleksi Novel":
        if st.button("← Keluar ke Beranda Utama"):
            st.session_state.menu = "Utama"
            st.rerun()

        if not st.session_state.logged_in_user:
            st.warning("Anda harus masuk (login) terlebih dahulu melalui menu 'Masuk' untuk membaca koleksi novel.")
            if st.button("Pindah ke Halaman Login"):
                st.session_state.menu = "Login"
                st.rerun()
        else:
            st.title("NovelNest Library")
            st.markdown(f"Status Login: **{st.session_state.logged_in_user}**")
            st.markdown("---")

            if st.session_state.selected_novel is None:
                st.subheader("Pilih Novel Favorit Anda:")
                if not db["daftar_novel"]:
                    st.info("Belum ada novel tersedia.")
                else:
                    for idx_n, n_item in enumerate(db["daftar_novel"]):
                        if st.button(f"{n_item['judul']} [{n_item['genre']}]", key=f"pilih_n_{idx_n}", use_container_width=True):
                            st.session_state.selected_novel = n_item
                            st.rerun()
            else:
                current_novel = st.session_state.selected_novel
                if st.button("Kembali ke Daftar Novel"):
                    st.session_state.selected_novel = None
                    st.session_state.selected_bab = None
                    st.rerun()

                if st.session_state.selected_bab is None:
                    st.title(f"{current_novel['judul']}")
                    st.markdown(f"**Genre/Deskripsi:** {current_novel['genre']}")
                    st.markdown("---")
                    st.subheader("Daftar Bab Tersedia")
                    if not current_novel["babad"]:
                        st.info("Belum ada bab yang ditulis untuk novel ini.")
                    else:
                        for idx_b, b_item in enumerate(current_novel["babad"]):
                            if st.button(f"{b_item['nama_bab']}", key=f"buka_b_{idx_b}"):
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
                        <div style="background-color: {box_bg}; color: {fg_teks}; padding: 25px; border-radius: 8px; line-height: 1.6; white-space: pre-wrap; font-weight: 500;">
{current_bab['isi']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown("---")
                    st.subheader("Kolom Komentar")

                    if "komentar" not in current_bab:
                        current_bab["komentar"] = []

                    with st.form("form_tambah_komentar"):
                        isi_komentar = st.text_area("Tulis komentar Anda...")
                        if st.form_submit_button("Kirim Komentar"):
                            if isi_komentar.strip():
                                current_bab["komentar"].append({
                                    "user": st.session_state.logged_in_user,
                                    "pesan": isi_komentar.strip(),
                                    "balasan": []
                                })
                                simpan_data(db)
                                st.success("Komentar berhasil dikirim.")
                                st.rerun()
                            else:
                                st.warning("Komentar tidak boleh kosong.")

                    if not current_bab["komentar"]:
                        st.info("Belum ada komentar di bab ini.")
                    else:
                        for idx_k, kom in enumerate(current_bab["komentar"]):
                            if "balasan" not in kom:
                                kom["balasan"] = []
                            st.markdown(
                                f"""
                                <div style="background-color: {box_bg}; padding: 12px; border-radius: 6px; margin-bottom: 10px;">
                                    <strong>{kom['user']}</strong><br>{kom['pesan']}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            for bal in kom["balasan"]:
                                st.markdown(
                                    f"""
                                    <div style="background-color: rgba(0,0,0,0.05); padding: 8px 10px; border-radius: 6px; margin-left: 30px; margin-bottom: 6px; border-left: 3px solid {accent_btn};">
                                        <span style="font-size: 13px;">↳ <strong>{bal['user']}</strong>: {bal['pesan']}</span>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                            with st.form(f"form_balas_{idx_k}"):
                                pesan_balasan = st.text_input("Balas komentar ini...", key=f"input_balas_{idx_k}")
                                if st.form_submit_button("Kirim Balasan"):
                                    if pesan_balasan.strip():
                                        kom["balasan"].append({
                                            "user": st.session_state.logged_in_user,
                                            "pesan": pesan_balasan.strip()
                                        })
                                        simpan_data(db)
                                        st.success("Balasan berhasil dikirim.")
                                        st.rerun()
                                    else:
                                        st.warning("Balasan tidak boleh kosong.")
                            st.markdown("---")
