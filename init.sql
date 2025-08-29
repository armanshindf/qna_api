CREATE USER qna_user WITH PASSWORD 'secure_password';
CREATE DATABASE qna_db OWNER qna_user;
GRANT ALL PRIVILEGES ON DATABASE qna_db TO qna_user;

\c qna_db;

GRANT ALL ON SCHEMA public TO qna_user;