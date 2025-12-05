# Tổng quan về Cryptography (Mật mã học)

## 1. Cryptography là gì?

**Cryptography (mật mã học)** là ngành khoa học nghiên cứu các kỹ thuật bảo vệ thông tin trước đối thủ tấn công.

* Mục tiêu chính: biến **dữ liệu gốc (plaintext)** thành **dữ liệu đã mã hóa (ciphertext)** sao cho chỉ những người có **khóa bí mật phù hợp** mới khôi phục lại được.
* Cryptography không chỉ là “mã hóa/giải mã”, mà còn bao gồm:

  * Xác thực danh tính (authentication)
  * Đảm bảo toàn vẹn dữ liệu (integrity)
  * Chống chối bỏ (non‑repudiation)

Song song với đó là **Cryptanalysis (phá mã)** – nghiên cứu kỹ thuật tấn công, phân tích để phá vỡ hoặc làm suy yếu các hệ mật mã.

---

## 2. Các mục tiêu cốt lõi của mật mã học

Trong bảo mật thông tin, cryptography thường được dùng để đạt các thuộc tính sau:

1. **Confidentiality (Bí mật):**

   * Chỉ những bên được phép mới đọc được dữ liệu.
   * Ví dụ: nội dung tin nhắn trên Messenger/Signal/Telegram.

2. **Integrity (Toàn vẹn):**

   * Dữ liệu không bị thay đổi trái phép trong quá trình lưu trữ hay truyền tải.
   * Nếu có thay đổi, hệ thống phải phát hiện được.

3. **Authentication (Xác thực):**

   * Xác minh danh tính của người dùng hoặc dịch vụ.
   * Ví dụ: đăng nhập với mật khẩu, OTP, khóa công khai, chứng thư số.

4. **Non‑repudiation (Chống chối bỏ):**

   * Người gửi không thể phủ nhận việc đã gửi một thông điệp.
   * Thường dùng chữ ký số, chứng thư số.

5. (Tuỳ ngữ cảnh) **Availability (Khả dụng):**

   * Hệ thống vẫn sẵn sàng phục vụ, không bị tê liệt bởi tấn công.

---

## 3. Các nhóm thuật toán mật mã chính

### 3.1. Mật mã khóa đối xứng (Symmetric Cryptography)

* **Đặc trưng:** cùng **một khóa bí mật** dùng cho cả mã hóa và giải mã.
* Thường dùng cho mã hóa **khối lượng dữ liệu lớn** vì nhanh, hiệu quả.

#### 3.1.1. Mã khối (Block cipher)

* Là thuật toán mã hóa dữ liệu theo **từng khối có kích thước cố định** (ví dụ 64 bit, 128 bit…).
* Ví dụ tiêu biểu:

  * **DES, 3DES** .
  * **AES** .

#### 3.1.2. Mã dòng (Stream cipher)

* Tạo ra một **key stream** (chuỗi bit giả ngẫu nhiên) rồi XOR với plaintext.
* Ví dụ: ChaCha20, các stream cipher trong chuẩn di động.

### 3.2. Mật mã khóa công khai (Asymmetric/Public‑key Cryptography)

* Mỗi thực thể có **cặp khóa**:

  * **Khóa công khai (public key):** được công bố.
  * **Khóa bí mật (private key):** bí mật - các bên liên quan giữ.
* Các ứng dụng chính:

1. **Mã hóa khóa (key encapsulation / key exchange):**

   * Dùng public‑key để **trao đổi một khóa đối xứng an toàn**, sau đó dùng khóa đối xứng để mã hóa dữ liệu lớn.
   * Ví dụ: **RSA**, **Diffie–Hellman**, **ECDH**.

2. **Chữ ký số (Digital Signature):**

   * Dùng private key để ký, public key để kiểm tra chữ ký.
   * Đảm bảo **tính toàn vẹn** và **chống chối bỏ**.
   * Ví dụ: RSA signature, ECDSA, EdDSA, các chữ ký hậu lượng tử (Dilithium, Falcon…).

