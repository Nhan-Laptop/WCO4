# Symmetric Cipher

Symmetric cipher (mật mã đối xứng) là phương pháp mã hóa sử dụng cùng một khóa bí mật cho cả mã hóa và giải mã. Nhờ tốc độ xử lý nhanh và hiệu suất cao, nó được dùng rộng rãi trong thực tế để bảo vệ dữ liệu trong HTTPS, VPN, mã hóa ổ đĩa và ứng dụng nhắn tin. Các thuật toán như AES và ChaCha20 chính là nền tảng giúp đảm bảo tính bảo mật của hầu hết hệ thống truyền thông hiện đại.
Các loại mã hóa đối xứng hiện nay được chia ra thành 2 loại cơ bản:
- Stream cipher
- Block cipher

## Block Cipher

Block cipher là thuật toán mật mã đối xứng mã hóa dữ liệu theo từng khối (block) có kích thước cố định — phổ biến nhất là 128 bit. Mỗi block plaintext sẽ được biến đổi thành một block ciphertext thông qua một hàm phụ thuộc vào khóa bí mật.

Ví dụ:
- [Advanced Encryption Standard (AES)](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
- [Data Encryption Standard (DES)](https://littlenopro.github.io/posts/DES/)

Trong thực tế, block cipher không hoạt động một mình mà cần mode of operation (CBC, CTR, GCM…) để xử lý dữ liệu dài hơn một block.

Ưu điểm:
- Bảo mật cao khi dùng mode đúng (ví dụ GCM)
- Phù hợp cho mã hóa dữ liệu lớn (ổ đĩa, file, database)

Nhược điểm:
- Cần padding nếu dữ liệu không đủ block
- Tốc độ mã hóa và giải mã khá chậm

## Stream Cipher

Stream cipher là thuật toán mật mã đối xứng mã hóa dữ liệu từng bit hoặc từng byte một. Nó tạo ra một chuỗi khóa giả ngẫu nhiên (keystream), sau đó XOR với plaintext để tạo ciphertext:

$$
C = P \oplus \text{keystream}
$$

Ví dụ:
- [RC4]((https://littlenopro.github.io/posts/Stream_Ciphers/))
- [ChaCha20]((https://littlenopro.github.io/posts/Stream_Ciphers/))

Stream cipher thường dùng cho dữ liệu truyền liên tục như âm thanh, video, hoặc giao thức mạng thời gian thực.

Ưu điểm:
- Không cần padding
- Nhanh và hiệu quả cho dữ liệu luồng, độ trễ thấp

Nhược điểm:
- Nếu keystream bị lộ hoặc trùng lặp -> có thể bị phá mã nhanh chóng.

## Bài tập

Làm hết phần https://cryptohack.org/challenges/aes/.
