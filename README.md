Nama    : Silvia Lalita Damayanti
NPM     : 2506621863
Kelas   : PBP D

### Tugas 1
1. Saat merancang struktur HTML, saya menambahkan beberapa elemen semantik seperti <section> dan <article>. Semua ini saya gunakan untuk mengorganisasi konten-konten pada website serta mempermudah styling karena semantik membantu melabeli konten pada html dengan konteks yang jelas. Misalnya:
    - <section> saya gunakan untuk membagi website menjadi beberapa bagian berdasarkan topik, seperti section hero yang berisi profile dan section experience yang berisi detail pengalaman-pengalaman saya.
    - <article> saya gunakan pada bagian experience card karena memuat judul pengalaman, peran, dan deskripsi pengalaman yang membentuk suatu konten yang independen.
Namun saya tidak menggunakan elemen semantik <aside> karena sejauh ini portofolio saya belum memiliki konten yang membutuhkan fungsi semantik tersebut.
2. Dalam menyusun web yang responsive, kesulitan terbesar saya adalah menyesuaikan ukuran dan posisi elemen agar tetap proporsional pada ukuran layar yang berbeda. Contohnya saat mengerjakan bagian Experiences, pada ukuran default (desktop) saya menggunakan grid tiga kolom. Untuk menentukan kapan jumlah kolom perlu dikurangi menjadi dua lalu satu, saya mempertimbangkan lebar container yang saya gunakan, yaitu 960px. Saya membagi lebar tersebut menjadi tiga untuk memperkirakan lebar setiap card, kemudian menentukan breakpoint berdasarkan kapan dua atau tiga card tidak lagi dapat ditampilkan dengan lebar yang nyaman. Hal ini saya lakukan dengan mempertimbangkan keterbacaan dan kenyamanan pengguna, sehingga card tidak menjadi terlalu sempit dan informasi di dalamnya tetap mudah dibaca pada layar yang lebih kecil.
3. Karena website yang saya buat masih berupa static web, informasi di dalamnya masih harus dituliskan dan diubah secara langsung pada kode HTML. Hal ini cukup membatasi ketika saya ingin menambahkan atau memperbarui pengalaman di bagian Experience, karena setiap perubahan harus dilakukan secara manual. Selain itu, website saat ini belum dapat memberikan interaksi yang lebih kompleks kepada pengguna. Pada iterasi selanjutnya, saya ingin menambahkan sistem dinamis agar experience atau data-data lainnya dapat dikelompokkan berdasarkan kategori serta ditambahkan atau diperbarui dengan lebih mudah.
4. Deklarasi AI: Proses perancangan portofolio ini saya susun dengan bantuan AI ChatGPT. Proses pengerjaan Tugas 1 saya awali dengan membaca dan menonton tutorial HTML dan CSS di YouTube dan W3School, informasi-informasi yang tidak tercover di YouTube maupun W3School, seperti contohnya best practice, baru saya tanyakan kepada ChatGPT. Namun, jawaban yang diberikan saya evaluasi dan pelajari lagi lebih lanjut sebelum akhirnya saya terapkan dalam kode saya. Beberapa kesulitan yang saya alami dan tanyakan ke AI yakni:
    1. Menentukan best practice ukuran tiap header dan teks paragraph di website. Saya belum terbiasa pakai satuan rem dan menentukan rasio ukuran antar-header. Saya meminta panduan ukuran yang umum digunakan agar variasi hirarki teksnya proporsional (tidak terlalu besar/kecil).
        - "ubah rem ke px rumusnya apa dah"
        - "kalo h1 font-size: clamp(3rem, 7vw, 5rem); coba bikinin ke ak dong enaknya h2,3,4,5 seberapa"
    2. Mengevaluasi apakah susunan card yang saya gunakan sudah sesuai dengan best practice. Awalnya saya mengerjakan terlebih dahulu sesuai kemampuan dan pemahaman saya, kemudian saya kirimkan potongan kode yang telah saya buat beserta foto referensi wireframenya ke ChatGPT untuk dikoreksi. Dibalas dengan rekomendasi untuk menggunakan <article> karena sebelumnya saya masih menggunakan <div>. 
    3. Meminta format commit message yang rapi dan profesional dengan format conventional commits.



### Tugas 2
0. AI Disclosure: 
    Saya menggunakan AI ChatGPT sebagai alat bantu untuk memahami konsep Django MVT Architecture, mendapatkan masukan terkait implementasi dan struktur kode, menulis commit message di git yang rapi dan profesional, serta merapikan konten yang akan dimuat dalam portofolio. Seluruh keputusan dan implementasi akhir disesuaikan dan diperiksa kembali oleh saya.

    Sumber Belajar:
    Website PBP pbp.cs.ui.ac.id
    ChatGPT https://chatgpt.com/share/6aa7e920-2618-83ec-b187-5bcaff720735 
    Youtube https://youtu.be/c-6XRnYHbkw?si=OwLPrVYQKdLUJNRL 
1. Alur yang terjadi ketika pengguna membuka halaman Education
    Ketika pengguna membuka halaman portofolio baru, yaitu halaman Education pada Tugas 2, browser mengirimkan request ke proyek Django. Django pertama-tama mengecek portofolio/urls.py sebagai URL konfigurasi proyek untuk menentukan aplikasi yang menangani URL tersebut. Request kemudian diteruskan ke main/urls.py, yang memetakan URL tersebut ke view tertentu, yaitu show_education. View menjalankan logika yang diperlukan, salah satunya mengambil data dari model Education yang merepresentasikan data pendidikan di database. Setelah data diperoleh, view mengirimkannya sebagai context ke template education.html. Template kemudian menggunakan data tersebut untuk menghasilkan HTML secara dinamis. HTML hasil rendering selanjutnya dikirim kembali ke browser dan ditampilkan sebagai halaman Education.