> Thực tế, hầu hết hệ thống thực tế sử dụng **kết hợp**: public‑key cho trao đổi khóa, symmetric‑key cho mã hóa dữ liệu.

### 3.3. Hàm băm (Cryptographic Hash Function)

* Hàm ( H ) nhận vào thông điệp tùy ý độ dài, trả về **hash** (digest) có độ dài cố định.
* Thuộc tính quan trọng:

  * **Preimage resistance:** khó tìm ( m ) sao cho ( H(m) = y ) đã cho.
  * **Second preimage resistance:** khó tìm ( m' \neq m ) sao cho ( H(m) = H(m') ).
  * **Collision resistance:** khó tìm **hai thông điệp khác nhau** cùng hash.
* Ứng dụng:

  * Kiểm tra toàn vẹn file (checksum an toàn).
  * Lưu trữ mật khẩu (hash + salt).
  * Thành phần trong chữ ký số, blockchain, commitment,…

### 3.4. MAC, AEAD, KDF và các primitive khác

1. **MAC (Message Authentication Code):**

   * Đảm bảo **toàn vẹn + xác thực** dùng **khóa bí mật chung**.
   * Ví dụ: HMAC‑SHA256, CMAC‑AES.

2. **AEAD (Authenticated Encryption with Associated Data):**

   * Mã hóa **có xác thực** trong một bước.
   * Ví dụ: AES‑GCM, ChaCha20‑Poly1305.

3. **KDF (Key Derivation Function):**

   * Dùng để sinh khóa từ một bí mật gốc (master key, mật khẩu, seed…).
   * Ví dụ: HKDF, PBKDF2, scrypt, Argon2.

4. **PRNG/DRBG (Pseudo‑Random Number Generator):**

   * Sinh số giả ngẫu nhiên phục vụ sinh khóa, IV, nonce.
   * Chất lượng PRNG kém có thể làm **toang cả hệ mật mã**.

---

## 4. Ứng dụng mật mã vào các giao thức và hệ thống

Trong thực tế, các primitive mật mã được **ghép lại thành giao thức** để giải quyết bài toán cụ thể:

* **TLS / HTTPS:** bảo vệ kết nối web (mã hóa kênh giữa trình duyệt và server).
* **VPN (IPsec, OpenVPN, WireGuard):** bảo vệ luồng dữ liệu giữa hai mạng.
* **SSH:** truy cập shell từ xa an toàn.
* **Disk encryption (BitLocker, LUKS,…):** mã hóa ổ đĩa, USB, SSD.
* **Ứng dụng nhắn tin (Signal, WhatsApp,…):** dùng end‑to‑end encryption với nhiều lớp primitive (X3DH, Double Ratchet, AEAD…).
* **Blockchain / tiền mã hóa:** dùng chữ ký số, hash, Merkle tree để đảm bảo toàn vẹn và đồng thuận.

Việc thiết kế **giao thức** đúng còn khó hơn việc chọn thuật toán, vì rất nhiều lỗ hổng xuất phát từ logic protocol hoặc implement sai.

---

## 5. Các kiểu tấn công trong mật mã học (Khái quát)

1. **Brute‑force / Exhaustive search:**

   * Thử mọi khóa có thể. Do đó, độ dài khóa phải đủ lớn.

2. **Cryptanalytic attacks:**

   * Khai thác cấu trúc toán học của thuật toán (differential, linear cryptanalysis, algebraic attack,…).
   * Chủ yếu nhắm vào các block cipher và stream cipher thiết kế yếu.

3. **Attack trên mode/protocol/implementation:**

   * Padding oracle, downgrade attack, replay, tấn công vào lỗi logic giao thức.
   * Lỗi implement: dùng IV/nonce trùng, random yếu, quên kiểm tra MAC,…

4. **Side‑channel attacks:**

   * Khai thác rò rỉ vật lý: thời gian chạy, mức tiêu thụ điện, sóng điện từ, lỗi phần cứng,…

5. **Human‑factor / misconfiguration:**

   * Quản lý khóa kém, để lộ private key, dùng mật khẩu yếu, cấu hình sai (dùng thuật toán cũ, tắt verify certificate,…).

---
