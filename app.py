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
                    )
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
        with open(FILE_DATABASE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
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

if "admin_step" not in st.session_state:
    st.session_state.admin_step = 0

if "show_theme_selector" not in st.session_state:
    st.session_state.show_theme_selector = False

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
        padding-top: 20px !important;
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
    [data-testid="stSidebar"] div.stButton > button {{
        background-color: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        text-align: left;
        margin-bottom: 6px;
    }}
    [data-testid="stSidebar"] div.stButton > button:hover {{
        background-color: {accent_btn};
        border-color: transparent;
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

if st.sidebar.button("Beranda"):
    st.session_state.menu = "Beranda"
    st.session_state.selected_novel = None
    st.session_state.selected_bab = None
    st.session_state.admin_step = 0
    st.rerun()

if st.sidebar.button("Masuk (Login)"):
    st.session_state.menu = "Login"
    st.session_state.admin_step = 0
    st.rerun()

if st.sidebar.button("Registrasi Akun"):
    st.session_state.menu = "Registrasi"
    st.session_state.admin_step = 0
    st.rerun()

if st.sidebar.button("Koleksi Novel"):
    st.session_state.menu = "Koleksi"
    st.session_state.selected_novel = None
    st.session_state.selected_bab = None
    st.session_state.admin_step = 0
    st.rerun()

if st.session_state.is_admin:
    if st.sidebar.button("Admin Dashboard"):
        st.session_state.menu = "AdminDashboard"
        st.rerun()

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

if st.session_state.menu == "Beranda":
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

elif st.session_state.menu == "Login":
    st.title("User Login")

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
                    st.session_state.menu = "AdminDashboard"

                    st.success(
                        "Verifikasi sukses! "
                        "Mengalihkan ke halaman admin."
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

                        st.success(
                            f"Berhasil masuk sebagai {u_name}. "
                            "Silakan buka menu 'Koleksi Novel'."
                        )
                    else:
                        st.error(
                            "Username atau Password salah."
                        )

elif st.session_state.menu == "AdminDashboard":
    if not st.session_state.is_admin:
        st.error(
            "Akses ditolak! Halaman ini bersifat rahasia."
        )
    else:
        st.title("Admin Dashboard")

        if st.button("Keluar dari Mode Admin"):
            st.session_state.is_admin = False
            st.session_state.menu = "Beranda"
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
                    "**Bab Terdaftar:**"
                )

                if not target_n["babad"]:
                    st.caption(
                        "Belum ada bab."
                    )
                else:
                    for b_item in target_n["babad"]:
                        st.write(
                            f"- {b_item['nama_bab']}"
                        )

                st.markdown("---")

                with st.form("tambah_bab_form"):
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
                                    "komentar": []
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
                    st.write(
                        f"- Username: **{usr}** "
                        f"| Password: **{pwd}**"
                    )

elif st.session_state.menu == "Koleksi":
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
                                    )
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
                    for kom in current_bab["komentar"]:
                        st.markdown(
                            f"""
                            <div style="
                                background-color: {box_bg};
                                padding: 10px;
                                border-radius: 6px;
                                margin-bottom: 8px;
                            ">
                                <strong>{kom['user']}</strong>
                                <br>
                                {kom['pesan']}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

elif st.session_state.menu == "Registrasi":
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
