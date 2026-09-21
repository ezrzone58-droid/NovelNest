import streamlit as st
import json
import os

st.set_page_config(
    page_title="NovelNest - Web Edition",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
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
                    "current_session": data.get("current_session", None)
                }

        except Exception as e:
            st.error(f"Gagal memuat data: {e}")

    return {
        "tema": "biru",
        "daftar_novel": [],
        "antrian_registrasi": [],
        "users_terdaftar": {"admin": "admin"},
        "current_session": None
    }

def simpan_data(data):
    try:
        with open(FILE_DATABASE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    except Exception as e:
        st.error(f"Gagal menyimpan data: {e}")

if "db" not in st.session_state:
    st.session_state.db = muat_data()

# Sinkronkan session login dari database jika belum ada di session_state
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = st.session_state.db.get("current_session", None)

if "menu" not in st.session_state:
    st.session_state.menu = "Beranda"

if "selected_novel" not in st.session_state:
    st.session_state.selected_novel = None

if "selected_bab" not in st.session_state:
    st.session_state.selected_bab = None

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

if "admin_step" not in st.session_state:
    st.session_state.admin_step = 0

if "show_theme_selector" not in st.session_state:
    st.session_state.show_theme_selector = False

if "show_panduan" not in st.session_state:
    st.session_state.show_panduan = False

db = st.session_state.db

tema = db.get("tema", "biru")

if tema == "merah":
    bg_sidebar = "#18181b"
    bg_utama = "#121212"
    fg_teks = "#f3f4f6"
    accent_btn = "#dc2626"
    box_bg = "#27272a"
    muted_color = "#d1d5db"

elif tema == "hijau":
    bg_sidebar = "#064e3b"
    bg_utama = "#f0fdf4"
    fg_teks = "#022c22"
    accent_btn = "#059669"
    box_bg = "#d1fae5"
    muted_color = "#065f46"

elif tema == "ungu":
    bg_sidebar = "#3b0764"
    bg_utama = "#faf5ff"
    fg_teks = "#2e1065"
    accent_btn = "#7c3aed"
    box_bg = "#f3e8ff"
    muted_color = "#581c87"

else:
    bg_sidebar = "#0f172a"
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

    [data-testid="stSidebar"] {{
        background-color: {bg_sidebar};
        padding-top: 0px !important;
    }}

    [data-testid="stSidebar"]::before {{
        content: "";
        display: block;
        height: 45px;
        background-color: {bg_sidebar};
        width: 100%;
        position: relative;
        z-index: 999;
    }}

    [data-testid="stSidebarCollapseButton"] .material-icons,
    [data-testid="stSidebarCollapseButton"] .material-symbols-rounded,
    [data-testid="stSidebarCollapseButton"] .material-symbols-outlined,
    [data-testid="stSidebarCollapseButton"] .material-symbols-sharp {{
        font-size: 0 !important;
        line-height: 0 !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
        visibility: hidden !important;
    }}

    [data-testid="stSidebarCollapseButton"] span {{
        font-size: 0 !important;
        line-height: 0 !important;
        overflow: hidden !important;
    }}

    [data-testid="stSidebarCollapseButton"] {{
        min-width: 40px !important;
        min-height: 40px !important;
    }}

    [data-testid="stSidebar"] * {{
        color: #ffffff !important;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }}

    div.stButton > button {{
        background-color: {accent_btn};
        color: white;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        width: 100%;
    }}

    div.stButton > button:hover {{
        opacity: 0.9;
    }}

    input,
    textarea {{
        background-color: {box_bg} !important;
        color: {fg_teks} !important;
        border-radius: 6px !important;
        border: 1px solid rgba(0,0,0,0.2) !important;
    }}

    p,
    span,
    label {{
        color: {fg_teks} !important;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }}

    div[data-baseweb="select"] > div {{
        background-color: {box_bg} !important;
        color: {fg_teks} !important;
    }}

    button[data-baseweb="tab"] {{
        color: {fg_teks} !important;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    """
    <h2 style="
        text-align: center;
        letter-spacing: 1px;
        font-weight: 700;
        margin-top: -10px;
    ">
        NovelNest
    </h2>
    """,
    unsafe_allow_html=True
)

# Indikator status login di sidebar
if st.session_state.logged_in_user:
    st.sidebar.markdown(
        f"""
        <div style="background-color: rgba(255,255,255,0.1); padding: 8px; border-radius: 6px; text-align: center; margin-bottom: 10px;">
            <span style="font-size: 12px;">Masuk sebagai:</span><br>
            <strong>{st.session_state.logged_in_user}</strong>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.sidebar.button("🚪 Keluar (Logout)"):
        st.session_state.logged_in_user = None
        st.session_state.is_admin = False
        db["current_session"] = None
        simpan_data(db)
        st.success("Berhasil keluar.")
        st.rerun()

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    <p style="
        font-size: 11px;
        color: #cbd5e1;
        text-transform: uppercase;
        font-weight: 600;
    ">
        Menu Navigasi
    </p>
    """,
    unsafe_allow_html=True
)

navigasi = st.sidebar.radio(
    "Navigasi",
    [
        "Beranda",
        "Masuk (Login)",
        "Registrasi Akun",
        "Koleksi Novel"
    ]
    + (["Admin Dashboard"] if st.session_state.is_admin else []),
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

if st.sidebar.button("⚙️ Setting Aplikasi"):
    st.session_state.show_theme_selector = (
        not st.session_state.show_theme_selector
    )

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

    st.sidebar.markdown("---")

    if st.sidebar.button("📖 Cara Login & Registrasi"):
        st.session_state.show_panduan = not st.session_state.show_panduan

    if st.session_state.show_panduan:
        st.sidebar.markdown(
            f"""
            <div style="
                background-color: rgba(255, 255, 255, 0.1);
                color: #ffffff;
                padding: 12px;
                border-radius: 6px;
                margin-top: 10px;
                font-size: 13px;
                line-height: 1.5;
            ">
                <strong>Panduan Singkat:</strong><br><br>
                1. <strong>Registrasi</strong>: Masuk ke menu Registrasi Akun, ajukan ID sementara, lalu minta kode verifikasi ke Admin.<br><br>
                2. <strong>Aktivasi</strong>: Masukkan ID dan kode admin di tab aktivasi untuk membuat username & password.<br><br>
                3. <strong>Login</strong>: Gunakan akun baru Anda pada menu Masuk (Login) untuk mulai membaca novel.
            </div>
            """,
            unsafe_allow_html=True
        )

if navigasi == "Beranda":
    st.markdown(
        """
        <h1 style="
            text-align: center;
            font-weight: 800;
        ">
            NovelNest
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="
            text-align: center;
            padding: 20px 0;
        ">
            <p style="
                font-size: 16px;
                font-style: italic;
                color: {muted_color};
                font-weight: 500;
            ">
                Rumah digital bagi para pembaca untuk
                menikmati berbagai cerita menarik.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

elif navigasi == "Masuk (Login)":
    st.title("User Login")

    if st.session_state.logged_in_user:
        st.info(f"Anda sudah masuk sebagai **{st.session_state.logged_in_user}**. Silakan buka menu **Koleksi Novel** atau klik tombol Logout di sidebar jika ingin berganti akun.")
    else:
        if st.session_state.admin_step == 1:
            st.info(
                "Deteksi akses administrator. "
                "Masukkan verifikasi lapis pertama."
            )

            with st.form("form_verif_1"):
                v1 = st.text_input(
                    "Password Lapis 1 (123):",
                    type="password"
                )

                if st.form_submit_button("Lanjutkan"):
                    if v1 == "123":
                        st.session_state.admin_step = 2
                        st.rerun()
                    else:
                        st.error(
                            "Password lapis pertama salah."
                        )
                        st.session_state.admin_step = 0

        elif st.session_state.admin_step == 2:
            st.info(
                "Verifikasi lapis kedua diperlukan."
            )

            with st.form("form_verif_2"):
                v2 = st.text_input(
                    "Password Lapis 2 (321):",
                    type="password"
                )

                if st.form_submit_button("Masuk Admin"):
                    if v2 == "321":
                        st.session_state.is_admin = True
                        st.session_state.admin_step = 0

                        st.success(
                            "Verifikasi sukses! "
                            "Silakan pilih menu Admin Dashboard di sidebar."
                        )

                        st.rerun()
                    else:
                        st.error(
                            "Password lapis kedua salah."
                        )
                        st.session_state.admin_step = 0

        else:
            with st.form("form_user_login"):
                u_name = st.text_input("Username")

                u_pass = st.text_input(
                    "Password",
                    type="password"
                )

                if st.form_submit_button("Masuk"):
                    if u_name == "admin" and u_pass == "admin":
                        st.session_state.admin_step = 1
                        st.rerun()
                    else:
                        registered = db["users_terdaftar"]

                        if (
                            u_name in registered
                            and registered[u_name] == u_pass
                        ):
                            st.session_state.logged_in_user = u_name
                            db["current_session"] = u_name
                            simpan_data(db)

                            st.success(
                                f"Berhasil masuk sebagai {u_name}. "
                                "Silakan buka menu 'Koleksi Novel'."
                            )
                            st.rerun()
                        else:
                            st.error(
                                "Username atau Password salah."
                            )

elif navigasi == "Admin Dashboard":
    if not st.session_state.is_admin:
        st.error(
            "Akses ditolak! Halaman ini bersifat rahasia."
        )
    else:
        st.title("Admin Dashboard")

        if st.button("Keluar dari Mode Admin"):
            st.session_state.is_admin = False
            st.rerun()

        tab_a, tab_b, tab_c = st.tabs(
            [
                "Kelola Novel",
                "Kelola Bab",
                "Data User dan Antrean"
            ]
        )

        with tab_a:
            st.subheader("Tambah Novel Baru")

            with st.form("tambah_novel_form"):
                jdl = st.text_input(
                    "Judul Novel"
                )

                gnr = st.text_input(
                    "Deskripsi / Genre"
                )

                if st.form_submit_button(
                    "Simpan Novel"
                ):
                    if jdl and gnr:
                        db["daftar_novel"].append(
                            {
                                "judul": jdl,
                                "genre": gnr,
                                "babad": []
                            }
                        )

                        simpan_data(db)

                        st.success(
                            "Novel baru berhasil ditambahkan."
                        )

                        st.rerun()
                    else:
                        st.warning(
                            "Judul dan genre wajib diisi."
                        )

            st.markdown("---")
            st.subheader("Daftar Hapus Novel")

            if not db["daftar_novel"]:
                st.info(
                    "Belum ada novel di database."
                )
            else:
                for idx, nov in enumerate(
                    db["daftar_novel"]
                ):
                    c1, c2 = st.columns([3, 1])

                    c1.write(
                        f"**{nov['judul']}** "
                        f"({nov['genre']})"
                    )

                    if c2.button(
                        "Hapus",
                        key=f"hapus_nov_{idx}"
                    ):
                        db["daftar_novel"].remove(
                            nov
                        )

                        simpan_data(db)

                        st.rerun()

        with tab_b:
            st.subheader(
                "Manajemen Bab Cerita"
            )

            if not db["daftar_novel"]:
                st.info(
                    "Belum ada novel tersedia "
                    "untuk diberi bab."
                )
            else:
                pilih_nov_nama = st.selectbox(
                    "Pilih Novel",
                    [
                        n["judul"]
                        for n in db["daftar_novel"]
                    ]
                )

                target_n = next(
                    n
                    for n in db["daftar_novel"]
                    if n["judul"] == pilih_nov_nama
                )

                st.markdown(
                    "**Bab Terdaftar & Pengaturan:**"
                )

                if not target_n["babad"]:
                    st.caption(
                        "Belum ada bab."
                    )
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
                    nama_b = st.text_input(
                        "Nama Bab (Contoh: Bab 1)"
                    )

                    isi_b = st.text_area(
                        "Isi Cerita Lengkap",
                        height=150
                    )

                    if st.form_submit_button(
                        "Simpan Bab Baru"
                    ):
                        if nama_b and isi_b:
                            target_n["babad"].append(
                                {
                                    "nama_bab": nama_b,
                                    "isi": isi_b,
                                    "komentar": [],
                                    "balasan": []
                                }
                            )

                            simpan_data(db)

                            st.success(
                                "Bab berhasil disimpan."
                            )

                            st.rerun()
                        else:
                            st.warning(
                                "Nama bab dan isi cerita "
                                "wajib diisi."
                            )

        with tab_c:
            st.subheader(
                "Antrean Registrasi Pengajuan User"
            )

            if not db["antrian_registrasi"]:
                st.info(
                    "Tidak ada antrean registrasi."
                )
            else:
                for q_idx, req in enumerate(
                    db["antrian_registrasi"]
                ):
                    col_1, col_2, col_3 = st.columns(
                        [2, 1, 1]
                    )

                    col_1.write(
                        f"ID Sementara: **{req['id']}**"
                    )

                    kode_inputan = col_2.text_input(
                        "Kode Verifikasi",
                        value=req.get("kode", ""),
                        key=f"q_kode_{q_idx}"
                    )

                    if col_3.button(
                        "Kirim Kode",
                        key=f"btn_q_{q_idx}"
                    ):
                        req["kode"] = kode_inputan

                        simpan_data(db)

                        st.success(
                            f"Kode untuk ID {req['id']} "
                            "berhasil dikirim."
                        )

                        st.rerun()

                    st.markdown("---")

            st.subheader(
                "Database User Aktif"
            )

            active_users = {
                k: v
                for k, v in db["users_terdaftar"].items()
                if k != "admin"
            }

            if not active_users:
                st.info(
                    "Belum ada user terdaftar selain admin."
                )
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
                        if db.get("current_session") == usr:
                            db["current_session"] = None
                            st.session_state.logged_in_user = None
                        simpan_data(db)
                        st.success(f"Akun {usr} berhasil dihapus.")
                        st.rerun()

elif navigasi == "Koleksi Novel":
    if not st.session_state.logged_in_user:
        st.warning(
            "Anda harus masuk (login) terlebih dahulu "
            "melalui menu 'Masuk (Login)' untuk membaca "
            "koleksi novel."
        )
    else:
        st.title("NovelNest Library")

        st.markdown(
            f"Status Login: "
            f"**{st.session_state.logged_in_user}**"
        )

        st.markdown("---")

        if st.session_state.selected_novel is None:
            st.subheader(
                "Pilih Novel Favorit Anda:"
            )

            if not db["daftar_novel"]:
                st.info(
                    "Belum ada novel tersedia."
                )
            else:
                for idx_n, n_item in enumerate(
                    db["daftar_novel"]
                ):
                    if st.button(
                        f"{n_item['judul']} "
                        f"[{n_item['genre']}]",
                        key=f"pilih_n_{idx_n}",
                        use_container_width=True
                    ):
                        st.session_state.selected_novel = n_item

                        st.rerun()

        else:
            current_novel = (
                st.session_state.selected_novel
            )

            if st.button(
                "Kembali ke Daftar Novel"
            ):
                st.session_state.selected_novel = None
                st.session_state.selected_bab = None

                st.rerun()

            if st.session_state.selected_bab is None:
                st.title(
                    f"{current_novel['judul']}"
                )

                st.markdown(
                    f"**Genre/Deskripsi:** "
                    f"{current_novel['genre']}"
                )

                st.markdown("---")

                st.subheader(
                    "Daftar Bab Tersedia"
                )

                if not current_novel["babad"]:
                    st.info(
                        "Belum ada bab yang ditulis "
                        "untuk novel ini."
                    )
                else:
                    for idx_b, b_item in enumerate(
                        current_novel["babad"]
                    ):
                        if st.button(
                            f"{b_item['nama_bab']}",
                            key=f"buka_b_{idx_b}"
                        ):
                            st.session_state.selected_bab = b_item

                            st.rerun()

            else:
                current_bab = (
                    st.session_state.selected_bab
                )

                if st.button(
                    "Kembali ke Daftar Bab"
                ):
                    st.session_state.selected_bab = None

                    st.rerun()

                st.markdown(
                    f"### {current_novel['judul']} "
                    f"— {current_bab['nama_bab']}"
                )

                st.markdown("---")

                st.markdown(
                    f"""
                    <div style="
                        background-color: {box_bg};
                        color: {fg_teks};
                        padding: 25px;
                        border-radius: 8px;
                        line-height: 1.6;
                        white-space: pre-wrap;
                        font-weight: 500;
                    ">
{current_bab['isi']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown("---")

                st.subheader(
                    "Kolom Komentar"
                )

                if "komentar" not in current_bab:
                    current_bab["komentar"] = []

                with st.form(
                    "form_tambah_komentar"
                ):
                    isi_komentar = st.text_area(
                        "Tulis komentar Anda..."
                    )

                    submit_komentar = (
                        st.form_submit_button(
                            "Kirim Komentar"
                        )
                    )

                    if submit_komentar:
                        if isi_komentar.strip():
                            current_bab[
                                "komentar"
                            ].append(
                                {
                                    "user": (
                                        st.session_state
                                        .logged_in_user
                                    ),
                                    "pesan": (
                                        isi_komentar.strip()
                                    ),
                                    "balasan": []
                                }
                            )

                            simpan_data(db)

                            st.success(
                                "Komentar berhasil dikirim."
                            )

                            st.rerun()

                        else:
                            st.warning(
                                "Komentar tidak boleh kosong."
                            )

                if not current_bab["komentar"]:
                    st.info(
                        "Belum ada komentar di bab ini."
                    )

                else:
                    for idx_k, kom in enumerate(current_bab["komentar"]):
                        if "balasan" not in kom:
                            kom["balasan"] = []
                            
                        st.markdown(
                            f"""
                            <div style="
                                background-color: {box_bg};
                                padding: 12px;
                                border-radius: 6px;
                                margin-bottom: 10px;
                            ">
                                <strong>{kom['user']}</strong>
                                <br>
                                {kom['pesan']}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        for idx_b_kom, bal in enumerate(kom["balasan"]):
                            st.markdown(
                                f"""
                                <div style="
                                    background-color: rgba(0,0,0,0.05);
                                    padding: 8px 10px;
                                    border-radius: 6px;
                                    margin-left: 30px;
                                    margin-bottom: 6px;
                                    border-left: 3px solid {accent_btn};
                                ">
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

elif navigasi == "Registrasi Akun":
    st.title("User Registration")

    t_reg1, t_reg2 = st.tabs(
        [
            "1. Ajukan ID Sementara",
            "2. Aktivasi Akun & Ubah Profil"
        ]
    )

    with t_reg1:
        with st.form("form_ajukan_id"):
            id_temp = st.text_input(
                "Masukkan ID Sementara Anda:"
            )

            if st.form_submit_button(
                "Kirim Pengajuan"
            ):
                if not id_temp:
                    st.warning(
                        "ID tidak boleh kosong."
                    )
                else:
                    found_req = next(
                        (
                            x
                            for x in db["antrian_registrasi"]
                            if x["id"] == id_temp
                        ),
                        None
                    )

                    if found_req:
                        pos = (
                            db["antrian_registrasi"]
                            .index(found_req)
                            + 1
                        )

                        st.info(
                            f"ID sudah terdaftar "
                            f"dalam antrean ke-#{pos}.\n"
                            f"Kode Admin: "
                            f"{found_req.get('kode', 'Menunggu pengiriman...')}"
                        )

                    else:
                        db[
                            "antrian_registrasi"
                        ].append(
                            {
                                "id": id_temp,
                                "kode": "",
                                "username": "",
                                "password": ""
                            }
                        )

                        simpan_data(db)

                        st.success(
                            "Pengajuan berhasil dikirim. "
                            f"Nomor antrean Anda: "
                            f"#{len(db['antrian_registrasi'])}"
                        )

    with t_reg2:
        with st.form("form_aktivasi_akun"):
            inp_id = st.text_input(
                "ID Sementara Anda:"
            )

            inp_kode = st.text_input(
                "Kode Verifikasi dari Admin:"
            )

            inp_new_u = st.text_input(
                "Username Baru:"
            )

            inp_new_p = st.text_input(
                "Password Baru:",
                type="password"
            )

            if st.form_submit_button(
                "Simpan Perubahan Akun"
            ):
                target_q = next(
                    (
                        x
                        for x in db["antrian_registrasi"]
                        if x["id"] == inp_id
                    ),
                    None
                )

                if not target_q:
                    st.error(
                        "ID tidak ditemukan "
                        "dalam antrean registrasi."
                    )

                elif target_q.get("kode") != inp_kode:
                    st.error(
                        "Kode verifikasi salah "
                        "atau belum dikirimkan oleh admin."
                    )

                elif inp_new_u in db["users_terdaftar"]:
                    st.error(
                        "Username tersebut "
                        "sudah digunakan orang lain."
                    )

                else:
                    db[
                        "users_terdaftar"
                    ][inp_new_u] = inp_new_p

                    db[
                        "antrian_registrasi"
                    ].remove(target_q)

                    simpan_data(db)

                    st.success(
                        "Akun berhasil diaktifkan. "
                        "Silakan lakukan login melalui "
                        "menu 'Masuk (Login)'."
                    )