2. Mengapa data disimpan di model, bukan template
    Karena model dan template memiliki tanggung jawab yang berbeda. Model mengurus data, sedangkan template mengurus tampilan. Jika data ditulis langsung di template, setiap ada perubahan atau penambahan data, developer harus mengedit kode HTML secara manual. Dengan model, data dapat dikelola melalui database atau Django Admin tanpa mengubah kode template. Selain itu, satu template dapat digunakan untuk menampilkan banyak objek dengan struktur yang sama, sehingga data tidak perlu ditulis berulang kali satu per satu. Jika ingin mengubah tampilan, developer juga cukup mengubah template satu kali dan perubahan tersebut akan diterapkan pada seluruh data yang ditampilkan. Hal ini membuat kode lebih mudah dipelihara dan dikembangkan, serta memungkinkan fitur seperti pencarian atau filter ditambahkan di kemudian hari.
3. Perbedaan "makemigrations" dan "migrate"
    makemigrations digunakan untuk membuat file migration berdasarkan perubahan yang dilakukan pada models.py. File tersebut berisi instruksi mengenai perubahan struktur database yang perlu dilakukan. Sementara itu, migrate digunakan untuk menerapkan migration tersebut ke database. Contohnya, pada project saya, saya menambahkan model Education yang berisi data riwayat pendidikan saya. Saya juga sempat menambahkan kategori "committee" pada model Experience untuk memperluas kategori pengalaman yang dapat dimasukkan. Setelah melakukan penambahan dan pengubahan pada model, saya jalankan:
        python manage.py makemigrations
        python manage.py migrate
    Dengan demikian, perubahan pada model dapat diterapkan pada struktur database.



### Tugas 3
0. Selama mengerjakan Tugas 3, saya menggunakan AI ChatGPT sebagai learning dan debugging assistant, terutama untuk membantu memahami konsep Django, mencari penyebab error, dan mengeksplorasi cara mengimplementasikan fitur. Jawaban yang diberikan telah saya evaluasi dan pelajari lagi lebih lanjut sebelum akhirnya saya terapkan dalam kode saya.
Beberapa hal yang saya tanyakan kepada AI antara lain:
    01.  Git Branch Workflow | Membantu menghafal syntax git, termasuk menyusun commit message yang profesional. link: https://chatgpt.com/share/6ab130d9-f254-83ec-b348-00eb05ef0b48
    02. Alur Forms & Data Delivery | Meringkas catatan pada Tutorial 3 dan memberikan hint serta arahan selama mengerjakan Tugas 3. link: https://chatgpt.com/share/6ab13193-4554-83ec-b8f7-8c1e50167a19
    03. Menggunakan Icon Dari BoxIcons | Mencari penyebab error dan bertanya seputar CSS. link: https://chatgpt.com/share/6ab131e2-2500-83ec-9362-30936dd96647
1. Jelaskan mengapa kita menggunakan ModelForm pada Django alih-alih membuat form HTML secara manual. Selain itu, jelaskan pula mengapa kita diwajibkan menambahkan {% csrf_token %} pada form tersebut!
    ModelForm digunakan karena dapat membuat form berdasarkan model Django yang sudah dibuat. Jadi, tidak perlu mendefinisikan setiap field secara manual di HTML dan mengatur sendiri bagaimana data dari form akan disimpan ke database. ModelForm juga membantu melakukan validasi data yang diisi pengguna dan menyediakan fungsi seperti form.save() untuk menyimpan data ke database. Contohnya pada project saya, ExperienceForm dibuat berdasarkan model Experience. 
    {% csrf_token %} digunakan untuk keamanan form dari CSRF (Cross-Site Request Forgery), yaitu serangan ketika pihak lain mencoba membuat user yang sedang login mengirim request ke website tanpa sepengetahuan user. Django menggunakan CSRF token untuk memastikan bahwa request POST tersebut berasal dari form yang memang dibuat oleh aplikasi kita. Oleh karena itu, form yang melakukan request seperti POST perlu menyertakan {% csrf_token %}
2. Pada Tutorial 03, kita membahas format data JSON dan   XML. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML?
    JSON (JavaScript Object Notation) lebih banyak digunakan karena formatnya lebih sederhana, ringkas, dan mlebih udah dibaca dan diproses dibandingkan XML. JSON juga memiliki struktur yang mirip dengan object dan array pada JavaScript, sehingga lebih mudah digunakan oleh aplikasi web. Contoh perbamndingan JSON dengan XML:
    JSON:
        {
            "title": "Portfolio Website",
            "description": "Personal portfolio menggunakan Django"
        }
    Sedangkan XML membutuhkan tag pembuka dan penutup:
        <project>
            <title>Portfolio Website</title>
            <description>Personal portfolio menggunakan Django</description>
        </project>
3. Jelaskan alur yang terjadi saat kamu menggunakan fungsi view untuk mengembalikan data portofoliomu dalam bentuk JSON. Mengapa kita perlu melakukan proses serialization pada model Django sebelum datanya dikembalikan?
    1. View mengambil data dari database menggunakan model Django. Misal:
        projects = Project.object.all()
    2. Data di-serialize dari object/queryset Django menjadi format JSON.
        projects_json = serializers.serialize("json",projects)
    3. View mengembalikan JSON sebagai response kepada client.
        return HttpResponse(projects_json, content_type="application/json")
    Serialization diperlukan karena data yang diambil dari database masih berupa object Django, sehingga perlu diubah menjadi format JSON agar dapat dikirim dan diproses oleh client atau aplikasi lain.
