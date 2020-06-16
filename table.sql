CREATE TABLE company(
    name VARCHAR(150),
    ogrn VARCHAR(15) UNIQUE,
    okpo INT,
    current_status VARCHAR(35),
    reg_date DATE,
    auth_capital BIGINT
);
