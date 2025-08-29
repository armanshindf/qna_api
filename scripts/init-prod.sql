CREATE USER qna_user WITH PASSWORD 'secure_password';
CREATE DATABASE qna_prod OWNER qna_user;
GRANT ALL PRIVILEGES ON DATABASE qna_prod TO qna_user;